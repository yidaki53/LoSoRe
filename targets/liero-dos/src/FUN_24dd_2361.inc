{ liero-dos::FUN_24dd_2361 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_2361.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_2361.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: recon:real decompiler C (unmatched) ---
// #include <stdint.h>
// 
// extern void swi(uint16_t);
// 
// uint16_t FUN_24dd_2361(uint16_t in_AX, uint16_t in_CX, uint16_t in_BX, uint16_t unaff_ES) {
//     uint16_t uVar5;
//     uint8_t bVar4;
//     uint8_t bVar2;
//     uint16_t uVar3;
//     uint16_t *ptr_d0 = (uint16_t *)0xd0;
//     uint16_t *ptr_d2 = (uint16_t *)0xd2;
//     uint8_t *ptr_d4 = (uint8_t *)0xd4;
//     uint8_t *ptr_d6 = (uint8_t *)0xd6;
// 
//     uVar5 = ((uint16_t)((uint8_t)(in_CX >> 8)) << 8) | *ptr_d6;
//     bVar4 = (uint8_t)uVar5 ^ 0x3f;
//     bVar2 = *ptr_d4 | (uint8_t)(uVar5 >> 8);
//     if (((bVar2 & bVar4 ^ bVar2) & 8) != 0) {
//         bVar2 = bVar2 | 0x20;
//     }
//     if ((bVar4 & bVar2) != 0) {
//         *ptr_d4 = bVar2 | 0x80;
//         if ((bVar2 & bVar4) == 0x20) {
//             return in_AX;
//         }
//         swi(0x21);
//         *ptr_d0 = in_BX;
//         *ptr_d2 = unaff_ES;
//         uVar3 = (*(uint16_t(*)())*ptr_d0)();
//         return uVar3;
//     }
//     *ptr_d4 = bVar2 & 0x7f;
//     return in_AX;
// }
// --- end reference ---
function FUN_24dd_2361: Word;
begin
  { TODO: translate from asm/FUN_24dd_2361.s — UNMATCHED until an oracle passes }
end;

