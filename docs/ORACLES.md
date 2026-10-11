# Oracles — strongest first
1. byte-exact: rebuilt bytes == original (reccmp/asm-differ).
2. relocation-aware: equal modulo addresses/relocs.
3. round-trip: .bin->src->.bin identical with original compiler (pathologic_re pattern).
4. trace-parity: Frida draw/call traces equal (openrecet pattern).
Every function record stores which oracle passed. No pass = not decompiled.
