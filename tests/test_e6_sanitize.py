"""Regression tests for tools/e6_match.py prompt/sanitize pipeline.

Pins the three overnight6 failure modes: Ghidra/C type spellings leaking
into TP7 output, markdown fences/backticks in model output, and the
loop-structure outline that the prompt feeds to the model.
"""
import importlib.util
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent


def _load():
    sys.path.insert(0, str(REPO / "tools"))
    spec = importlib.util.spec_from_file_location(
        "e6_match", REPO / "tools" / "e6_match.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_fix_types_maps_ghidra_c_spellings():
    e6 = _load()
    src = ("var local_4: uint;\n"
           "var local_6: int;\n"
           "var local_8: undefined4;\n"
           "var local_a: qword;\n"
           "var local_b: unsigned;\n")
    out = e6._fix_types(src)
    assert "uint" not in out
    assert ": int;" not in out
    assert "undefined4" not in out
    assert "QWord" not in out and "qword" not in out
    assert "local_4: Word;" in out
    assert "local_6: Integer;" in out
    assert "local_8: Longint;" in out


def test_fix_types_leaves_identifiers_alone():
    e6 = _load()
    src = "MemW[0x4c] := local_104 xor integer_of_point;\n"
    # identifiers containing 'int'/'eger' substrings must survive
    assert e6._fix_types(src) == src


def test_sanitize_strips_fences_and_backticks():
    e6 = _load()
    raw = ("```pascal\n"
           "procedure FUN_X(param_1: Word);\n"
           "begin\n"
           "  param_1 := param_1 + 1;\n"
           "end;\n"
           "```\n")
    out = e6.sanitize_pas(raw, "FUN_X", "procedure FUN_X(param_1: Word);")
    assert "```" not in out
    assert "`" not in out
    assert out.lstrip().startswith("procedure FUN_X")
    assert out.rstrip().endswith("end;")


def test_sanitize_native_pascal_pass():
    e6 = _load()
    raw = ("procedure FUN_X;\nvar\n  n: int;\nbegin\n  n := 0;\nend;\n")
    out = e6.sanitize_pas(raw, "FUN_X", "procedure FUN_X;")
    assert "n: Integer;" in out


def test_fix_arity_truncates_surplus_args():
    e6 = _load()
    # FUN_24dd_3eaf is declared with 3 params in _forward.inc
    src = ("  FUN_24dd_3eaf(5, s3, s, $CC, $24DD);\n"
           "  FUN_24dd_3e95(s3, s);\n")
    out = e6._fix_arity(src)
    assert "FUN_24dd_3eaf(5, s3, s)" in out
    # correctly-arity calls pass through untouched
    assert "FUN_24dd_3e95(s3, s)" in out


def test_fix_arity_zero_param_function():
    e6 = _load()
    # FUN_24dd_3dbd is declared with no params
    out = e6._fix_arity("  x := FUN_24dd_3dbd(a, b);\n")
    assert "FUN_24dd_3dbd;" in out or out.strip().endswith("FUN_24dd_3dbd")


def test_fix_types_strips_register_and_typedefs():
    e6 = _load()
    # C storage-class keyword is deleted as a whole token
    assert "register" not in e6._fix_types("var x: register Word;")
    # _t typedefs map onto TP7 spellings
    out = e6._fix_types("var a: byte_t; b: word_t; c: uint32_t;")
    assert "byte_t" not in out and "word_t" not in out and "uint32_t" not in out
    assert "Byte" in out and "Word" in out and "Longint" in out


def test_declare_undeclared_adds_missing_locals():
    e6 = _load()
    body = ("procedure P(param_1: Word);\nvar\n  a: Word;\nbegin\n"
            "  a := d + i;\n  v2 := param_1;\nend;\n")
    out = e6._declare_undeclared(body)
    # d, i, v2 are now declared; a and param_1 are not duplicated
    for name in ("d", "i", "v2"):
        assert re.search(rf"^\s*{name}\s*:\s*Word\s*;", out, re.M), name
    assert len(re.findall(r"^\s*a\s*:\s*Word\s*;", out, re.M)) == 1
    assert len(re.findall(r"param_1\s*:\s*Word", out)) == 1
    # known types/keywords never get declared
    assert not re.search(r"^\s*begin\s*:", out, re.M)


def test_declare_undeclared_ignores_fun_and_known():
    e6 = _load()
    body = ("procedure P;\nbegin\n  Mem[0] := 1;\n  FUN_abc(2);\n  Inc(MemW[4]);\nend;\n")
    out = e6._declare_undeclared(body)
    # no bogus declarations for Mem/FUN_abc/MemW
    assert "Mem:" not in out.replace("MemW:", "")
    assert "FUN_abc" not in out.split("begin")[0]


def test_expand_ptr_stmts_derefs_and_increments():
    e6 = _load()
    # cast-pointer store with post-increment becomes MemW store + Inc
    out = e6._normalize_c_early("*(Byte*)param_4++ = wDestLen;")
    assert "MemW[Word(param_4)] := wDestLen" in out
    assert "Inc(param_4)" in out
    # deref load
    out = e6._normalize_c_early("wSrcLen = *(Byte*)param_3;")
    assert "MemW[Word(param_3)]" in out
    # pointer bump compount assignment
    assert e6._normalize_c_early("param_4 += line_rem;") == "Inc(param_4, line_rem)"
    # standalone ++ / --
    assert e6._normalize_c_early("p++;") == "Inc(p)"
    assert e6._normalize_c_early("q--;") == "Dec(q)"
    # multiplication must survive
    assert e6._normalize_c_early("x = a * b;") == "x = a * b;"
    # GCC inline-asm crumbs collapse away
    assert e6._normalize_c_early("__asm__ __volatile__(;") == ""
    assert e6._normalize_c_early('"pushl %%bp\\n";') == ""
    # storage-class keywords are stripped
    assert "register" not in e6._normalize_c_early("register x = 1;")


def test_normalize_for_countdown_and_casts():
    e6 = _load()
    # for (i = start; i; i--) sentinel
    assert e6._normalize_c_early("for (i = param_2; i; i--);") == \
        "for__countdown__i__param_2"
    # scalar casts vanish (no-op C casts -> nothing)
    assert e6._normalize_c_early("x = (int)y;") == "x = y;"
    assert e6._normalize_c_early("x = (unsigned short)y;") == "x = y;"


def test_strip_stmt_decls_removes_c_leak():
    e6 = _load()
    src = ("procedure P;\nvar\n  x: Word;\nbegin\n"
           "  x := 1;\n  Word param_1;\n  Byte y2 = 3;\n"
           "  x := 2;\nend;\n")
    out = e6._strip_stmt_decls(src)
    assert "Word param_1;" not in out
    assert "Byte y2 = 3;" not in out
    # assignments and the var block survive
    assert "x := 1;" in out
    assert "x := 2;" in out
    assert "  x: Word;" in out


def test_region_outline_reports_real_loop():
    e6 = _load()
    asm = (REPO / "targets" / "liero-dos" / "asm" / "FUN_1000_5e66.s").read_text(
        errors="replace")
    out = e6.region_outline(asm)
    assert "loop@0x" in out
    assert "instrs" in out
    # 20 natural loops in this routine (asmcfg-verified); outline caps at 40
    assert out.count("loop@0x") == 20


def test_region_outline_straight_line_degrades():
    e6 = _load()
    out = e6.region_outline("no assembly here at all")
    assert "no loops" in out or "unavailable" in out
