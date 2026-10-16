#@category LSR
# Export per-function disassembly + metadata for the Lost-Source Revival Factory.
# Runs as a Ghidra post-script (Jython). Writes:
#   <outdir>/asm/<func>.s        raw instruction listing per function
#   <outdir>/functions.json      metadata: name, entry, size, calls, params
# Args (via -postScript ExportFuncs "<outdir>" or getScriptArgs): [outdir]
import os, json
from ghidra.app.decompiler import DecompInterface
from ghidra.program.model.address import AddressSet

prog = currentProgram
fm = prog.getFunctionManager()
listing = prog.getListing()

# resolve outdir from script args or env
outdir = None
try:
    args = getScriptArgs()
    if args:
        outdir = args[0]
except Exception:
    pass
if not outdir:
    outdir = os.environ.get("LSR_OUTDIR")
if not outdir:
    outdir = os.path.join(os.getcwd(), "targets", prog.getName(), "_lsr_export")

asm_dir = os.path.join(outdir, "asm")
if not os.path.isdir(asm_dir):
    os.makedirs(asm_dir)

# decompiler (best-effort; may fail for some funcs)
decomp = DecompInterface()
decomp.openProgram(prog)

def safe_name(n):
    keep = "-_.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(c if c in keep else "_" for c in n) or "unnamed"

funcs_meta = []
for func in fm.getFunctions(True):
    name = func.getName()
    entry = func.getEntryPoint().toString()
    body = func.getBody()
    size = body.getNumAddresses()

    # instruction listing
    lines = []
    instr_iter = listing.getInstructions(body, True)
    ninstr = 0
    while instr_iter.hasNext():
        instr = instr_iter.next()
        lines.append("%s  %s" % (instr.getAddressString(False, True),
                                 instr.toString()))
        ninstr += 1

    # called functions
    called = sorted(set(
        r.getToAddress().toString()
        for r in prog.getReferenceManager().getReferencesTo(func.getEntryPoint())
    ))
    callees = []
    for ref in prog.getReferenceManager().getReferencesFrom(func.getEntryPoint()):
        pass

    # parameters
    params = [p.getName() for p in func.getParameters()]

    with open(os.path.join(asm_dir, safe_name(name) + ".s"), "w") as f:
        f.write("; %s  entry=%s size=%d\n" % (name, entry, size))
        f.write("\n".join(lines))
        f.write("\n")

    # best-effort decompile
    c_ok = False
    try:
        res = decomp.decompileFunction(func, 120, monitor)
        if res is not None and res.decompileCompleted():
            cf = res.getDecompiledFunction()
            if cf is not None:
                cpath = os.path.join(outdir, "decomp", safe_name(name) + ".c")
                if not os.path.isdir(os.path.dirname(cpath)):
                    os.makedirs(os.path.dirname(cpath))
                with open(cpath, "w") as f:
                    f.write(cf.getC())
                c_ok = True
    except Exception:
        pass

    funcs_meta.append({
        "name": name, "entry": entry, "size": size,
        "num_instructions": ninstr, "params": params,
        "calling_convention": str(func.getCallingConventionName()),
        "decompiled": c_ok,
    })

meta = {
    "program": prog.getName(),
    "executable_path": prog.getExecutablePath(),
    "language": str(prog.getLanguageID()),
    "compiler": str(prog.getCompiler()),
    "image_base": str(prog.getImageBase()),
    "num_functions": len(funcs_meta),
    "functions": funcs_meta,
}
with open(os.path.join(outdir, "functions.json"), "w") as f:
    json.dump(meta, f, indent=2)

print("[ExportFuncs] wrote %d functions to %s" % (len(funcs_meta), outdir))
