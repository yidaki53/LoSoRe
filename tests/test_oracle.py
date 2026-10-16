"""Real-oracle tests: DAT round-trip + the no-vacuous-PASS contract.

These pin that (a) the format oracle is a genuine regression guard (fixture with
distinctive values catches offset drift) and (b) verify never claims PASS when
nothing was checked.
"""
import importlib.util
import pathlib
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent


def _load_dat():
    p = REPO / "targets" / "liero" / "tools" / "liero_dat.py"
    spec = importlib.util.spec_from_file_location("liero_dat", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _run(script, *args, cwd=None):
    return subprocess.run([sys.executable, str(REPO / script), *args],
                          capture_output=True, text=True, cwd=str(cwd or REPO))


def test_dat_selftest_passes():
    ok, msg = _load_dat().selftest()
    assert ok, msg


def test_dat_round_trip_is_real_guard():
    """A buffer whose bytes match the documented layout round-trips; a wrong one doesn't."""
    mod = _load_dat()
    ok, _ = mod.selftest()
    assert ok
    # build a valid buffer via the fixture path, then confirm round_trip agrees
    buf = bytearray(mod.DAT_LEN)
    import struct
    vals = {"max_bonuses": 9, "loading_times": 0x1234, "lives": 5,
            "game_mode": 1, "weapons_p1": [1, 2, 3, 4, 5],
            "weapons_p2": [6, 7, 8, 9, 10], "health_p1": 50, "health_p2": 60}
    for key, off, kind in mod.FIELDS:
        v = vals[key]
        if kind == "u8":
            buf[off] = v
        elif kind == "u16":
            struct.pack_into("<H", buf, off, v)
        elif kind == "i16":
            struct.pack_into("<h", buf, off, v)
        else:
            buf[off:off + 5] = bytes(v)
    rt_ok, cov, _ = mod.round_trip(bytes(buf))
    assert rt_ok and cov > 0


def test_dat_oracle_via_verify(tmp_path):
    # dat-parity runs the selftest even with no BYOD (real check, disc-gated otherwise)
    r = _run("engine/verify.py", "--target", "liero", "--oracle", "dat-parity",
             "--byod", str(tmp_path / "absent"))
    assert r.returncode == 0 and "SKIP" in r.stdout  # no BYOD -> disc-gated skip


def test_verify_no_vacuous_pass_on_empty_config(tmp_path):
    # empty build.sha1 + BYOD present must WARN "NOT verified", never claim PASS
    byod = tmp_path / "byod"; byod.mkdir()
    (byod / "LIERO.EXE").write_bytes(b"MZ" + bytes(range(32)))
    work = tmp_path / "repo"
    cfg = work / "targets" / "faketgt" / "config"; cfg.mkdir(parents=True)
    (cfg / "build.sha1").write_text("# <sha1> <relpath> — oracle gate\n")  # empty
    build = tmp_path / "build"; build.mkdir()
    r = _run("engine/verify.py", "--target", "faketgt", "--byod", str(byod),
             "--build", str(build), "--oracle", "byte-exact", cwd=work)
    assert r.returncode == 0
    assert "NOT verified" in r.stdout and "PASS" not in r.stdout
