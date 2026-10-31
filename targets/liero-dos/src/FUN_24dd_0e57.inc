{ liero-dos::FUN_24dd_0e57 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_0e57.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_0e57.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: recon:real decompiler C (unmatched) ---
// #include <stdint.h>
// 
// extern void FUN_24dd_2361(void);
// 
// void FUN_24dd_0e57(uint16_t *unaff_SI, uint16_t *in_BX, uint16_t *unaff_DI) {
//     if ((((unaff_SI[3] & 0x7fff) == 0 && unaff_SI[0] == 0) && unaff_SI[1] == 0) && unaff_SI[2] == 0) {
//         if (in_BX == (uint16_t *)0xffff) {
//             return;
//         }
//         if ((int16_t)in_BX[4] < 0x4001) {
//             return;
//         }
//         if ((((in_BX[3] & 0x7fff) == 0 && in_BX[0] == 0) && in_BX[1] == 0) && in_BX[2] == 0) {
//             return;
//         }
//     } else if (((((in_BX == (uint16_t *)0xffff) || ((int16_t)in_BX[4] < 0x4001)) ||
//                 ((((in_BX[3] & 0x7fff) == 0 && in_BX[0] == 0) && in_BX[1] == 0) && in_BX[2] == 0)) ||
//                (in_BX[3] < unaff_SI[3])) ||
//               ((in_BX[3] <= unaff_SI[3] &&
//                ((in_BX[2] < unaff_SI[2] ||
//                 ((in_BX[2] <= unaff_SI[2] &&
//                  ((in_BX[1] < unaff_SI[1] || ((in_BX[1] <= unaff_SI[1] && (in_BX[0] < unaff_SI[0])))))))))
//                ))) {
//         goto LAB_24dd_0ece;
//     }
//     unaff_SI = in_BX;
// LAB_24dd_0ece:
//     FUN_24dd_2361();
//     for (int iVar3 = 6; iVar3 != 0; iVar3--) {
//         *unaff_DI = *unaff_SI;
//         unaff_DI++;
//         unaff_SI++;
//     }
// }
// --- end reference ---
procedure FUN_24dd_0e57;
begin
  { TODO: translate from asm/FUN_24dd_0e57.s — UNMATCHED until an oracle passes }
end;

