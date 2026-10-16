{ liero::FUN_24dd_0ee2 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_0ee2.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_0ee2.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void FUN_24dd_0ee2(uint *param_1,uint *param_2,uint *param_3)
// 
// {
//   ulong uVar1;
//   byte bVar2;
//   byte bVar3;
//   uint uVar4;
//   uint uVar5;
//   byte bVar6;
//   uint uVar7;
//   uint uVar8;
//   uint uVar9;
//   uint uVar10;
//   uint uVar11;
//   uint uVar12;
//   uint uVar13;
//   uint uVar14;
//   uint *puVar15;
//   int iVar16;
//   undefined2 unaff_ES;
//   undefined2 unaff_DS;
//   bool bVar18;
//   byte local_7;
//   uint local_6;
//   char local_4;
//   int iVar17;
//   
//   bVar2 = (byte)param_2[5] ^ (byte)param_3[5];
//   uVar5 = param_3[4];
//   uVar14 = param_2[4];
//   bVar18 = uVar5 < 0x4001;
//   puVar15 = param_3;
//   if ((int)uVar5 < 0x4001) {
//     if (0x4000 < (int)uVar14) {
//       bVar18 = false;
//       local_7 = FUN_24dd_0e57();
//       puVar15 = param_2;
//       if (bVar18) {
//         return;
//       }
//       goto LAB_24dd_0f75;
//     }
//     if ((int)uVar5 < (int)uVar14) {
//       bVar6 = (byte)param_2[5];
//       uVar8 = uVar14;
//       uVar14 = uVar5;
//       puVar15 = param_2;
//     }
//     else {
//       bVar6 = (byte)param_3[5];
//       uVar8 = uVar5;
//       param_3 = param_2;
//     }
//     local_6 = puVar15[4];
//     local_7 = bVar6;
//     if ((-0x3fff < (int)uVar14) && ((int)(uVar8 - uVar14) < 0x41)) {
//       bVar3 = (byte)(uVar8 - uVar14);
//       uVar14 = *param_3;
//       uVar8 = param_3[1];
//       uVar12 = param_3[2];
//       uVar9 = param_3[3];
//       local_4 = '\0';
//       while (bVar18 = '\a' < (char)bVar3, bVar3 = bVar3 - 8, bVar18) {
//         local_4 = (char)uVar14;
//         uVar14 = CONCAT11((char)uVar8,(char)(uVar14 >> 8));
//         uVar8 = CONCAT11((char)uVar12,(char)(uVar8 >> 8));
//         uVar12 = CONCAT11((char)uVar9,(char)(uVar12 >> 8));
//         uVar9 = uVar9 >> 8;
//       }
//       for (bVar3 = bVar3 & 7; bVar3 != 0; bVar3 = bVar3 - 1) {
//         uVar5 = uVar9 & 1;
//         uVar9 = uVar9 >> 1;
//         uVar4 = uVar12 & 1;
//         local_4 = (char)(CONCAT11((uVar14 & 1) != 0,local_4) >> 1);
//         uVar14 = (uint)(CONCAT12((uVar8 & 1) != 0,uVar14) >> 1);
//         uVar12 = (uint)(CONCAT12(uVar5 != 0,uVar12) >> 1);
//         uVar8 = (uint)(CONCAT12(uVar4 != 0,uVar8) >> 1);
//       }
//       if (bVar2 == 0) {
//         uVar4 = uVar14 + *puVar15;
//         uVar5 = (uint)CARRY2(uVar14,*puVar15);
//         uVar14 = uVar8 + puVar15[1];
//         uVar13 = uVar14 + uVar5;
//         uVar5 = (uint)(CARRY2(uVar8,puVar15[1]) || CARRY2(uVar14,uVar5));
//         uVar14 = uVar12 + puVar15[2];
//         uVar7 = uVar14 + uVar5;
//         uVar12 = (uint)(CARRY2(uVar12,puVar15[2]) || CARRY2(uVar14,uVar5));
//         bVar18 = CARRY2(uVar9,puVar15[3]);
//         uVar9 = uVar9 + puVar15[3];
//         uVar10 = uVar9 + uVar12;
//         uVar5 = uVar4;
//         uVar8 = uVar7;
//         uVar11 = uVar10;
//         uVar14 = uVar13;
//         if (bVar18 || CARRY2(uVar9,uVar12)) {
//           uVar11 = (uint)(CONCAT12(bVar18 || CARRY2(uVar9,uVar12),uVar10) >> 1);
//           uVar8 = (uint)(CONCAT12((uVar10 & 1) != 0,uVar7) >> 1);
//           uVar14 = (uint)(CONCAT12((uVar7 & 1) != 0,uVar13) >> 1);
//           uVar5 = (uint)(CONCAT12((uVar13 & 1) != 0,uVar4) >> 1);
//           local_4 = (char)(CONCAT11((uVar4 & 1) != 0,local_4) >> 1);
//           local_6 = local_6 + 1;
//         }
//       }
//       else {
//         uVar5 = uVar14 - *puVar15;
//         uVar4 = (uint)(uVar14 < *puVar15);
//         uVar11 = uVar8 - puVar15[1];
//         uVar14 = uVar11 - uVar4;
//         uVar4 = (uint)(uVar8 < puVar15[1] || uVar11 < uVar4);
//         uVar11 = uVar12 - puVar15[2];
//         uVar8 = uVar11 - uVar4;
//         uVar12 = (uint)(uVar12 < puVar15[2] || uVar11 < uVar4);
//         uVar4 = uVar9 - puVar15[3];
//         uVar11 = uVar4 - uVar12;
//         local_7 = bVar6 ^ 1;
//         if (uVar9 < puVar15[3] || uVar4 < uVar12) {
//           uVar9 = ~uVar8;
//           uVar12 = ~uVar14;
//           uVar14 = ~uVar5;
//           bVar18 = local_4 == '\0';
//           local_4 = -local_4;
//           uVar5 = uVar14 + bVar18;
//           uVar8 = (uint)CARRY2(uVar14,(uint)bVar18);
//           uVar14 = uVar12 + uVar8;
//           uVar12 = (uint)CARRY2(uVar12,uVar8);
//           uVar8 = uVar9 + uVar12;
//           uVar11 = ~uVar11 + (uint)CARRY2(uVar9,uVar12);
//           local_7 = bVar6;
//         }
//         iVar16 = 0x40;
//         if (-1 < (int)uVar11) {
//           do {
//             iVar17 = iVar16;
//             iVar16 = iVar17 + -1;
//             if ((iVar16 == 0) && (uVar11 == 0)) {
//               local_6 = 0xc001;
//               local_7 = 0;
//               uVar12 = 0;
//               goto LAB_24dd_106b;
//             }
//             bVar18 = local_4 < '\0';
//             local_4 = local_4 << 1;
//             uVar1 = (ulong)CONCAT12(bVar18,uVar5) << 1;
//             uVar5 = (uint)uVar1 | (uint)bVar18;
//             bVar18 = (uVar1 & 0x10000) != 0;
//             uVar1 = (ulong)CONCAT12(bVar18,uVar14) << 1;
//             uVar14 = (uint)uVar1 | (uint)bVar18;
//             bVar18 = (uVar1 & 0x10000) != 0;
//             uVar1 = (ulong)CONCAT12(bVar18,uVar8) << 1;
//             uVar8 = (uint)uVar1 | (uint)bVar18;
//             uVar11 = uVar11 * 2 + (uint)((uVar1 & 0x10000) != 0);
//           } while (-1 < (int)uVar11);
//           local_6 = local_6 + iVar17 + -0x41;
//         }
//       }
//       bVar18 = CARRY2(uVar5,(uint)(local_4 < '\0'));
//       uVar5 = uVar5 + (local_4 < '\0');
//       uVar12 = (uint)bVar18;
//       bVar18 = CARRY2(uVar14,uVar12);
//       uVar14 = uVar14 + uVar12;
//       uVar12 = (uint)bVar18;
//       bVar18 = CARRY2(uVar8,uVar12);
//       uVar8 = uVar8 + uVar12;
//       uVar9 = (uint)bVar18;
//       uVar12 = uVar11 + uVar9;
//       if (CARRY2(uVar11,uVar9)) {
//         uVar12 = (uint)(CONCAT12(1,uVar12) >> 1);
//         local_6 = local_6 + 1;
//       }
//       if ((int)local_6 < 0x4001) {
//         if (-0x3fff < (int)local_6) goto LAB_24dd_106b;
//         local_6 = 0xc001;
//       }
//       else {
//         local_6 = 0x4001;
//       }
//       FUN_24dd_2361();
//       local_7 = 0;
//       uVar5 = 0;
//       uVar14 = 0;
//       uVar8 = 0;
//       uVar12 = 0;
//       goto LAB_24dd_106b;
//     }
//   }
//   else {
//     FUN_24dd_0e57(param_2);
//     if (bVar18) {
//       return;
//     }
//     if ((0x4000 < (int)uVar14) && (bVar2 != 0)) {
//       FUN_24dd_060f();
//       return;
//     }
//     local_7 = (byte)param_3[5];
// LAB_24dd_0f75:
//     local_6 = 0x4001;
//   }
//   uVar5 = *puVar15;
//   uVar14 = puVar15[1];
//   uVar8 = puVar15[2];
//   uVar12 = puVar15[3];
// LAB_24dd_106b:
//   *param_1 = uVar5;
//   param_1[1] = uVar14;
//   param_1[2] = uVar8;
//   param_1[3] = uVar12;
//   param_1[4] = local_6;
//   *(byte *)(param_1 + 5) = local_7;
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_0ee2;
begin
  { TODO: translate from asm/FUN_24dd_0ee2.s — UNMATCHED until an oracle passes }
end;

