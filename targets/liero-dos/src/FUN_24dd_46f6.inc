{ liero-dos::FUN_24dd_46f6 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_46f6.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_46f6.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: recon:real decompiler C (unmatched) ---
// #include <stdint.h>
// 
// extern void FUN_24dd_4712(void);
// 
// void FUN_24dd_46f6(uint16_t in_AX, uint16_t in_DX, uint16_t *unaff_DI) {
//     uint32_t uVar1;
//     uint16_t bVar2;
//     char cVar3;
// 
//     if ((int16_t)in_DX < 0) {
//         FUN_24dd_4712();
//         *(unaff_DI - 1) = 0x2d;
//         return;
//     }
// 
//     do {
//         uVar1 = (uint32_t)in_DX;
//         in_DX = in_DX / 10;
//         uVar1 = (uVar1 % 10) << 0x10 | (uint32_t)in_AX;
//         in_AX = uVar1 / 10;
//         cVar3 = (char)(uVar1 % 10);
//         bVar2 = cVar3 + 0x30;
//         if (0x39 < bVar2) {
//             bVar2 = cVar3 + 0x37;
//         }
//         unaff_DI--;
//         *unaff_DI = bVar2;
//     } while (in_AX != 0 || in_DX != 0);
// }
// --- end reference ---
procedure FUN_24dd_46f6;
begin
  { TODO: translate from asm/FUN_24dd_46f6.s — UNMATCHED until an oracle passes }
end;

