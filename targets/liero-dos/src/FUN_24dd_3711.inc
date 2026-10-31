{ liero-dos::FUN_24dd_3711 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_3711.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_3711.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: recon:real decompiler C (unmatched) ---
// #include <stdint.h>
// 
// extern void FUN_24dd_374d(void);
// 
// void FUN_24dd_3711(uint32_t param_1) {
//     int iVar1;
//     uint16_t uVar2;
//     uint16_t *ptr;
// 
//     uVar2 = (uint16_t)(param_1 >> 16);
//     iVar1 = (int)param_1;
//     ptr = (uint16_t *)(iVar1 + 2);
// 
//     if (*ptr != (int16_t)-0x284f) {
//         if (*ptr != (int16_t)-0x284e) {
//             *(uint16_t *)0x6410 = 0x67;
//             return;
//         }
//         FUN_24dd_374d();
//     }
//     FUN_24dd_374d();
//     *ptr = 0xd7b0;
// }
// --- end reference ---
procedure FUN_24dd_3711(param_1: Longint);
begin
  { TODO: translate from asm/FUN_24dd_3711.s — UNMATCHED until an oracle passes }
end;

