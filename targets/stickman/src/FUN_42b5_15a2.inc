{ stickman::FUN_42b5_15a2 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_42b5_15a2.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_42b5_15a2.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_42b5_15a2(void)
// 
// {
//   byte bVar1;
//   int iVar2;
//   int in_CX;
//   char cVar3;
//   int in_BX;
//   byte *unaff_DI;
//   undefined2 unaff_ES;
//   bool bVar4;
//   undefined4 uVar5;
//   undefined2 uVar6;
//   undefined2 uVar7;
//   undefined2 uVar8;
//   
//   uVar6 = 0;
//   uVar7 = 0;
//   uVar8 = 0;
//   if (in_CX != 0) {
//     bVar1 = *unaff_DI;
//     bVar4 = bVar1 < 0x20;
//     if (((bVar1 == 0x20) || (bVar4 = bVar1 < 0x2b, bVar1 == 0x2b)) ||
//        (bVar4 = bVar1 < 0x2d, bVar1 == 0x2d)) {
//       unaff_DI = unaff_DI + 1;
//       in_CX = in_CX + -1;
//     }
//     FUN_42b5_164e(0,0,0);
//     if (!bVar4) {
//       if ((in_BX == 0) || ((cVar3 = '\0', in_CX != 0 && (*unaff_DI == 0x2e)))) {
//         cVar3 = '\0';
//         if (in_CX == 0) {
//           return;
//         }
//         bVar4 = *unaff_DI < 0x2e;
//         if (*unaff_DI != 0x2e) {
//           return;
//         }
//         unaff_DI = unaff_DI + 1;
//         in_CX = in_CX + -1;
//         FUN_42b5_164e(uVar6,uVar7,uVar8);
//         if (bVar4) {
//           return;
//         }
//         cVar3 = -cVar3;
//       }
//       if (in_CX != 0) {
//         bVar1 = *unaff_DI;
//         bVar4 = bVar1 < 0x45;
//         if ((bVar1 == 0x45) || (bVar4 = bVar1 < 0x65, bVar1 == 0x65)) {
//           unaff_DI = unaff_DI + 1;
//           in_CX = in_CX + -1;
//           uVar5 = FUN_42b5_1387();
//           iVar2 = (int)uVar5;
//           if (bVar4) {
//             return;
//           }
//           cVar3 = cVar3 + (char)uVar5;
//           if ((int)((ulong)uVar5 >> 0x10) != iVar2 >> 0xf) {
//             return;
//           }
//           if (0x3f < iVar2) {
//             return;
//           }
//           if (iVar2 < -0x3f) {
//             return;
//           }
//         }
//       }
//       if (cVar3 < -0x24) {
//         FUN_42b5_168c(cVar3,unaff_DI,in_CX);
//       }
//       FUN_42b5_168c();
//     }
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_42b5_15a2;
begin
  { TODO: translate from asm/FUN_42b5_15a2.s — UNMATCHED until an oracle passes }
end;

