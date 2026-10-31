{ liero-dos::FUN_24dd_3d36 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_3d36.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_3d36.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: recon:real decompiler C (unmatched) ---
// #include <stdint.h>
// 
// void FUN_24dd_3d36(void) {
//     uint16_t uVar1;
//     uint8_t *pbVar2;
//     uint8_t *pbVar3;
//     uint32_t uVar4;
//     int in_DX;
// 
//     uVar1 = *(uint16_t *)0x640c;
//     uVar4 = (uint32_t)*(uint8_t *)0x80;
//     pbVar2 = (uint8_t *)0x81;
//     do {
//         for (; (pbVar3 = pbVar2, uVar4 != 0 && (*pbVar2 < 0x21)); pbVar2 = pbVar2 + 1) {
//             uVar4 = uVar4 - 1;
//         }
//         for (; (uVar4 != 0 && (0x20 < *pbVar3)); pbVar3 = pbVar3 + 1) {
//             uVar4 = uVar4 - 1;
//         }
//     } while ((pbVar3 != pbVar2) && (in_DX = in_DX + -1, pbVar2 = pbVar3, in_DX != 0));
// }
// --- end reference ---
procedure FUN_24dd_3d36;
begin
  { TODO: translate from asm/FUN_24dd_3d36.s — UNMATCHED until an oracle passes }
end;

