{ liero::FUN_24dd_3360 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_3360.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_3360.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_24dd_3360(undefined2 *param_1)
// 
// {
//   undefined2 *puVar1;
//   code *pcVar2;
//   undefined1 uVar3;
//   byte bVar4;
//   uint uVar5;
//   undefined1 extraout_AH;
//   uint uVar6;
//   uint in_CX;
//   int iVar7;
//   undefined2 extraout_DX;
//   uint extraout_DX_00;
//   uint extraout_DX_01;
//   int extraout_DX_02;
//   int extraout_DX_03;
//   uint *puVar8;
//   undefined1 *unaff_BP;
//   undefined1 *puVar9;
//   undefined1 *puVar10;
//   undefined2 *unaff_DI;
//   undefined2 *puVar11;
//   undefined2 unaff_ES;
//   undefined2 unaff_SS;
//   undefined2 unaff_DS;
//   bool bVar12;
//   bool bVar13;
//   char cVar14;
//   char cVar15;
//   byte bStack_2b;
//   uint local_2a [9];
//   byte abStack_17 [7];
//   int local_10;
//   uint local_e;
//   uint local_c;
//   uint local_a;
//   uint local_8;
//   uint local_6;
//   
//   do {
//     puVar9 = unaff_BP;
//     cVar15 = SBORROW2((int)&stack0xfffe,0x28);
//     cVar14 = (int)local_2a < 0;
//     bVar13 = &stack0x0000 == (undefined1 *)0x2a;
//     pcVar2 = (code *)swi(0x35);
//     (*pcVar2)();
//     do {
//     } while (bVar13 || cVar15 != cVar14);
//     pcVar2 = (code *)swi(0x3c);
//     (*pcVar2)();
//     in_CX = in_CX ^ (uint)&stack0xfffe;
//     unaff_BP = &stack0xfffe;
//   } while ((int)in_CX < 1);
//   if (0x12 < (int)in_CX) {
//     in_CX = 0x12;
//   }
//   if ((int)in_CX < -0x12) {
//     in_CX = 0xffee;
//   }
//   pcVar2 = (code *)swi(0x3d);
//   local_8 = in_CX;
//   (*pcVar2)();
//   local_c = local_e;
//   uVar5 = local_e & 0x7fff;
//   if (uVar5 == 0) {
//     local_2a[0] = local_2a[0] & 0xff00;
//     local_a = 0;
//   }
//   else {
//     if (uVar5 == 0x7fff) {
//       if (local_10 == -0x8000) {
//         if ((int)local_e < 0) {
//           puVar1 = unaff_DI;
//           unaff_DI = (undefined2 *)((int)unaff_DI + 1);
//           *(undefined1 *)puVar1 = 0x2d;
//         }
//         puVar11 = unaff_DI + 1;
//         *unaff_DI = 0x4e49;
//         unaff_DI = (undefined2 *)((int)unaff_DI + 3);
//         *(undefined1 *)puVar11 = 0x46;
//       }
//       else {
//         puVar11 = unaff_DI + 1;
//         *unaff_DI = 0x414e;
//         unaff_DI = (undefined2 *)((int)unaff_DI + 3);
//         *(undefined1 *)puVar11 = 0x4e;
//       }
//       goto LAB_24dd_34fc;
//     }
//     pcVar2 = (code *)swi(0x37);
//     local_e = uVar5;
//     (*pcVar2)();
//     puVar10 = puVar9 + 1;
//     out(*puVar9,extraout_DX);
//     uVar3 = in(extraout_DX);
//     local_a = (uint)((ulong)((long)(CONCAT11(extraout_AH,uVar3) + -0x3fff) * 0x4d10) >> 0x10);
//     FUN_24dd_35d4();
//     pcVar2 = (code *)swi(0x35);
//     (*pcVar2)();
//     pcVar2 = (code *)swi(0x3c);
//     bVar4 = (*pcVar2)();
//     cVar15 = '\0';
//     cVar14 = (char)(bVar4 ^ 0xd9) < '\0';
//     uVar3 = (bVar4 ^ 0xd9) == 0;
//     do {
//       pcVar2 = (code *)swi(0x39);
//       (*pcVar2)();
//     } while ((bool)uVar3 || cVar15 != cVar14);
//     pcVar2 = (code *)swi(0x3d);
//     (*pcVar2)();
//     do {
//       bVar13 = (local_6 & 0x4100) == 0;
//       if (!bVar13) {
//         pcVar2 = (code *)swi(0x3c);
//         (*pcVar2)();
//         func_0x0010bd56();
//         puVar10 = puVar10 + 1;
//         bVar13 = puVar10 == (undefined1 *)0x0;
//       }
//       bVar12 = false;
//       pcVar2 = (code *)swi(0x3b);
//       (*pcVar2)();
//     } while (bVar12 || bVar13);
//     puVar8 = local_2a;
//     bVar4 = 4;
//     iVar7 = 9;
//     pcVar2 = (code *)swi(0x3d);
//     (*pcVar2)();
//     do {
//       *puVar8 = (CONCAT11(abStack_17[iVar7],abStack_17[iVar7] >> (bVar4 & 0x1f)) & 0xfff) + 0x3030;
//       puVar8 = puVar8 + 1;
//       iVar7 = iVar7 + -1;
//     } while (iVar7 != 0);
//     *puVar8 = 0;
//     if ((-1 < (int)local_8) && (0x23 < (int)local_a)) {
//       local_8 = 0xffee;
//     }
//     if ((int)local_8 < 0) {
//       uVar5 = -local_8;
//     }
//     else {
//       uVar5 = local_8 + local_a + 1;
//       if ((int)uVar5 < 0) {
//         local_2a[0] = local_2a[0] & 0xff00;
//         goto LAB_24dd_3479;
//       }
//     }
//     if ((uVar5 < 0x12) &&
//        (bVar4 = *(byte *)((int)local_2a + uVar5), *(undefined1 *)((int)local_2a + uVar5) = 0,
//        0x34 < bVar4)) {
//       while (-1 < (int)(uVar5 - 1)) {
//         (&bStack_2b)[uVar5] = (&bStack_2b)[uVar5] + 1;
//         if ((&bStack_2b)[uVar5] < 0x3a) goto LAB_24dd_3479;
//         (&bStack_2b)[uVar5] = 0;
//         uVar5 = uVar5 - 1;
//       }
//       local_2a[0] = 0x31;
//       local_a = local_a + 1;
//     }
//   }
// LAB_24dd_3479:
//   if ((int)local_8 < 0) {
//     uVar3 = 0x20;
//     if ((int)local_c < 0) {
//       uVar3 = 0x2d;
//     }
//     *(undefined1 *)unaff_DI = uVar3;
//     uVar3 = FUN_24dd_350e();
//     *(undefined1 *)((int)unaff_DI + 1) = uVar3;
//     puVar11 = unaff_DI + 1;
//     if (extraout_DX_02 == -1) goto LAB_24dd_34d3;
//     puVar11 = (undefined2 *)((int)unaff_DI + 3);
//     *(undefined1 *)(unaff_DI + 1) = 0x2e;
//     do {
//       uVar3 = FUN_24dd_350e();
//       puVar1 = puVar11;
//       puVar11 = (undefined2 *)((int)puVar11 + 1);
//       *(undefined1 *)puVar1 = uVar3;
//       if (extraout_DX_03 == -1) goto LAB_24dd_34d3;
//     } while( true );
//   }
//   if ((int)local_c < 0) {
//     puVar1 = unaff_DI;
//     unaff_DI = (undefined2 *)((int)unaff_DI + 1);
//     *(undefined1 *)puVar1 = 0x2d;
//   }
//   uVar5 = local_a;
//   if ((int)local_a < 0) {
//     puVar1 = unaff_DI;
//     unaff_DI = (undefined2 *)((int)unaff_DI + 1);
//     *(undefined1 *)puVar1 = 0x30;
//     uVar6 = local_8;
//   }
//   else {
//     do {
//       uVar3 = FUN_24dd_350e();
//       puVar1 = unaff_DI;
//       unaff_DI = (undefined2 *)((int)unaff_DI + 1);
//       *(undefined1 *)puVar1 = uVar3;
//       uVar5 = uVar5 - 1;
//       uVar6 = extraout_DX_00;
//     } while (-1 < (int)uVar5);
//   }
//   if (uVar6 != 0) {
//     puVar1 = unaff_DI;
//     unaff_DI = (undefined2 *)((int)unaff_DI + 1);
//     *(undefined1 *)puVar1 = 0x2e;
//     do {
//       uVar5 = uVar5 + 1;
//       if (uVar5 == 0) break;
//       puVar1 = unaff_DI;
//       unaff_DI = (undefined2 *)((int)unaff_DI + 1);
//       *(undefined1 *)puVar1 = 0x30;
//       uVar6 = uVar6 - 1;
//     } while (uVar6 != 0);
//     while (-1 < (int)(uVar6 - 1)) {
//       uVar3 = FUN_24dd_350e();
//       puVar1 = unaff_DI;
//       unaff_DI = (undefined2 *)((int)unaff_DI + 1);
//       *(undefined1 *)puVar1 = uVar3;
//       uVar6 = extraout_DX_01;
//     }
//   }
// LAB_24dd_34fc:
//   while( true ) {
//     iVar7 = (int)unaff_DI - (int)param_1;
//     pcVar2 = (code *)swi(0x37);
//     (*pcVar2)();
//     puVar11 = param_1;
//     if (iVar7 == 1) break;
// LAB_24dd_34d3:
//     *(undefined1 *)puVar11 = 0x45;
//     uVar3 = 0x2b;
//     uVar5 = local_a;
//     if ((int)local_a < 0) {
//       uVar3 = 0x2d;
//       uVar5 = -local_a;
//     }
//     *(undefined1 *)((int)puVar11 + 1) = uVar3;
//     uVar6 = (uint)(char)(uVar5 / 100);
//     puVar11[1] = CONCAT11((char)(uVar6 % 10),(char)(uVar6 / 10)) + 0x3030;
//     uVar5 = (uint)(char)(uVar5 % 100);
//     unaff_DI = puVar11 + 3;
//     puVar11[2] = CONCAT11((char)(uVar5 % 10),(char)(uVar5 / 10)) + 0x3030;
//   }
//   pcVar2 = (code *)swi(0x3d);
//   (*pcVar2)();
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_3360;
begin
  { TODO: translate from asm/FUN_24dd_3360.s — UNMATCHED until an oracle passes }
end;

