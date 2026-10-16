// Export per-function disassembly + metadata for the Lost-Source Revival Factory.
// Ghidra Java post-script. Writes into LSR_OUTDIR (env) or scriptArgs[0]:
//   asm/<func>.s      raw instruction listing per function
//   decomp/<func>.c   best-effort decompiler output
//   functions.json    metadata: name, entry, size, instr count, params, cc
//@category LSR
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.listing.*;
import ghidra.program.model.address.*;
import ghidra.program.model.symbol.*;
import java.io.*;
import java.nio.file.*;
import java.util.*;

public class ExportFuncs extends GhidraScript {
    @Override
    public void run() throws Exception {
        Program prog = currentProgram;
        FunctionManager fm = prog.getFunctionManager();
        Listing listing = prog.getListing();

        String outdir = null;
        try {
            String[] a = getScriptArgs();
            if (a != null && a.length > 0) outdir = a[0];
        } catch (Exception ignore) {}
        if (outdir == null) outdir = System.getenv("LSR_OUTDIR");
        if (outdir == null) outdir = System.getProperty("user.dir");

        Path asmDir = Paths.get(outdir, "asm");
        Path decompDir = Paths.get(outdir, "decomp");
        Files.createDirectories(asmDir);
        Files.createDirectories(decompDir);

        DecompInterface decomp = new DecompInterface();
        decomp.openProgram(prog);

        StringBuilder meta = new StringBuilder();
        meta.append("{\n  \"program\": \"").append(esc(prog.getName())).append("\",\n");
        meta.append("  \"executable_path\": \"").append(esc(prog.getExecutablePath())).append("\",\n");
        meta.append("  \"language\": \"").append(esc(prog.getLanguageID().toString())).append("\",\n");
        meta.append("  \"compiler\": \"").append(esc(prog.getCompiler())).append("\",\n");
        meta.append("  \"image_base\": \"").append(esc(prog.getImageBase().toString())).append("\",\n");
        meta.append("  \"functions\": [\n");

        int n = 0;
        FunctionIterator it = fm.getFunctions(true);
        while (it.hasNext()) {
            Function func = it.next();
            String name = func.getName();
            String entry = func.getEntryPoint().toString();
            AddressSetView body = func.getBody();
            long size = body.getNumAddresses();

            // instruction listing
            StringBuilder sb = new StringBuilder();
            sb.append("; ").append(name).append("  entry=").append(entry)
              .append(" size=").append(size).append("\n");
            int ninstr = 0;
            InstructionIterator ii = listing.getInstructions(body, true);
            while (ii.hasNext()) {
                Instruction instr = ii.next();
                sb.append(instr.getAddressString(false, true)).append("  ")
                  .append(instr.toString()).append("\n");
                ninstr++;
            }
            Files.write(asmDir.resolve(safe(name) + ".s"),
                        sb.toString().getBytes("UTF-8"));

            // params
            StringBuilder params = new StringBuilder();
            Parameter[] ps = func.getParameters();
            for (int i = 0; i < ps.length; i++) {
                if (i > 0) params.append(",");
                params.append("\"").append(esc(ps[i].getName())).append("\"");
            }

            // best-effort decompile
            boolean cOk = false;
            try {
                DecompileResults res = decomp.decompileFunction(func, 120, monitor);
                if (res != null && res.decompileCompleted() && res.getDecompiledFunction() != null) {
                    Files.write(decompDir.resolve(safe(name) + ".c"),
                                res.getDecompiledFunction().getC().getBytes("UTF-8"));
                    cOk = true;
                }
            } catch (Exception ignore) {}

            if (n > 0) meta.append(",\n");
            meta.append("    {\"name\": \"").append(esc(name)).append("\", ")
                .append("\"entry\": \"").append(entry).append("\", ")
                .append("\"size\": ").append(size).append(", ")
                .append("\"num_instructions\": ").append(ninstr).append(", ")
                .append("\"params\": [").append(params).append("], ")
                .append("\"calling_convention\": \"").append(esc(func.getCallingConventionName())).append("\", ")
                .append("\"decompiled\": ").append(cOk).append("}");
            n++;
        }
        meta.append("\n  ],\n  \"num_functions\": ").append(n).append("\n}\n");
        Files.write(Paths.get(outdir, "functions.json"), meta.toString().getBytes("UTF-8"));

        println("[ExportFuncs] wrote " + n + " functions to " + outdir);
    }

    private static String safe(String n) {
        StringBuilder b = new StringBuilder();
        for (char c : n.toCharArray()) {
            boolean ok = (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')
                    || (c >= '0' && c <= '9') || c == '-' || c == '_' || c == '.';
            b.append(ok ? c : '_');
        }
        String s = b.toString();
        return s.isEmpty() ? "unnamed" : s;
    }

    private static String esc(String s) {
        if (s == null) return "";
        return s.replace("\\", "\\\\").replace("\"", "\\\"");
    }
}
