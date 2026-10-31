{ liero-dos::FUN_24dd_041e — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_041e.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_041e.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: recon:contested decompiler C (unmatched) ---
// #include <stdint.h>
// 
// void FUN_24dd_041e(uint16_t in_AX, void *in_CX, uint16_t in_BX) {
//     uint32_t *puVar1;
//     uint32_t *puVar2;
//     uint32_t *puVar3;
//     uint16_t uVar4;
//     uint32_t uVar5;
// 
//     if ((((in_AX != 0) && (((uint32_t)in_CX & 0xfff7) == 0)) &&
//         ((*(uint32_t *)0x63ec < in_BX ||
//          ((*(uint32_t *)0x63ec <= in_BX && ((uint32_t *)*(uint32_t *)0x63ea <= in_CX)))))) &&
//        ((in_BX < *(uint32_t *)0x63f0 ||
//         ((in_BX <= *(uint32_t *)0x63f0 && (in_CX < (uint32_t *)*(uint32_t *)0x63ee)))))) {
//         uVar5 = FUN_24dd_04dc();
//         *(int *)(in_CX + 1) = (int)uVar5;
//         *(uint16_t *)((int)in_CX + 6) = (uint16_t)((uVar5 >> 0x10) & 0xFFFF);
//         puVar3 = (uint32_t *)0x63f6;
//         do {
//             do {
//                 uVar4 = *(uint16_t *)puVar3;
//                 puVar2 = puVar3;
//                 puVar1 = (uint32_t *)*(uint32_t *)puVar2;
//                 puVar3 = (uint32_t *)puVar1;
//             } while (uVar4 < in_BX);
//             if (in_BX < uVar4) goto LAB_24dd_046f;
//         } while (puVar3 < in_CX);
//         if (in_CX != puVar3) {
// LAB_24dd_046f:
//             FUN_24dd_047d(puVar2, uVar4);
//             FUN_24dd_047d();
//             return;
//         }
//     }
//     return;
// }
// --- end reference ---
procedure FUN_24dd_041e;
begin
  { TODO: translate from asm/FUN_24dd_041e.s — UNMATCHED until an oracle passes }
end;

