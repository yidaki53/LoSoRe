{ liero::FUN_24cb_00a7 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24cb_00a7.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24cb_00a7.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_24cb_00a7(byte *param_1,byte *param_2)
// 
// {
//   undefined2 uVar1;
//   byte *pbVar2;
//   byte *pbVar3;
//   byte bVar4;
//   int iVar5;
//   int iVar6;
//   byte *pbVar7;
//   byte *pbVar8;
//   undefined2 unaff_SS;
//   undefined2 unaff_DS;
//   bool bVar9;
//   byte local_22 [32];
//   
//   pbVar7 = (byte *)param_1;
//   pbVar8 = local_22;
//   bVar4 = *param_1;
//   if (0x1f < bVar4) {
//     bVar4 = 0x1f;
//   }
//   iVar5 = (int)(char)bVar4;
//   iVar6 = iVar5 + 1;
//   for (; iVar5 != 0; iVar5 = iVar5 + -1) {
//     pbVar7 = pbVar7 + 1;
//     bVar4 = *pbVar7;
//     if ((0x60 < bVar4) && (bVar4 < 0x7b)) {
//       bVar4 = bVar4 - 0x20;
//     }
//     pbVar2 = pbVar8;
//     pbVar8 = pbVar8 + 1;
//     *pbVar2 = bVar4;
//   }
//   *pbVar8 = 0x3d;
//   uVar1 = *(undefined2 *)0x2c;
//   pbVar8 = (byte *)0x0;
//   while (bVar9 = *pbVar8 == 0, !bVar9) {
//     pbVar7 = local_22;
//     iVar5 = iVar6;
//     do {
//       if (iVar5 == 0) break;
//       iVar5 = iVar5 + -1;
//       pbVar3 = pbVar7;
//       pbVar7 = pbVar7 + 1;
//       pbVar2 = pbVar8;
//       pbVar8 = pbVar8 + 1;
//       bVar9 = *pbVar2 == *pbVar3;
//     } while (bVar9);
//     if (bVar9) break;
//     pbVar8 = pbVar8 + -1;
//     do {
//       pbVar2 = pbVar8;
//       pbVar8 = pbVar8 + 1;
//     } while (*pbVar2 != 0);
//   }
//   iVar5 = 0x100;
//   pbVar7 = pbVar8;
//   do {
//     if (iVar5 == 0) break;
//     iVar5 = iVar5 + -1;
//     pbVar2 = pbVar7;
//     pbVar7 = pbVar7 + 1;
//   } while (*pbVar2 != 0);
//   pbVar7 = (byte *)param_2;
//   *param_2 = ~(byte)iVar5;
//   for (iVar5 = CONCAT11((char)((uint)iVar5 >> 8),~(byte)iVar5); pbVar7 = pbVar7 + 1, iVar5 != 0;
//       iVar5 = iVar5 + -1) {
//     pbVar2 = pbVar8;
//     pbVar8 = pbVar8 + 1;
//     *pbVar7 = *pbVar2;
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_24cb_00a7;
begin
  { TODO: translate from asm/FUN_24cb_00a7.s — UNMATCHED until an oracle passes }
end;

