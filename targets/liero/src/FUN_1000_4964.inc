{ liero::FUN_1000_4964 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_4964.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_4964.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void FUN_1000_4964(int param_1)
// 
// {
//   uint *puVar1;
//   int *piVar2;
//   char *pcVar3;
//   undefined4 uVar4;
//   byte bVar5;
//   byte bVar6;
//   char cVar7;
//   uint uVar8;
//   uint uVar9;
//   uint uVar10;
//   uint uVar11;
//   uint uVar12;
//   uint uVar13;
//   uint uVar14;
//   int iVar15;
//   uint uVar16;
//   int iVar17;
//   int iVar18;
//   int iVar19;
//   uint *puVar20;
//   int iVar21;
//   undefined2 uVar22;
//   undefined2 uVar23;
//   undefined2 uVar24;
//   undefined2 unaff_DS;
//   bool bVar25;
//   bool bVar26;
//   undefined2 uVar27;
//   undefined2 uVar28;
//   undefined2 uVar29;
//   undefined2 uVar30;
//   undefined4 local_25;
//   byte local_21;
//   uint local_1f;
//   uint local_1d;
//   uint local_1b;
//   int local_19;
//   uint local_17;
//   int local_15;
//   uint local_8;
//   uint local_6;
//   int local_4;
//   
//   uVar24 = 0x24dd;
//   FUN_24dd_0530();
//   uVar22 = (undefined2)((ulong)*(undefined4 *)0x6688 >> 0x10);
//   puVar20 = (uint *)((int)*(undefined4 *)0x6688 + param_1 * 0x14);
//   local_25 = (uint *)CONCAT22(uVar22,puVar20);
//   local_21 = 0;
//   bVar5 = (byte)puVar20[8] & 0x7f;
//   do {
//     local_21 = local_21 + 1;
//     bVar26 = false;
//     uVar16 = puVar20[4];
//     uVar14 = puVar20[5];
//     uVar13 = *local_25;
//     *local_25 = *local_25 + uVar16;
//     puVar20[1] = puVar20[1] + uVar14 + (uint)CARRY2(uVar13,uVar16);
//     uVar16 = puVar20[6];
//     uVar14 = puVar20[7];
//     puVar1 = puVar20 + 2;
//     uVar13 = *puVar1;
//     *puVar1 = *puVar1 + uVar16;
//     puVar20[3] = puVar20[3] + uVar14 + (uint)CARRY2(uVar13,uVar16);
//     if (*(char *)(bVar5 + 0x11a5) == '\x02') {
//       local_15 = *(int *)((uint)*(byte *)((int)puVar20 + 0x11) * 8 + 0x15a0);
//       FUN_24dd_3d80();
//       local_17 = FUN_24dd_3dbd();
//       local_19 = *(int *)((uint)*(byte *)((int)puVar20 + 0x11) * 8 + 0x15a4);
//       FUN_24dd_3d80();
//       local_1b = FUN_24dd_3dbd();
//       bVar6 = (byte)puVar20[8] & 0x80;
//       if (bVar6 == 0x80) {
//         if ((*(char *)((int)*(undefined4 *)0x6670 + 0x9a) != '\0') &&
//            (*(char *)(*(byte *)0x6720 + 0x783b) != '\0')) {
//           iVar17 = *(int *)((uint)*(byte *)((int)puVar20 + 0x11) * 8 + 0x15a0);
//           FUN_24dd_3d80();
//           uVar13 = FUN_24dd_3dbd();
//           bVar25 = CARRY2(local_17,uVar13);
//           local_17 = local_17 + uVar13;
//           local_15 = local_15 + iVar17 + (uint)bVar25;
//           iVar17 = *(int *)((uint)*(byte *)((int)puVar20 + 0x11) * 8 + 0x15a4);
//           FUN_24dd_3d80();
//           uVar13 = FUN_24dd_3dbd();
//           bVar25 = CARRY2(local_1b,uVar13);
//           local_1b = local_1b + uVar13;
//           local_19 = local_19 + iVar17 + (uint)bVar25;
//         }
//       }
//       else if (((bVar6 == 0) && (*(char *)((int)*(undefined4 *)0x6670 + 0x144) != '\0')) &&
//               (*(char *)(*(byte *)0x6727 + 0x783b) != '\0')) {
//         iVar17 = *(int *)((uint)*(byte *)((int)puVar20 + 0x11) * 8 + 0x15a0);
//         FUN_24dd_3d80();
//         uVar13 = FUN_24dd_3dbd();
//         bVar25 = CARRY2(local_17,uVar13);
//         local_17 = local_17 + uVar13;
//         local_15 = local_15 + iVar17 + (uint)bVar25;
//         iVar17 = *(int *)((uint)*(byte *)((int)puVar20 + 0x11) * 8 + 0x15a4);
//         FUN_24dd_3d80();
//         uVar13 = FUN_24dd_3dbd();
//         bVar25 = CARRY2(local_1b,uVar13);
//         local_1b = local_1b + uVar13;
//         local_19 = local_19 + iVar17 + (uint)bVar25;
//       }
//       uVar13 = puVar20[5];
//       uVar16 = FUN_24dd_3e7c();
//       uVar16 = uVar13 + local_15 + (uint)CARRY2(uVar16,local_17);
//       uVar13 = FUN_24dd_3dbd();
//       puVar20[4] = uVar13;
//       puVar20[5] = uVar16;
//       uVar13 = puVar20[7];
//       uVar16 = FUN_24dd_3e7c();
//       uVar16 = uVar13 + local_19 + (uint)CARRY2(uVar16,local_1b);
//       uVar24 = 0x24dd;
//       uVar13 = FUN_24dd_3dbd();
//       puVar20[6] = uVar13;
//       puVar20[7] = uVar16;
//     }
//     else if (*(char *)(bVar5 + 0x11a5) == '\x03') {
//       iVar17 = *(int *)((uint)*(byte *)((int)puVar20 + 0x11) * 8 + 0x15a0);
//       FUN_24dd_3d80();
//       uVar8 = FUN_24dd_3dbd();
//       iVar18 = *(int *)((uint)*(byte *)((int)puVar20 + 0x11) * 8 + 0x15a4);
//       FUN_24dd_3d80();
//       uVar9 = FUN_24dd_3dbd();
//       uVar10 = FUN_24dd_4654(*(int *)((uint)bVar5 * 2 + 0xc7c) << 1);
//       uVar13 = *(uint *)((uint)bVar5 * 2 + 0xc7c);
//       uVar16 = puVar20[4];
//       uVar14 = puVar20[5];
//       uVar11 = uVar16 + uVar8;
//       uVar12 = uVar11 - uVar13;
//       puVar20[4] = uVar12 + uVar10;
//       puVar20[5] = (((uVar14 + iVar17 + (uint)CARRY2(uVar16,uVar8)) - ((int)uVar13 >> 0xf)) -
//                    (uint)(uVar11 < uVar13)) + (uint)CARRY2(uVar12,uVar10);
//       uVar24 = 0x24dd;
//       uVar8 = FUN_24dd_4654(*(int *)((uint)bVar5 * 2 + 0xc7c) << 1);
//       uVar13 = *(uint *)((uint)bVar5 * 2 + 0xc7c);
//       uVar16 = puVar20[6];
//       uVar14 = puVar20[7];
//       uVar10 = uVar16 + uVar9;
//       uVar11 = uVar10 - uVar13;
//       puVar20[6] = uVar11 + uVar8;
//       puVar20[7] = (((uVar14 + iVar18 + (uint)CARRY2(uVar16,uVar9)) - ((int)uVar13 >> 0xf)) -
//                    (uint)(uVar10 < uVar13)) + (uint)CARRY2(uVar11,uVar8);
//     }
//     if (*(char *)(bVar5 + 0xfed) != '\0') {
//       iVar17 = puVar20[1] + puVar20[5] + (uint)CARRY2(*local_25,puVar20[4]);
//       iVar18 = puVar20[3] + puVar20[7] + (uint)CARRY2(puVar20[2],puVar20[6]);
//       iVar19 = 0x20;
//       bVar6 = FUN_24dd_4161();
//       if ((((*(byte *)(iVar19 + 0x6604) & bVar6) != 0) || (iVar17 < 0)) || (0x1f7 < iVar17)) {
//         if (*(char *)(bVar5 + 0xfed) == 'd') {
//           uVar13 = puVar20[4];
//           uVar16 = puVar20[5];
//           puVar20[4] = -uVar13;
//           puVar20[5] = (~uVar16 + 1) - (uint)(uVar13 != 0);
//         }
//         else {
//           uVar13 = 0;
//           FUN_24dd_3d80();
//           iVar17 = FUN_24dd_3dbd();
//           puVar20[4] = -iVar17;
//           puVar20[5] = (~uVar13 + 1) - (uint)(iVar17 != 0);
//           uVar13 = puVar20[7];
//           FUN_24dd_3d80();
//           uVar16 = FUN_24dd_3dbd();
//           puVar20[6] = uVar16;
//           puVar20[7] = uVar13;
//         }
//       }
//       iVar17 = 0x20;
//       uVar24 = 0x24dd;
//       bVar6 = FUN_24dd_4161();
//       if ((((*(byte *)(iVar17 + 0x6604) & bVar6) != 0) || (0x15c < iVar18)) || (iVar18 < 0)) {
//         if (*(char *)(bVar5 + 0xfed) == 'd') {
//           uVar13 = puVar20[6];
//           uVar16 = puVar20[7];
//           puVar20[6] = -uVar13;
//           puVar20[7] = (~uVar16 + 1) - (uint)(uVar13 != 0);
//         }
//         else {
//           uVar13 = 0;
//           FUN_24dd_3d80();
//           iVar17 = FUN_24dd_3dbd();
//           puVar20[6] = -iVar17;
//           puVar20[7] = (~uVar13 + 1) - (uint)(iVar17 != 0);
//           uVar13 = puVar20[5];
//           FUN_24dd_3d80();
//           uVar16 = FUN_24dd_3dbd();
//           puVar20[4] = uVar16;
//           puVar20[5] = uVar13;
//         }
//         uVar24 = 0x24dd;
//       }
//     }
//     if (*(int *)((uint)bVar5 * 2 + 0xd1c) != 100) {
//       uVar16 = *(int *)((uint)bVar5 * 2 + 0xd1c) >> 0xf;
//       FUN_24dd_3d80();
//       uVar13 = FUN_24dd_3dbd();
//       puVar20[4] = uVar13;
//       puVar20[5] = uVar16;
//       uVar16 = *(int *)((uint)bVar5 * 2 + 0xd1c) >> 0xf;
//       FUN_24dd_3d80();
//       uVar24 = 0x24dd;
//       uVar13 = FUN_24dd_3dbd();
//       puVar20[6] = uVar13;
//       puVar20[7] = uVar16;
//     }
//     if ((*(char *)(bVar5 + 0x1295) != '\0') &&
//        (*(uint *)0x6520 % (uint)*(byte *)(bVar5 + 0x12bd) == 0)) {
//       FUN_202c_1b84(uVar24,puVar20[3],puVar20[1],(byte)puVar20[8] & 0x80 | *(byte *)(bVar5 + 0x1295)
//                    );
//     }
//     if ((*(char *)(bVar5 + 0x130d) != '\0') &&
//        (*(uint *)0x6520 % (uint)*(byte *)(bVar5 + 0x1335) == 0)) {
//       if (*(char *)(bVar5 + 0x12e5) == '\x01') {
//         uVar9 = (uint)((byte)puVar20[8] & 0x80 | *(byte *)(bVar5 + 0x130d));
//         uVar27 = 0;
//         uVar13 = puVar20[1];
//         uVar16 = puVar20[3];
//         uVar14 = puVar20[5];
//         uVar24 = FUN_24dd_3dbd(uVar16,uVar13,0,uVar9);
//         uVar8 = puVar20[7];
//         uVar23 = FUN_24dd_3dbd(uVar24,uVar14);
//         FUN_202c_14b6(uVar23,uVar8,uVar24,uVar14,uVar16,uVar13,uVar27,uVar9);
//       }
//       else {
//         uVar9 = (uint)((byte)puVar20[8] & 0x80 | *(byte *)(bVar5 + 0x130d));
//         uVar28 = 0;
//         uVar13 = puVar20[1];
//         uVar16 = puVar20[3];
//         uVar14 = puVar20[5];
//         uVar24 = FUN_24dd_3dbd(uVar16,uVar13,0,uVar9);
//         uVar8 = puVar20[7];
//         uVar23 = FUN_24dd_3dbd(uVar24,uVar14);
//         uVar27 = FUN_24dd_4654(0x80);
//         FUN_202c_165d(uVar27,uVar23,uVar8,uVar24,uVar14,uVar16,uVar13,uVar28,uVar9);
//       }
//     }
//     if (*(char *)(bVar5 + 0xf9d) == '\x01') {
//       local_4 = 0;
//       while( true ) {
//         if (((((*(char *)((int)*(undefined4 *)0x6688 + local_4 * 0x14 + 0x10) != '\0') &&
//               (*(char *)((int)*(undefined4 *)0x6688 + local_4 * 0x14 + 0x10) != (char)puVar20[8]))
//              && ((int)(puVar20[1] - 2) < *(int *)((int)*(undefined4 *)0x6688 + local_4 * 0x14 + 2)))
//             && ((*(int *)((int)*(undefined4 *)0x6688 + local_4 * 0x14 + 2) < (int)(puVar20[1] + 2)
//                 && ((int)(puVar20[3] - 2) <
//                     *(int *)((int)*(undefined4 *)0x6688 + local_4 * 0x14 + 6))))) &&
//            (*(int *)((int)*(undefined4 *)0x6688 + local_4 * 0x14 + 6) < (int)(puVar20[3] + 2))) {
//           iVar17 = 0;
//           FUN_24dd_3d80();
//           uVar16 = FUN_24dd_3dbd();
//           uVar24 = (undefined2)((ulong)*(undefined4 *)0x6688 >> 0x10);
//           iVar18 = (int)*(undefined4 *)0x6688 + local_4 * 0x14;
//           puVar1 = (uint *)(iVar18 + 8);
//           uVar13 = *puVar1;
//           *puVar1 = *puVar1 + uVar16;
//           piVar2 = (int *)(iVar18 + 10);
//           *piVar2 = *piVar2 + iVar17 + (uint)CARRY2(uVar13,uVar16);
//           iVar17 = 0;
//           FUN_24dd_3d80();
//           uVar16 = FUN_24dd_3dbd();
//           uVar24 = (undefined2)((ulong)*(undefined4 *)0x6688 >> 0x10);
//           iVar18 = (int)*(undefined4 *)0x6688 + local_4 * 0x14;
//           puVar1 = (uint *)(iVar18 + 0xc);
//           uVar13 = *puVar1;
//           *puVar1 = *puVar1 + uVar16;
//           piVar2 = (int *)(iVar18 + 0xe);
//           *piVar2 = *piVar2 + iVar17 + (uint)CARRY2(uVar13,uVar16);
//         }
//         if (local_4 == 600) break;
//         local_4 = local_4 + 1;
//       }
//       local_4 = 0;
//       while( true ) {
//         if (((*(char *)((int)*(undefined4 *)0x6694 + local_4 * 0x14 + 0x12) != '\0') &&
//             ((int)(puVar20[1] - 2) < *(int *)((int)*(undefined4 *)0x6694 + local_4 * 0x14 + 2))) &&
//            ((*(int *)((int)*(undefined4 *)0x6694 + local_4 * 0x14 + 2) < (int)(puVar20[1] + 2) &&
//             (((int)(puVar20[3] - 2) < *(int *)((int)*(undefined4 *)0x6694 + local_4 * 0x14 + 6) &&
//              (*(int *)((int)*(undefined4 *)0x6694 + local_4 * 0x14 + 6) < (int)(puVar20[3] + 2))))))
//            ) {
//           iVar17 = 0;
//           FUN_24dd_3d80();
//           uVar16 = FUN_24dd_3dbd();
//           uVar24 = (undefined2)((ulong)*(undefined4 *)0x6694 >> 0x10);
//           iVar18 = (int)*(undefined4 *)0x6694 + local_4 * 0x14;
//           puVar1 = (uint *)(iVar18 + 8);
//           uVar13 = *puVar1;
//           *puVar1 = *puVar1 + uVar16;
//           piVar2 = (int *)(iVar18 + 10);
//           *piVar2 = *piVar2 + iVar17 + (uint)CARRY2(uVar13,uVar16);
//           iVar17 = 0;
//           FUN_24dd_3d80();
//           uVar16 = FUN_24dd_3dbd();
//           uVar24 = (undefined2)((ulong)*(undefined4 *)0x6694 >> 0x10);
//           iVar18 = (int)*(undefined4 *)0x6694 + local_4 * 0x14;
//           puVar1 = (uint *)(iVar18 + 0xc);
//           uVar13 = *puVar1;
//           *puVar1 = *puVar1 + uVar16;
//           piVar2 = (int *)(iVar18 + 0xe);
//           *piVar2 = *piVar2 + iVar17 + (uint)CARRY2(uVar13,uVar16);
//         }
//         if (local_4 == 600) break;
//         local_4 = local_4 + 1;
//       }
//     }
//     iVar17 = puVar20[1] + puVar20[5] + (uint)CARRY2(*local_25,puVar20[4]);
//     iVar18 = puVar20[3] + puVar20[7] + (uint)CARRY2(puVar20[2],puVar20[6]);
//     if (iVar17 < 0) {
//       puVar20[1] = 0;
//     }
//     if (iVar18 < 0) {
//       puVar20[3] = 0;
//     }
//     if (0x1f7 < iVar17) {
//       puVar20[1] = 0x1f7;
//     }
//     if (0x15d < iVar18) {
//       puVar20[3] = 0x15d;
//     }
//     iVar19 = 0x20;
//     uVar24 = 0x24dd;
//     bVar6 = FUN_24dd_4161();
//     if (((((*(byte *)(iVar19 + 0x6604) & bVar6) == 0) && (-1 < iVar18)) && (iVar18 < 0x15d)) &&
//        ((-1 < iVar17 && (iVar17 < 0x1f8)))) {
//       if (*(int *)((uint)bVar5 * 2 + 0xac4) != 0) {
//         uVar16 = *(uint *)((uint)bVar5 * 2 + 0xac4);
//         puVar1 = puVar20 + 6;
//         uVar13 = *puVar1;
//         *puVar1 = *puVar1 + uVar16;
//         puVar20[7] = puVar20[7] + ((int)uVar16 >> 0xf) + (uint)CARRY2(uVar13,uVar16);
//       }
//       if ((*(char *)(bVar5 + 0x1155) != '\0') && ((*(uint *)0x6520 & 7) == 0)) {
//         if (*(char *)(bVar5 + 0x117d) == '\0') {
//           *(char *)((int)puVar20 + 0x11) = *(char *)((int)puVar20 + 0x11) + '\x01';
//           if (*(byte *)(bVar5 + 0x1155) < *(byte *)((int)puVar20 + 0x11)) {
//             *(undefined1 *)((int)puVar20 + 0x11) = 0;
//           }
//         }
//         else {
//           if (((int)puVar20[5] < 0) &&
//              (*(char *)((int)puVar20 + 0x11) = *(char *)((int)puVar20 + 0x11) + -1,
//              *(char *)((int)puVar20 + 0x11) == -1)) {
//             *(undefined1 *)((int)puVar20 + 0x11) = *(undefined1 *)(bVar5 + 0x1155);
//           }
//           if (((0 < (int)puVar20[5]) || ((-1 < (int)puVar20[5] && (puVar20[4] != 0)))) &&
//              (*(char *)((int)puVar20 + 0x11) = *(char *)((int)puVar20 + 0x11) + '\x01',
//              *(byte *)(bVar5 + 0x1155) < *(byte *)((int)puVar20 + 0x11))) {
//             *(undefined1 *)((int)puVar20 + 0x11) = 0;
//           }
//         }
//       }
//     }
//     else if (*(char *)(bVar5 + 0xfed) == '\0') {
//       if (*(char *)(bVar5 + 0xf25) == '\x01') {
//         bVar26 = true;
//       }
//       else {
//         puVar20[4] = 0;
//         puVar20[5] = 0;
//         puVar20[6] = 0;
//         puVar20[7] = 0;
//       }
//     }
//     if ((0 < *(int *)((uint)bVar5 * 2 + 0x1014)) &&
//        (puVar20[9] = puVar20[9] - 1, (int)puVar20[9] < 0)) {
//       bVar26 = true;
//     }
//     local_8 = 0;
//     while( true ) {
//       cVar7 = FUN_1000_0d70(puVar20[3],puVar20[1],*(undefined1 *)(bVar5 + 0xa25),local_8 & 0xff);
//       if (cVar7 != '\0') {
//         iVar17 = 0;
//         FUN_24dd_3d80();
//         uVar16 = FUN_24dd_3dbd();
//         uVar24 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
//         iVar18 = (int)*(undefined4 *)0x6670 + local_8 * 0xaa;
//         puVar1 = (uint *)(iVar18 + 0x30);
//         uVar13 = *puVar1;
//         *puVar1 = *puVar1 + uVar16;
//         piVar2 = (int *)(iVar18 + 0x32);
//         *piVar2 = *piVar2 + iVar17 + (uint)CARRY2(uVar13,uVar16);
//         iVar17 = 0;
//         FUN_24dd_3d80();
//         uVar24 = 0x24dd;
//         uVar16 = FUN_24dd_3dbd();
//         uVar23 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
//         iVar18 = (int)*(undefined4 *)0x6670 + local_8 * 0xaa;
//         puVar1 = (uint *)(iVar18 + 0x34);
//         uVar13 = *puVar1;
//         *puVar1 = *puVar1 + uVar16;
//         piVar2 = (int *)(iVar18 + 0x36);
//         *piVar2 = *piVar2 + iVar17 + (uint)CARRY2(uVar13,uVar16);
//         piVar2 = (int *)((int)*(undefined4 *)0x6670 + local_8 * 0xaa + 0x50);
//         *piVar2 = *piVar2 - (uint)*(byte *)(bVar5 + 0x10b5);
//         if (*(int *)((int)*(undefined4 *)0x6670 + local_8 * 0xaa + 0x50) < 1) {
//           if (local_8 == 0) {
//             if ((puVar20[8] & 0x80) == 0x80) {
//               *(undefined1 *)((int)*(undefined4 *)0x6670 + 0x96) = 0;
//             }
//             else {
//               *(undefined1 *)((int)*(undefined4 *)0x6670 + 0x96) = 1;
//             }
//           }
//           else if (local_8 == 1) {
//             if ((puVar20[8] & 0x80) == 0x80) {
//               *(undefined1 *)((int)*(undefined4 *)0x6670 + 0x140) = 1;
//             }
//             else {
//               *(undefined1 *)((int)*(undefined4 *)0x6670 + 0x140) = 0;
//             }
//           }
//         }
//         bVar6 = *(byte *)(bVar5 + 0x6453);
//         if (bVar6 != 0) {
//           local_6 = 1;
//           while( true ) {
//             uVar30 = 7;
//             uVar29 = 0;
//             uVar13 = puVar20[1];
//             uVar16 = puVar20[3];
//             uVar14 = puVar20[5];
//             uVar23 = FUN_24dd_3dbd(uVar16,uVar13,0,7);
//             uVar8 = puVar20[7];
//             uVar27 = FUN_24dd_3dbd(uVar23,uVar14);
//             uVar28 = FUN_24dd_4654(0x80);
//             uVar24 = 0x202c;
//             FUN_202c_165d(uVar28,uVar27,uVar8,uVar23,uVar14,uVar16,uVar13,uVar29,uVar30);
//             if (local_6 == bVar6) break;
//             local_6 = local_6 + 1;
//           }
//         }
//         if (((*(char *)0x4b8 != '\0') && (*(char *)(bVar5 + 0x10b5) != '\0')) &&
//            (0 < *(int *)((int)*(undefined4 *)0x6670 + local_8 * 0xaa + 0x50))) {
//           uVar24 = 0x24dd;
//           iVar17 = FUN_24dd_4654(3);
//           if (iVar17 == 0) {
//             uVar24 = 0x235c;
//             cVar7 = FUN_235c_0a1e(*(undefined1 *)(local_8 + 0x4b6));
//             if (cVar7 == '\0') {
//               iVar17 = FUN_24dd_4654(3);
//               iVar18 = (iVar17 + 0x13) * 4;
//               uVar24 = 0x235c;
//               FUN_235c_095c(0,CONCAT11((char)((uint)(iVar17 + 0x13) >> 8),
//                                        *(undefined1 *)(local_8 + 0x4b6)),
//                             *(undefined2 *)(iVar18 + 0x6734),*(undefined2 *)(iVar18 + 0x6736));
//             }
//           }
//         }
//         if (*(char *)(bVar5 + 0xf4d) != '\0') {
//           uVar24 = 0x24dd;
//           iVar17 = FUN_24dd_4654(*(undefined1 *)(bVar5 + 0xf4d));
//           if ((iVar17 == 0) && (bVar26 = *(char *)(bVar5 + 0xefd) == '\x01', !bVar26)) {
//             *(undefined1 *)(puVar20 + 8) = 0;
//             return;
//           }
//         }
//       }
//       if (local_8 == 1) break;
//       local_8 = local_8 + 1;
//     }
//     if (bVar26) {
//       if (*(char *)(bVar5 + 0xe35) != '\0') {
//         FUN_202c_1b84(uVar24,puVar20[3],puVar20[1],
//                       (byte)puVar20[8] & 0x80 | *(byte *)(bVar5 + 0xe35));
//         uVar24 = 0x202c;
//       }
//       if ((*(char *)0x4b8 != '\0') && (*(char *)(bVar5 + 0xbb5) != '\0')) {
//         iVar17 = (uint)*(byte *)(bVar5 + 0xbb5) * 4;
//         uVar24 = 0x235c;
//         FUN_235c_095c(0,*(undefined1 *)(bVar5 + 0xbb5),*(undefined2 *)(iVar17 + 0x6734),
//                       *(undefined2 *)(iVar17 + 0x6736));
//       }
//       if ((*(char *)(bVar5 + 0x11f5) != '\0') && (bVar6 = *(byte *)(bVar5 + 0x11f5), bVar6 != 0)) {
//         local_6 = 1;
//         while( true ) {
//           if (*(char *)(bVar5 + 0x126d) == '\0') {
//             uVar14 = (uint)((byte)puVar20[8] & 0x80 | *(byte *)(bVar5 + 0x1245));
//             iVar17 = FUN_24dd_4654(2);
//             iVar17 = (uint)*(byte *)(bVar5 + 0x121d) - iVar17;
//             uVar13 = puVar20[1];
//             uVar16 = puVar20[3];
//             uVar29 = 0;
//             uVar28 = 0;
//             uVar27 = 0;
//             uVar23 = 0;
//             uVar24 = FUN_24dd_4654(0x80);
//             FUN_202c_165d(uVar24,uVar23,uVar27,uVar28,uVar29,uVar16,uVar13,iVar17,uVar14);
//           }
//           else {
//             uVar13 = (uint)((byte)puVar20[8] & 0x80 | *(byte *)(bVar5 + 0x1245));
//             iVar17 = FUN_24dd_4654(2);
//             FUN_202c_14b6(puVar20[6],puVar20[7],puVar20[4],puVar20[5],puVar20[3],puVar20[1],
//                           (uint)*(byte *)(bVar5 + 0x121d) - iVar17,uVar13);
//           }
//           uVar24 = 0x202c;
//           if (local_6 == bVar6) break;
//           local_6 = local_6 + 1;
//         }
//       }
//       uVar13 = (uint)*(byte *)(bVar5 + 0xe5d);
//       if (uVar13 != 0) {
//         iVar17 = puVar20[1] - 7;
//         iVar18 = puVar20[3] - 7;
//         uVar23 = (undefined2)((ulong)*(undefined4 *)0x6678 >> 0x10);
//         iVar21 = (int)*(undefined4 *)0x6678 + (uint)*(byte *)(uVar13 + 0x1369) * 0x100;
//         iVar19 = FUN_24dd_4654(*(undefined1 *)(uVar13 + 0x137d));
//         iVar19 = (uint)*(byte *)(uVar13 + 0x1373) + iVar19;
//         iVar15 = iVar19 * 0x100;
//         if ((*(byte *)(uVar13 + 4999) & 1) == 1) {
//           iVar15 = iVar15 + 1;
//         }
//         uVar24 = 0x202c;
//         FUN_202c_005a(iVar15,(int)*(undefined4 *)0x6678 + iVar19 * 0x100,
//                       (int)((ulong)*(undefined4 *)0x6678 >> 0x10),iVar21,uVar23,iVar18,iVar17);
//         if (*(char *)0x66af != '\0') {
//           uVar13 = puVar20[1];
//           local_1d = puVar20[1] - 10;
//           if ((int)local_1d <= (int)(uVar13 + 10)) {
//             do {
//               if ((local_1d < 0x8000) && ((int)local_1d < 0x1f8)) {
//                 uVar16 = puVar20[3];
//                 local_1f = puVar20[3] - 10;
//                 if ((int)local_1f <= (int)(uVar16 + 10)) {
//                   do {
//                     if ((local_1f < 0x8000) && ((int)local_1f < 0x15e)) {
//                       iVar17 = 0x20;
//                       bVar6 = FUN_24dd_4161();
//                       if ((*(byte *)(iVar17 + 0x14e0) & bVar6) != 0) {
//                         iVar17 = 0x20;
//                         uVar24 = 0x24dd;
//                         bVar6 = FUN_24dd_4161();
//                         if ((*(byte *)(iVar17 + 0x6604) & bVar6) != 0) {
//                           uVar4 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_1f * 4);
//                           pcVar3 = (char *)((int)uVar4 + local_1d);
//                           *pcVar3 = *pcVar3 + '\x04';
//                           goto LAB_1000_5aaa;
//                         }
//                       }
//                       uVar24 = 0x24dd;
//                       uVar4 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_1f * 4);
//                       bVar6 = *(byte *)((int)uVar4 + local_1d);
//                       if ((0xa3 < bVar6) && (bVar6 < 0xa8)) {
//                         iVar17 = 0x20;
//                         uVar24 = 0x24dd;
//                         bVar6 = FUN_24dd_4161();
//                         if ((*(byte *)(iVar17 + 0x6604) & bVar6) != 0) {
//                           uVar4 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_1f * 4);
//                           pcVar3 = (char *)((int)uVar4 + local_1d);
//                           *pcVar3 = *pcVar3 + -4;
//                         }
//                       }
//                     }
// LAB_1000_5aaa:
//                     if (local_1f == uVar16 + 10) break;
//                     local_1f = local_1f + 1;
//                   } while( true );
//                 }
//               }
//               if (local_1d == uVar13 + 10) break;
//               local_1d = local_1d + 1;
//             } while( true );
//           }
//         }
//       }
//       *(undefined1 *)(puVar20 + 8) = 0;
//     }
//     if (((*(char *)(bVar5 + 0x11a5) != '\x04') || (bVar26)) || ((7 < local_21 && (bVar5 != 0x1d))))
//     {
//       return;
//     }
//   } while( true );
// }
// 
// --- end reference ---
procedure FUN_1000_4964;
begin
  { TODO: translate from asm/FUN_1000_4964.s — UNMATCHED until an oracle passes }
end;

