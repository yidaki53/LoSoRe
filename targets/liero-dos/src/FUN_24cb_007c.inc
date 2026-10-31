{ liero-dos::FUN_24cb_007c — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24cb_007c.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24cb_007c.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: recon:real decompiler C (unmatched) ---
// #include <stdint.h>
// 
// void __stdcall16far FUN_24cb_007c(uint16_t *param_1) {
//     uint16_t bx;
//     uint16_t es;
// 
//     // Simulate the interrupt call
//     asm volatile (
//         "int $0x21"
//         : "=b" (bx), "=S" (es)
//         :
//         : "memory"
//     );
// 
//     *param_1 = bx;
//     *(param_1 + 1) = es;
//     return;
// }
// --- end reference ---
procedure FUN_24cb_007c(param_1: Pointer);
begin
  { TODO: translate from asm/FUN_24cb_007c.s — UNMATCHED until an oracle passes }
end;

