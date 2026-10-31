import pathlib

p = pathlib.Path(__file__).resolve().parent.parent / "engine" / "draft.py"
s = p.read_text()

# 1. C-residue gate: ';' is also Pascal's statement terminator — counting it
#    rejects nearly all valid LLM Pascal. Only C-exclusive markers count.
old1 = r'''_C_LINE_RE = re.compile(r"[;{}]|->|::|#include|^\s*(int|void|char|unsigned)\b")'''
new1 = r'''_C_LINE_RE = re.compile(r"[{}]|->|::|#include|^\s*(int|void|char|unsigned|uint\w*|u?int\d+_t|size_t)\b")'''
assert s.count(old1) == 1, f"p1: {s.count(old1)}"
s = s.replace(old1, new1)

# 2. _parse_decl: strip calling-convention tokens (__cdecl16near etc.) so the
#    return type is read from the real type word, not the convention.
old2 = '''    ret_words = m.group(1).split()
    ret = ret_words[-1].lower() if ret_words else "void"
'''
new2 = '''    ret_words = [w for w in m.group(1).split() if not w.startswith("__")]
    ret = ret_words[-1].lower() if ret_words else "void"
'''
assert s.count(old2) == 1, f"p2: {s.count(old2)}"
s = s.replace(old2, new2)

# 3a. Truncate the prompt's REFERENCE C (full 71KB seeds overflow the 8k server
#     context -> HTTP 400). Decl parsing still uses the full seed_c.
old3 = '''                            sib_txt = ("Called routines are forward-declared with EXACTLY "
                                       "these signatures — match arity and argument types "
                                       "when calling:\\n" + rows + "\\n")
                    prompt = (
'''
new3 = '''                            sib_txt = ("Called routines are forward-declared with EXACTLY "
                                       "these signatures — match arity and argument types "
                                       "when calling:\\n" + rows + "\\n")
                    prompt_seed = seed_c[:3500] + ("\\n... [reference C truncated for length]"
                                                  if len(seed_c) > 3500 else "")
                    prompt = (
'''
assert s.count(old3) == 1, f"p3: {s.count(old3)}"
s = s.replace(old3, new3)

# 3b. Prompt rules: forbid goto/labels and Delphi Result (both seen failing FPC).
old4 = '''                        "- Keep value types exact: never assign Word/Integer to Char or vice "
                        "versa - convert with `Chr(n)`/`Ord(c)`/`Byte(x)`/`Word(x)`. The "
                        "sibling signature table is authoritative for return types.\\n"
'''
new4 = '''                        "- Keep value types exact: never assign Word/Integer to Char or vice "
                        "versa - convert with `Chr(n)`/`Ord(c)`/`Byte(x)`/`Word(x)`. The "
                        "sibling signature table is authoritative for return types.\\n"
                        "- No `goto` and no `label` declarations — restructure jumps with "
                        "`if`/`while`/`repeat` loops.\\n"
                        "- Return a value by assigning the routine's own name "
                        "(`FUN_xxxx := ...`); never use Delphi's `Result`.\\n"
'''
assert s.count(old4) == 1, f"p4: {s.count(old4)}"
s = s.replace(old4, new4)

# 3c. Use the truncated seed in the prompt body.
old5 = r'''                        f"ASSEMBLY:\n{asm_text}\n\nREFERENCE C ({ref_source}, "
                        f"for meaning only):\n{seed_c}\n")'''
new5 = '''                        f"ASSEMBLY:\\n{asm_text}\\n\\nREFERENCE C ({ref_source}, "
                        f"for meaning only):\\n{prompt_seed}\\n")'''
assert s.count(old5) == 1, f"p5: {s.count(old5)}"
s = s.replace(old5, new5)

# 4. Compile gate: iterate revert passes (up to 3) so one pass's fallout
#    (e.g. newly-unsolved forwards) is also reverted -> guaranteed GREEN.
old6 = '''    for stem in sorted(bad):
        p = src / f"{stem}.inc"
        if not p.exists() or stem.startswith("_"):
            continue
        seed = read_decomp_seed(root, stem)
        ref_source = "Ghidra"
        if recon is not None:
            rcode, rwhy = read_recon_seed(recon, stem, allowed or set())
            if rcode:
                seed, ref_source = rcode, f"recon:{rwhy}"
        ref = _c_ref_block(seed, ref_source) if seed else "(* no decompiler seed yet *)"
        p.write_text(PAS_TEMPLATE.format(
            slug=target, fn=stem,
            kind=_yaml_kv(root / "config" / "target.yaml", "kind", "game"),
            oracle="none", backend="skeleton(compile-gate)", ref=ref,
            sig=_pascal_fn_skeleton(stem, _decl_for(root, stem, recon, allowed))))
        reverted += 1
    still, why2 = _errors()
'''
new6 = '''    for _pass in range(3):
        for stem in sorted(bad):
            p = src / f"{stem}.inc"
            if not p.exists() or stem.startswith("_"):
                continue
            seed = read_decomp_seed(root, stem)
            ref_source = "Ghidra"
            if recon is not None:
                rcode, rwhy = read_recon_seed(recon, stem, allowed or set())
                if rcode:
                    seed, ref_source = rcode, f"recon:{rwhy}"
            ref = _c_ref_block(seed, ref_source) if seed else "(* no decompiler seed yet *)"
            p.write_text(PAS_TEMPLATE.format(
                slug=target, fn=stem,
                kind=_yaml_kv(root / "config" / "target.yaml", "kind", "game"),
                oracle="none", backend="skeleton(compile-gate)", ref=ref,
                sig=_pascal_fn_skeleton(stem, _decl_for(root, stem, recon, allowed))))
            reverted += 1
        bad, why = _errors()
        if not bad:
            break
    still, why2 = _errors()
'''
assert s.count(old6) == 1, f"p6: {s.count(old6)}"
s = s.replace(old6, new6)

p.write_text(s)
print("fix_semantics ok: C-gate, conventions, truncation, goto/Result, gate loop")
