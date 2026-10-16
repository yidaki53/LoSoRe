{ liero::FUN_1000_10ec — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_10ec.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_10ec.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// /* WARNING: Control flow encountered bad instruction data */
// 
// void FUN_1000_10ec(void)
// 
// {
//   uint *puVar1;
//   int *piVar2;
//   char *pcVar3;
//   code *pcVar4;
//   undefined4 uVar5;
//   byte bVar6;
//   char cVar7;
//   byte bVar8;
//   undefined1 uVar9;
//   uint uVar10;
//   undefined2 uVar11;
//   int iVar12;
//   int iVar13;
//   int iVar14;
//   uint uVar15;
//   int iVar16;
//   uint uVar17;
//   uint uVar18;
//   uint uVar19;
//   undefined2 extraout_DX;
//   undefined2 extraout_DX_00;
//   int *piVar20;
//   int iVar21;
//   int iVar22;
//   undefined2 uVar23;
//   undefined2 uVar24;
//   undefined2 unaff_DS;
//   bool bVar25;
//   int iVar26;
//   int iVar27;
//   int iVar28;
//   int iVar29;
//   undefined2 uVar30;
//   undefined2 uVar31;
//   undefined2 uVar32;
//   undefined2 uVar33;
//   uint uStack_30;
//   undefined4 local_2e;
//   uint local_24;
//   int local_22;
//   uint local_20;
//   int local_1e;
//   uint local_1c;
//   int local_1a;
//   uint local_18;
//   int local_16;
//   int local_12;
//   uint local_10;
//   uint local_e;
//   uint local_c;
//   int local_a;
//   uint local_8;
//   int local_6;
//   uint local_4;
//   
//   FUN_24dd_0530();
//   local_4 = 0;
// LAB_1000_1104:
//   uVar23 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
//   piVar20 = (int *)((int)*(undefined4 *)0x6670 + local_4 * 0xaa);
//   local_2e = (int *)CONCAT22(uVar23,piVar20);
//   uVar15 = piVar20[0x28];
//   bVar25 = -1 < (int)uVar15 >> 0xf;
//   if (((int)uVar15 < 0 && bVar25) || ((bVar25 && (*(uint *)(local_4 * 2 + 0x66e8) < uVar15)))) {
//     piVar20[0x28] = *(int *)(local_4 * 2 + 0x66e8);
//   }
//   uVar24 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
//   iVar21 = (int)*(undefined4 *)0x6670 + local_4 * 0xaa;
//   iVar16 = *(int *)(iVar21 + 0x3a);
//   if ((0 < iVar16) ||
//      (((-1 < iVar16 && (*(int *)(iVar21 + 0x38) != 0)) || (*(char *)0x66ac != '\0')))) {
//     if ((char)piVar20[0x4d] == '\0') {
//       if (*(char *)(*(byte *)(local_4 * 7 + 0x6724) + 0x783b) != '\0') {
//         *(undefined1 *)((int)piVar20 + 0x9f) = 1;
//         *(undefined1 *)(*(byte *)(local_4 * 7 + 0x6724) + 0x783b) = 0;
//       }
//       if (0 < piVar20[0x26]) {
//         piVar20[0x26] = piVar20[0x26] + -1;
//       }
//       if (piVar20[0x26] == 0) {
//         iVar16 = piVar20[3];
//         iVar21 = piVar20[5];
//         do {
//           iVar13 = FUN_24dd_4654(0x1ee);
//           piVar20[3] = iVar13 + 5;
//           iVar13 = FUN_24dd_4654(0x154);
//           piVar20[5] = iVar13 + 5;
//           while( true ) {
//             iVar13 = 0x20;
//             bVar8 = FUN_24dd_4161();
//             if ((*(byte *)(iVar13 + 0x14c0) & bVar8) == 0) break;
//             piVar20[5] = piVar20[5] + 1;
//           }
//           cVar7 = FUN_1000_0c7f(*(undefined2 *)
//                                  ((int)*(undefined4 *)0x6670 + (local_4 ^ 1) * 0xaa + 10),
//                                 *(undefined2 *)
//                                  ((int)*(undefined4 *)0x6670 + (local_4 ^ 1) * 0xaa + 6),iVar21,
//                                 iVar16,piVar20[5],piVar20[3]);
//         } while (cVar7 == '\0');
//         piVar20[0x26] = piVar20[0x26] + -1;
//       }
//       if (piVar20[0x26] < 0) {
//         local_a = piVar20[3] + -0x50;
//         if (local_a < 0) {
//           local_a = 0;
//         }
//         if (0x15a < local_a) {
//           local_a = 0x15a;
//         }
//         local_c = piVar20[5] + -0x50;
//         if ((int)local_c < 0) {
//           local_c = 0;
//         }
//         if (0xc0 < (int)local_c) {
//           local_c = 0xc0;
//         }
//         if (((local_a + -5 < *(int *)(local_4 * 2 + 0x67b0)) &&
//             (*(int *)(local_4 * 2 + 0x67b0) < local_a + 5)) &&
//            (((int)(local_c + -5) < *(int *)(local_4 * 2 + 0x67b4) &&
//             ((*(int *)(local_4 * 2 + 0x67b4) < (int)(local_c + 5) &&
//              (*(char *)((int)piVar20 + 0x9f) != '\0')))))) {
//           iVar16 = piVar20[3] + -7;
//           iVar21 = piVar20[5] + -7;
//           uVar24 = (undefined2)((ulong)*(undefined4 *)0x6678 >> 0x10);
//           iVar22 = (int)*(undefined4 *)0x6678 + (uint)*(byte *)0x136a * 0x100;
//           iVar13 = FUN_24dd_4654(*(undefined1 *)0x137e);
//           iVar14 = ((uint)*(byte *)0x1374 + iVar13) * 0x100;
//           if (*(char *)0x1388 == '\x01') {
//             iVar14 = iVar14 + 1;
//           }
//           FUN_202c_005a(iVar14,(int)*(undefined4 *)0x6678 + ((uint)*(byte *)0x1374 + iVar13) * 0x100
//                         ,(int)((ulong)*(undefined4 *)0x6678 >> 0x10),iVar22,uVar24,iVar21,iVar16);
//           if (*(char *)0x66af != '\0') {
//             iVar16 = piVar20[3];
//             local_e = piVar20[3] - 10;
//             if ((int)local_e <= (int)(iVar16 + 10U)) {
//               do {
//                 if ((local_e < 0x8000) && ((int)local_e < 0x1f8)) {
//                   iVar21 = piVar20[5];
//                   local_10 = piVar20[5] - 10;
//                   if ((int)local_10 <= (int)(iVar21 + 10U)) {
//                     do {
//                       if ((local_10 < 0x8000) && ((int)local_10 < 0x15e)) {
//                         iVar13 = 0x20;
//                         bVar8 = FUN_24dd_4161();
//                         if ((*(byte *)(iVar13 + 0x14e0) & bVar8) != 0) {
//                           iVar13 = 0x20;
//                           bVar8 = FUN_24dd_4161();
//                           if ((*(byte *)(iVar13 + 0x6604) & bVar8) != 0) {
//                             uVar5 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_10 * 4);
//                             pcVar3 = (char *)((int)uVar5 + local_e);
//                             *pcVar3 = *pcVar3 + '\x04';
//                             goto LAB_1000_3497;
//                           }
//                         }
//                         uVar5 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_10 * 4);
//                         bVar8 = *(byte *)((int)uVar5 + local_e);
//                         if ((0xa3 < bVar8) && (bVar8 < 0xa8)) {
//                           iVar13 = 0x20;
//                           bVar8 = FUN_24dd_4161();
//                           if ((*(byte *)(iVar13 + 0x6604) & bVar8) != 0) {
//                             uVar5 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_10 * 4);
//                             pcVar3 = (char *)((int)uVar5 + local_e);
//                             *pcVar3 = *pcVar3 + -4;
//                           }
//                         }
//                       }
// LAB_1000_3497:
//                       if (local_10 == iVar21 + 10U) break;
//                       local_10 = local_10 + 1;
//                     } while( true );
//                   }
//                 }
//                 if (local_e == iVar16 + 10U) break;
//                 local_e = local_e + 1;
//               } while( true );
//             }
//           }
//           *(undefined1 *)((int)piVar20 + 0x9f) = 0;
//           if (*(char *)0x4b8 != '\0') {
//             FUN_235c_095c(0,0x16,*(undefined2 *)0x678c,*(undefined2 *)0x678e);
//           }
//           *(undefined1 *)(piVar20 + 0x4d) = 1;
//           *(undefined1 *)((int)piVar20 + 0x99) = 0;
//           piVar20[0x18] = 0;
//           piVar20[0x19] = 0;
//           piVar20[0x1a] = 0;
//           piVar20[0x1b] = 0;
//           piVar20[0x28] = *(int *)(local_4 * 2 + 0x66e8);
//         }
//       }
//     }
//     else {
//       iVar16 = piVar20[3] + piVar20[0x19] + (uint)CARRY2(piVar20[2],piVar20[0x18]);
//       iVar21 = piVar20[5] + piVar20[0x1b] + (uint)CARRY2(piVar20[4],piVar20[0x1a]);
//       local_6 = 0;
//       while( true ) {
//         *(undefined1 *)((int)piVar20 + local_6 + 0xa2) = 0;
//         bVar8 = *(byte *)(local_6 + 0x1ae);
//         uStack_30 = (uint)bVar8;
//         if (uStack_30 < 0x8000) {
//           local_8 = 0;
//           while( true ) {
//             iVar13 = 0x20;
//             bVar6 = FUN_24dd_4161();
//             if ((*(byte *)(iVar13 + 0x14c0) & bVar6) == 0) {
//               pcVar3 = (char *)((int)piVar20 + local_6 + 0xa2);
//               *pcVar3 = *pcVar3 + '\x01';
//             }
//             uStack_30 = (uint)bVar8;
//             if (local_8 == uStack_30) break;
//             local_8 = local_8 + 1;
//           }
//         }
//         if (iVar16 < 4) {
//           *(char *)((int)piVar20 + 0xa5) = *(char *)((int)piVar20 + 0xa5) + '\x05';
//         }
//         if (iVar21 < 5) {
//           *(char *)(piVar20 + 0x51) = (char)piVar20[0x51] + '\x05';
//         }
//         if (499 < iVar16) {
//           *(char *)((int)piVar20 + 0xa3) = *(char *)((int)piVar20 + 0xa3) + '\x05';
//         }
//         if (0x158 < iVar21) {
//           *(char *)(piVar20 + 0x52) = (char)piVar20[0x52] + '\x05';
//         }
//         if (local_6 == 3) break;
//         local_6 = local_6 + 1;
//       }
//       if (((*(byte *)(piVar20 + 0x51) < 2) && ((char)piVar20[0x52] != '\0')) &&
//          ((*(char *)((int)piVar20 + 0xa3) != '\0' || (*(char *)((int)piVar20 + 0xa5) != '\0')))) {
//         piVar20[5] = piVar20[5] + -1;
//         *(undefined1 *)((int)piVar20 + 0xa3) = 0;
//         *(undefined1 *)((int)piVar20 + 0xa5) = 0;
//         bVar8 = *(byte *)0x1af;
//         uStack_30 = (uint)bVar8;
//         if (uStack_30 < 0x8000) {
//           local_8 = 0;
//           while( true ) {
//             iVar16 = 0x20;
//             bVar6 = FUN_24dd_4161();
//             if ((*(byte *)(iVar16 + 0x14c0) & bVar6) == 0) {
//               *(char *)((int)piVar20 + 0xa3) = *(char *)((int)piVar20 + 0xa3) + '\x01';
//             }
//             uStack_30 = (uint)bVar8;
//             if (local_8 == uStack_30) break;
//             local_8 = local_8 + 1;
//           }
//         }
//         bVar8 = *(byte *)0x1b1;
//         uStack_30 = (uint)bVar8;
//         if (uStack_30 < 0x8000) {
//           local_8 = 0;
//           while( true ) {
//             iVar16 = 0x20;
//             bVar6 = FUN_24dd_4161();
//             if ((*(byte *)(iVar16 + 0x14c0) & bVar6) == 0) {
//               *(char *)((int)piVar20 + 0xa5) = *(char *)((int)piVar20 + 0xa5) + '\x01';
//             }
//             uStack_30 = (uint)bVar8;
//             if (local_8 == uStack_30) break;
//             local_8 = local_8 + 1;
//           }
//         }
//       }
//       if (((*(byte *)(piVar20 + 0x52) < 2) && ((char)piVar20[0x51] != '\0')) &&
//          ((*(char *)((int)piVar20 + 0xa3) != '\0' || (*(char *)((int)piVar20 + 0xa5) != '\0')))) {
//         piVar20[5] = piVar20[5] + 1;
//         *(undefined1 *)((int)piVar20 + 0xa3) = 0;
//         *(undefined1 *)((int)piVar20 + 0xa5) = 0;
//         bVar8 = *(byte *)0x1af;
//         uStack_30 = (uint)bVar8;
//         if (uStack_30 < 0x8000) {
//           local_8 = 0;
//           while( true ) {
//             iVar16 = 0x20;
//             bVar6 = FUN_24dd_4161();
//             if ((*(byte *)(iVar16 + 0x14c0) & bVar6) == 0) {
//               *(char *)((int)piVar20 + 0xa3) = *(char *)((int)piVar20 + 0xa3) + '\x01';
//             }
//             uStack_30 = (uint)bVar8;
//             if (local_8 == uStack_30) break;
//             local_8 = local_8 + 1;
//           }
//         }
//         bVar8 = *(byte *)0x1b1;
//         uStack_30 = (uint)bVar8;
//         if (uStack_30 < 0x8000) {
//           local_8 = 0;
//           while( true ) {
//             iVar16 = 0x20;
//             bVar6 = FUN_24dd_4161();
//             if ((*(byte *)(iVar16 + 0x14c0) & bVar6) == 0) {
//               *(char *)((int)piVar20 + 0xa5) = *(char *)((int)piVar20 + 0xa5) + '\x01';
//             }
//             uStack_30 = (uint)bVar8;
//             if (local_8 == uStack_30) break;
//             local_8 = local_8 + 1;
//           }
//         }
//       }
//       bVar8 = *(byte *)0x669c;
//       if (bVar8 != 0) {
//         local_8 = 1;
//         while( true ) {
//           if ((((*(char *)((int)*(undefined4 *)0x6698 + local_8 * 0xe + -2) != '\0') &&
//                (piVar20[3] + -5 < *(int *)((int)*(undefined4 *)0x6698 + local_8 * 0xe + -0xe))) &&
//               (*(int *)((int)*(undefined4 *)0x6698 + local_8 * 0xe + -0xe) < piVar20[3] + 5)) &&
//              ((piVar20[5] + -5 < *(int *)((int)*(undefined4 *)0x6698 + local_8 * 0xe + -10) &&
//               (*(int *)((int)*(undefined4 *)0x6698 + local_8 * 0xe + -10) < piVar20[5] + 7)))) {
//             cVar7 = *(char *)((int)*(undefined4 *)0x6698 + local_8 * 0xe + -2);
//             if (cVar7 == '\x02') {
//               uVar15 = piVar20[0x28];
//               if (((int)uVar15 >> 0xf < 0) ||
//                  ((-1 < (int)uVar15 && (uVar15 < *(uint *)(local_4 * 2 + 0x66e8))))) {
//                 *(undefined1 *)((int)*(undefined4 *)0x6698 + local_8 * 0xe + -2) = 0;
//                 iVar16 = FUN_24dd_4654(0x33);
//                 piVar20[0x28] =
//                      piVar20[0x28] +
//                      (int)(((ulong)(iVar16 + 10) * (ulong)*(uint *)(local_4 * 2 + 0x66e8) & 0xffff)
//                           / 100);
//                 uVar15 = piVar20[0x28];
//                 bVar25 = -1 < (int)uVar15 >> 0xf;
//                 if (((int)uVar15 < 0 && bVar25) ||
//                    ((bVar25 && (*(uint *)(local_4 * 2 + 0x66e8) < uVar15)))) {
//                   piVar20[0x28] = *(int *)(local_4 * 2 + 0x66e8);
//                 }
//               }
//             }
//             else if (cVar7 == '\x01') {
//               uVar15 = FUN_24dd_4654(10);
//               if (uVar15 < 2) {
//                 *(undefined1 *)((int)*(undefined4 *)0x6698 + local_8 * 0xe + -2) = 0;
//                 FUN_202c_1b84(0x24dd,*(undefined2 *)
//                                       ((int)*(undefined4 *)0x6698 + local_8 * 0xe + -10),
//                               *(undefined2 *)((int)*(undefined4 *)0x6698 + local_8 * 0xe + -0xe),1);
//               }
//               else {
//                 *(undefined1 *)((int)piVar20 + 0x99) = 0;
//                 piVar20[0x24] = -1;
//                 *(uint *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) =
//                      (uint)*(byte *)((int)*(undefined4 *)0x6698 + local_8 * 0xe + -1);
//                 *(uint *)((int)piVar20 + piVar20[0x27] * 2 + 0x7d) =
//                      (uint)*(byte *)(*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) + 0xe0d);
//                 if (*(char *)0x4b8 != '\0') {
//                   FUN_235c_095c(0,0x19,*(undefined2 *)0x6798,*(undefined2 *)0x679a);
//                 }
//                 *(undefined1 *)((int)*(undefined4 *)0x6698 + local_8 * 0xe + -2) = 0;
//                 *(undefined1 *)((int)piVar20 + piVar20[0x27] + 0x6f) = 1;
//                 iVar16 = piVar20[0x27];
//                 piVar20[iVar16 * 2 + 0x2c] = 0;
//                 piVar20[iVar16 * 2 + 0x2d] = 0;
//               }
//             }
//           }
//           uStack_30 = (uint)bVar8;
//           if (local_8 == uStack_30) break;
//           local_8 = local_8 + 1;
//         }
//       }
//       if (*(char *)(*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) + 0x11a5) == '\x02') {
//         local_6 = 0;
//         while( true ) {
//           uVar24 = (undefined2)((ulong)*(undefined4 *)0x6688 >> 0x10);
//           iVar16 = (int)*(undefined4 *)0x6688 + local_6 * 0x14;
//           if (((uint)(*(byte *)(iVar16 + 0x10) & 0x7f) ==
//                *(uint *)((int)piVar20 + piVar20[0x27] * 2 + 0x73)) &&
//              ((*(byte *)(iVar16 + 0x10) & 0x80) == *(byte *)(local_4 + 0x6c))) {
//             if (*(char *)(*(byte *)(local_4 * 7 + 0x6722) + 0x783b) != '\0') {
//               *(char *)(iVar16 + 0x11) =
//                    *(char *)(iVar16 + 0x11) - (((byte)*(undefined2 *)0x6520 & 1) + 1);
//             }
//             if (*(char *)(*(byte *)(local_4 * 7 + 0x6723) + 0x783b) != '\0') {
//               *(char *)(iVar16 + 0x11) =
//                    *(char *)(iVar16 + 0x11) + ((byte)*(undefined2 *)0x6520 & 1) + 1;
//             }
//             if (0x7f < *(byte *)(iVar16 + 0x11)) {
//               *(char *)(iVar16 + 0x11) = *(char *)(iVar16 + 0x11) + -0x80;
//             }
//             *(undefined1 *)(piVar20 + 0x50) = 0;
//           }
//           if (local_6 == 600) break;
//           local_6 = local_6 + 1;
//         }
//       }
//       if (((((char)piVar20[0x50] == '\0') &&
//            (*(char *)(*(byte *)(local_4 * 7 + 0x6720) + 0x783b) == '\0')) &&
//           (*(char *)(*(byte *)(local_4 * 7 + 0x6722) + 0x783b) == '\0')) &&
//          (*(char *)(*(byte *)(local_4 * 7 + 0x6723) + 0x783b) == '\0')) {
//         *(undefined1 *)(piVar20 + 0x50) = 1;
//       }
//       if (piVar20[0x2c] != 0 || piVar20[0x2d] != 0) {
//         uVar17 = piVar20[0x2c];
//         iVar16 = piVar20[0x2d];
//         puVar1 = (uint *)(piVar20 + 0x2a);
//         uVar15 = *puVar1;
//         *puVar1 = *puVar1 + uVar17;
//         piVar20[0x2b] = piVar20[0x2b] + iVar16 + (uint)CARRY2(uVar15,uVar17);
//         if ((*(char *)(*(byte *)(local_4 * 7 + 0x6720) + 0x783b) == '\0') &&
//            (*(char *)(*(byte *)(local_4 * 7 + 0x6721) + 0x783b) == '\0')) {
//           iVar16 = piVar20[0x2d];
//           FUN_24dd_3d80();
//           iVar21 = FUN_24dd_3dbd();
//           piVar20[0x2c] = iVar21;
//           piVar20[0x2d] = iVar16;
//         }
//         if (*(char *)((int)piVar20 + 0x9b) == '\0') {
//           if (piVar20[0x2b] < 0xc) {
//             piVar20[0x2c] = 0;
//             piVar20[0x2d] = 0;
//             piVar20[0x2b] = 0xc;
//           }
//           if (0x40 < piVar20[0x2b]) {
//             piVar20[0x2c] = 0;
//             piVar20[0x2d] = 0;
//             piVar20[0x2b] = 0x40;
//           }
//         }
//         else {
//           if (0x74 < piVar20[0x2b]) {
//             piVar20[0x2c] = 0;
//             piVar20[0x2d] = 0;
//             piVar20[0x2b] = 0x74;
//           }
//           if (piVar20[0x2b] < 0x40) {
//             piVar20[0x2c] = 0;
//             piVar20[0x2d] = 0;
//             piVar20[0x2b] = 0x40;
//           }
//         }
//       }
//       if ((((char)piVar20[0x50] == '\0') || ((char)piVar20[0x4e] == '\0')) ||
//          (*(char *)(*(byte *)(local_4 * 7 + 0x6725) + 0x783b) == '\0')) {
//         bVar25 = false;
//       }
//       else {
//         bVar25 = true;
//       }
//       if (!bVar25) {
//         if (*(char *)(*(byte *)(local_4 * 7 + 0x6720) + 0x783b) != '\0') {
//           if (*(char *)((int)piVar20 + 0x9b) == '\0') {
//             if ((piVar20[0x2d] < 1) || ((piVar20[0x2d] < 2 && ((uint)piVar20[0x2c] < 0x1170)))) {
//               puVar1 = (uint *)(piVar20 + 0x2c);
//               uVar15 = *puVar1;
//               *puVar1 = *puVar1 + 4000;
//               piVar20[0x2d] = piVar20[0x2d] + (uint)(0xf05f < uVar15);
//             }
//           }
//           else if ((*(char *)((int)piVar20 + 0x9b) == '\x01') &&
//                   ((-2 < piVar20[0x2d] || ((-3 < piVar20[0x2d] && (0xee90 < (uint)piVar20[0x2c])))))
//                   ) {
//             puVar1 = (uint *)(piVar20 + 0x2c);
//             uVar15 = *puVar1;
//             *puVar1 = *puVar1 - 4000;
//             piVar20[0x2d] = piVar20[0x2d] - (uint)(uVar15 < 4000);
//           }
//         }
//         if (*(char *)(*(byte *)(local_4 * 7 + 0x6721) + 0x783b) != '\0') {
//           if (*(char *)((int)piVar20 + 0x9b) == '\x01') {
//             if ((piVar20[0x2d] < 1) || ((piVar20[0x2d] < 2 && ((uint)piVar20[0x2c] < 0x1170)))) {
//               puVar1 = (uint *)(piVar20 + 0x2c);
//               uVar15 = *puVar1;
//               *puVar1 = *puVar1 + 4000;
//               piVar20[0x2d] = piVar20[0x2d] + (uint)(0xf05f < uVar15);
//             }
//           }
//           else if ((*(char *)((int)piVar20 + 0x9b) == '\0') &&
//                   ((-2 < piVar20[0x2d] || ((-3 < piVar20[0x2d] && (0xee90 < (uint)piVar20[0x2c])))))
//                   ) {
//             puVar1 = (uint *)(piVar20 + 0x2c);
//             uVar15 = *puVar1;
//             *puVar1 = *puVar1 - 4000;
//             piVar20[0x2d] = piVar20[0x2d] - (uint)(uVar15 < 4000);
//           }
//         }
//       }
//       if (*(char *)(*(byte *)(local_4 * 7 + 0x6725) + 0x783b) == '\0') {
//         if (*(char *)(*(byte *)(local_4 * 7 + 0x6726) + 0x783b) == '\0') {
//           *(undefined1 *)((int)piVar20 + 0x93) = 1;
//         }
//         else {
//           *(undefined1 *)(piVar20 + 6) = 0;
//           *(undefined1 *)(piVar20 + 0x4e) = 0;
//           if (((char)piVar20[0x52] != '\0') && (*(char *)((int)piVar20 + 0x93) != '\0')) {
//             puVar1 = (uint *)(piVar20 + 0x1a);
//             uVar15 = *puVar1;
//             *puVar1 = *puVar1 + 0x2500;
//             piVar20[0x1b] = piVar20[0x1b] - (uint)(uVar15 < 0xdb00);
//             *(undefined1 *)((int)piVar20 + 0x93) = 0;
//           }
//         }
//       }
//       else {
//         if ((char)piVar20[0x4e] != '\0') {
//           if (*(char *)(*(byte *)(local_4 * 7 + 0x6720) + 0x783b) != '\0') {
//             puVar1 = (uint *)(piVar20 + 0x13);
//             uVar15 = *puVar1;
//             *puVar1 = *puVar1 - 0x18;
//             piVar20[0x14] = piVar20[0x14] - (uint)(uVar15 < 0x18);
//           }
//           if (*(char *)(*(byte *)(local_4 * 7 + 0x6721) + 0x783b) != '\0') {
//             puVar1 = (uint *)(piVar20 + 0x13);
//             uVar15 = *puVar1;
//             *puVar1 = *puVar1 + 0x18;
//             piVar20[0x14] = piVar20[0x14] + (uint)(0xffe7 < uVar15);
//           }
//           if ((piVar20[0x14] < 0) || ((piVar20[0x14] < 1 && ((uint)piVar20[0x13] < 0xaa)))) {
//             piVar20[0x13] = 0xaa;
//             piVar20[0x14] = 0;
//           }
//           if ((0 < piVar20[0x14]) || ((-1 < piVar20[0x14] && (4000 < (uint)piVar20[0x13])))) {
//             piVar20[0x13] = 4000;
//             piVar20[0x14] = 0;
//           }
//         }
//         if (*(char *)(*(byte *)(local_4 * 7 + 0x6726) + 0x783b) != '\0') {
//           *(undefined1 *)(piVar20 + 0x4e) = 1;
//           *(undefined1 *)(piVar20 + 6) = 0;
//           if (*(char *)0x4b8 != '\0') {
//             FUN_235c_095c(0,6,*(undefined2 *)0x674c,*(undefined2 *)0x674e);
//           }
//           piVar20[8] = piVar20[3];
//           piVar20[10] = piVar20[5];
//           iVar16 = *(int *)(piVar20[0x2b] * 8 + 0x15a0);
//           iVar21 = FUN_24dd_3e7c();
//           piVar20[0xb] = iVar21;
//           piVar20[0xc] = iVar16;
//           iVar16 = *(int *)(piVar20[0x2b] * 8 + 0x15a4);
//           iVar21 = FUN_24dd_3e7c();
//           piVar20[0xd] = iVar21;
//           piVar20[0xe] = iVar16;
//           piVar20[0x13] = 4000;
//           piVar20[0x14] = 0;
//           *(undefined1 *)(*(byte *)(local_4 * 7 + 0x6726) + 0x783b) = 0;
//         }
//       }
//       local_8 = 1;
//       while( true ) {
//         if (-1 < *(int *)((int)piVar20 + local_8 * 2 + 0x87)) {
//           piVar2 = (int *)((int)piVar20 + local_8 * 2 + 0x87);
//           *piVar2 = *piVar2 + -1;
//         }
//         if (local_8 == 5) break;
//         local_8 = local_8 + 1;
//       }
//       if (*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x7d) < 1) {
//         *(undefined1 *)((int)piVar20 + piVar20[0x27] + 0x6f) = 0;
//         iVar13 = *(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) * 4;
//         iVar16 = *(int *)(iVar13 + 0x647a);
//         iVar21 = piVar20[0x27];
//         piVar20[iVar21 * 2 + 0x2c] = *(int *)(iVar13 + 0x6478);
//         piVar20[iVar21 * 2 + 0x2d] = iVar16;
//         *(uint *)((int)piVar20 + piVar20[0x27] * 2 + 0x7d) =
//              (uint)*(byte *)(*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) + 0xe0d);
//       }
//       if ((0 < piVar20[piVar20[0x27] * 2 + 0x2d]) ||
//          ((-1 < piVar20[piVar20[0x27] * 2 + 0x2d] && (piVar20[piVar20[0x27] * 2 + 0x2c] != 0)))) {
//         iVar21 = piVar20[0x27];
//         piVar2 = piVar20 + iVar21 * 2 + 0x2c;
//         iVar16 = *piVar2;
//         *piVar2 = *piVar2 + -1;
//         piVar20[iVar21 * 2 + 0x2d] = piVar20[iVar21 * 2 + 0x2d] - (uint)(iVar16 == 0);
//         if ((piVar20[piVar20[0x27] * 2 + 0x2d] < 0) ||
//            ((piVar20[piVar20[0x27] * 2 + 0x2d] < 1 && (piVar20[piVar20[0x27] * 2 + 0x2c] == 0)))) {
//           if ((*(char *)0x4b8 != '\0') &&
//              ((*(byte *)(*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) + 0xed5) & 1) == 1)) {
//             FUN_235c_095c(0,0x19,*(undefined2 *)0x6798,*(undefined2 *)0x679a);
//           }
//           *(undefined1 *)((int)piVar20 + piVar20[0x27] + 0x6f) = 1;
//         }
//       }
//       if ((-1 < piVar20[0x24]) && (piVar20[0x24] = piVar20[0x24] + -1, piVar20[0x24] == 0)) {
//         *(undefined1 *)((int)piVar20 + 0x99) = 0;
//       }
//       if (((*(char *)(*(byte *)(local_4 * 7 + 0x6724) + 0x783b) == '\0') ||
//           (*(char *)(*(byte *)(local_4 * 7 + 0x6725) + 0x783b) != '\0')) ||
//          (*(char *)((int)piVar20 + piVar20[0x27] + 0x6f) == '\0')) {
//         if ((*(char *)0x4b8 != '\0') &&
//            ((*(byte *)(*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) + 0xb8d) & 1) == 1)) {
//           FUN_235c_09eb(CONCAT11((char)((uint)(piVar20[0x27] * 2) >> 8),
//                                  *(undefined1 *)
//                                   (*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) + 0xb65)));
//         }
//       }
//       else if (*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x87) < 0) {
//         piVar2 = (int *)((int)piVar20 + piVar20[0x27] * 2 + 0x7d);
//         *piVar2 = *piVar2 + -1;
//         *(undefined2 *)((int)piVar20 + piVar20[0x27] * 2 + 0x87) =
//              *(undefined2 *)(*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) * 2 + 0xd6c);
//         *(undefined1 *)((int)piVar20 + 0x99) = 1;
//         piVar20[0x24] = (uint)*(byte *)(*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) + 0xf75);
//         iVar16 = 0;
//         uVar15 = FUN_24dd_3d80();
//         iVar21 = uVar15 + piVar20[2];
//         iVar14 = iVar16 + piVar20[3] + (uint)CARRY2(uVar15,piVar20[2]);
//         iVar16 = 0;
//         uVar15 = FUN_24dd_3d80();
//         iVar13 = uVar15 + piVar20[4];
//         iVar16 = iVar16 + piVar20[5] + (uint)CARRY2(uVar15,piVar20[4]) + -1;
//         if ((*(char *)(*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) + 0xe85) != '\0') &&
//            (iVar22 = FUN_24dd_4654(*(undefined1 *)
//                                     (*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) + 0xe85)),
//            iVar22 == 0)) {
//           piVar20[0x25] = (uint)*(byte *)(*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) + 0xead)
//           ;
//         }
//         if ((*(char *)0x4b8 != '\0') &&
//            (*(char *)(*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) + 0xb65) != '\0')) {
//           if ((*(byte *)(*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) + 0xb8d) & 1) == 1) {
//             cVar7 = FUN_235c_0a1e(CONCAT11((char)((uint)(piVar20[0x27] * 2) >> 8),
//                                            *(undefined1 *)
//                                             (*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) +
//                                             0xb65)));
//             if (cVar7 == '\0') {
//               iVar12 = (uint)*(byte *)(*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) + 0xb65) *
//                        4;
//               iVar22 = ((piVar20[0x27] & 0x7fffU) >> 7) * 0x100;
//               if ((*(byte *)(*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) + 0xb8d) & 1) == 1) {
//                 iVar22 = iVar22 + 1;
//               }
//               FUN_235c_095c(iVar22,CONCAT11((char)((uint)(piVar20[0x27] * 2) >> 8),
//                                             *(undefined1 *)
//                                              (*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) +
//                                              0xb65)),*(undefined2 *)(iVar12 + 0x6734),
//                             *(undefined2 *)(iVar12 + 0x6736));
//             }
//           }
//           else {
//             iVar12 = (uint)*(byte *)(*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) + 0xb65) * 4;
//             iVar22 = ((piVar20[0x27] & 0x7fffU) >> 7) * 0x100;
//             if ((*(byte *)(*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) + 0xb8d) & 1) == 1) {
//               iVar22 = iVar22 + 1;
//             }
//             FUN_235c_095c(iVar22,CONCAT11((char)((uint)(piVar20[0x27] * 2) >> 8),
//                                           *(undefined1 *)
//                                            (*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) +
//                                            0xb65)),*(undefined2 *)(iVar12 + 0x6734),
//                           *(undefined2 *)(iVar12 + 0x6736));
//           }
//         }
//         if (*(char *)(*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) + 0xa4d) == '\x01') {
//           local_a = *(int *)(*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) * 2 + 0xbdc);
//           if (local_a < 100) {
//             local_a = 100;
//           }
//           bVar8 = *(byte *)(*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) + 0xccd);
//           if (bVar8 != 0) {
//             local_c = 1;
//             while( true ) {
//               uVar15 = (uint)*(byte *)(local_4 + 0x6c) |
//                        *(uint *)((int)piVar20 + piVar20[0x27] * 2 + 0x73);
//               uVar24 = *(undefined2 *)
//                         (*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) * 2 + 0xbdc);
//               iVar22 = piVar20[0x19];
//               iVar26 = iVar13;
//               iVar27 = iVar16;
//               iVar28 = iVar21;
//               iVar29 = iVar14;
//               FUN_24dd_3d80(local_a,local_a >> 0xf,uVar24,iVar13,iVar16,iVar21,iVar14,uVar15);
//               uVar31 = FUN_24dd_3dbd();
//               iVar12 = piVar20[0x1b];
//               FUN_24dd_3d80(local_a,local_a >> 0xf,uVar31,iVar22);
//               uVar11 = FUN_24dd_3dbd();
//               FUN_202c_18c0((char)piVar20[0x2b],uVar11,iVar12,uVar31,iVar22,uVar24,iVar26,iVar27,
//                             iVar28,iVar29,uVar15);
//               uStack_30 = (uint)bVar8;
//               if (local_c == uStack_30) break;
//               local_c = local_c + 1;
//             }
//           }
//         }
//         else {
//           bVar8 = *(byte *)(*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) + 0xccd);
//           if (bVar8 != 0) {
//             local_c = 1;
//             while( true ) {
//               FUN_202c_18c0(CONCAT11((char)((uint)(piVar20[0x27] * 2) >> 8),(char)piVar20[0x2b]),0,0
//                             ,0,0,*(undefined2 *)
//                                   (*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) * 2 + 0xbdc),
//                             iVar13,iVar16,iVar21,iVar14,
//                             (uint)*(byte *)(local_4 + 0x6c) |
//                             *(uint *)((int)piVar20 + piVar20[0x27] * 2 + 0x73));
//               uStack_30 = (uint)bVar8;
//               if (local_c == uStack_30) break;
//               local_c = local_c + 1;
//             }
//           }
//         }
//         iVar16 = 0;
//         FUN_24dd_3d80();
//         uVar17 = FUN_24dd_3dbd();
//         puVar1 = (uint *)(piVar20 + 0x18);
//         uVar15 = *puVar1;
//         *puVar1 = *puVar1 - uVar17;
//         piVar20[0x19] = (piVar20[0x19] - iVar16) - (uint)(uVar15 < uVar17);
//         iVar16 = 0;
//         FUN_24dd_3d80();
//         uVar17 = FUN_24dd_3dbd();
//         puVar1 = (uint *)(piVar20 + 0x1a);
//         uVar15 = *puVar1;
//         *puVar1 = *puVar1 - uVar17;
//         piVar20[0x1b] = (piVar20[0x1b] - iVar16) - (uint)(uVar15 < uVar17);
//       }
//       if ((0 < piVar20[0x25]) && (piVar20[0x25] = piVar20[0x25] + -1, piVar20[0x25] == 0)) {
//         uVar31 = 8;
//         uVar24 = 0;
//         iVar16 = piVar20[3];
//         iVar21 = piVar20[5];
//         uVar15 = FUN_24dd_4654(16000);
//         iVar13 = uVar15 + 0xe0c0;
//         iVar14 = (7999 < uVar15) - 1;
//         uVar15 = FUN_24dd_4654(20000);
//         FUN_202c_14b6(-20000 - uVar15,-1 - (uint)(0xb1e0 < uVar15),iVar13,iVar14,iVar21,iVar16,
//                       uVar24,uVar31);
//       }
//       if ((char)piVar20[0x52] != '\0') {
//         iVar16 = piVar20[0x19];
//         FUN_24dd_3d80();
//         iVar21 = FUN_24dd_3dbd();
//         piVar20[0x18] = iVar21;
//         piVar20[0x19] = iVar16;
//       }
//       if (((0 < piVar20[0x19]) || ((-1 < piVar20[0x19] && (piVar20[0x18] != 0)))) &&
//          (*(char *)((int)piVar20 + 0xa3) != '\0')) {
//         if ((piVar20[0x19] < 1) && ((piVar20[0x19] < 0 || ((uint)piVar20[0x18] < 0xd001)))) {
//           piVar20[0x18] = 0;
//           piVar20[0x19] = 0;
//         }
//         else {
//           if (*(char *)0x4b8 != '\0') {
//             FUN_235c_095c(0,0xf,*(undefined2 *)0x6770,*(undefined2 *)0x6772);
//           }
//           iVar21 = (~piVar20[0x19] + 1U) - (uint)(piVar20[0x18] != 0);
//           iVar16 = FUN_24dd_3dbd();
//           piVar20[0x18] = iVar16;
//           piVar20[0x19] = iVar21;
//         }
//       }
//       if ((piVar20[0x19] < 0) && (*(char *)((int)piVar20 + 0xa5) != '\0')) {
//         if ((piVar20[0x19] < -1) ||
//            ((0x7fff < (uint)piVar20[0x19] && ((uint)piVar20[0x18] < 0x3000)))) {
//           if (*(char *)0x4b8 != '\0') {
//             FUN_235c_095c(0,0xf,*(undefined2 *)0x6770,*(undefined2 *)0x6772);
//           }
//           iVar21 = (~piVar20[0x19] + 1U) - (uint)(piVar20[0x18] != 0);
//           iVar16 = FUN_24dd_3dbd();
//           piVar20[0x18] = iVar16;
//           piVar20[0x19] = iVar21;
//         }
//         else {
//           piVar20[0x18] = 0;
//           piVar20[0x19] = 0;
//         }
//       }
//       if (((0 < piVar20[0x1b]) || ((-1 < piVar20[0x1b] && (piVar20[0x1a] != 0)))) &&
//          ((char)piVar20[0x52] != '\0')) {
//         if ((piVar20[0x1b] < 1) && ((piVar20[0x1b] < 0 || ((uint)piVar20[0x1a] < 0xd001)))) {
//           piVar20[0x1a] = 0;
//           piVar20[0x1b] = 0;
//         }
//         else {
//           if (*(char *)0x4b8 != '\0') {
//             FUN_235c_095c(0,0xf,*(undefined2 *)0x6770,*(undefined2 *)0x6772);
//           }
//           iVar21 = (~piVar20[0x1b] + 1U) - (uint)(piVar20[0x1a] != 0);
//           iVar16 = FUN_24dd_3dbd();
//           piVar20[0x1a] = iVar16;
//           piVar20[0x1b] = iVar21;
//         }
//       }
//       if ((piVar20[0x1b] < 0) && ((char)piVar20[0x51] != '\0')) {
//         if ((piVar20[0x1b] < -1) ||
//            ((0x7fff < (uint)piVar20[0x1b] && ((uint)piVar20[0x1a] < 0x3000)))) {
//           if (*(char *)0x4b8 != '\0') {
//             FUN_235c_095c(0,0xf,*(undefined2 *)0x6770,*(undefined2 *)0x6772);
//           }
//           iVar21 = (~piVar20[0x1b] + 1U) - (uint)(piVar20[0x1a] != 0);
//           iVar16 = FUN_24dd_3dbd();
//           piVar20[0x1a] = iVar16;
//           piVar20[0x1b] = iVar21;
//         }
//         else {
//           piVar20[0x1a] = 0;
//           piVar20[0x1b] = 0;
//         }
//       }
//       if ((char)piVar20[0x52] == '\0') {
//         puVar1 = (uint *)(piVar20 + 0x1a);
//         uVar15 = *puVar1;
//         *puVar1 = *puVar1 + 0x5dc;
//         piVar20[0x1b] = piVar20[0x1b] + (uint)(0xfa23 < uVar15);
//       }
//       if ((piVar20[0x19] < 1) && ((piVar20[0x19] < 0 || (piVar20[0x18] == 0)))) {
//         bVar25 = false;
//       }
//       else {
//         bVar25 = true;
//       }
//       if (bVar25) {
//         if (*(byte *)((int)piVar20 + 0xa3) < 2) {
//           uVar17 = piVar20[0x18];
//           iVar16 = piVar20[0x19];
//           puVar1 = (uint *)(piVar20 + 2);
//           uVar15 = *puVar1;
//           *puVar1 = *puVar1 + uVar17;
//           piVar20[3] = piVar20[3] + iVar16 + (uint)CARRY2(uVar15,uVar17);
//         }
//       }
//       else if ((!bVar25) && (*(byte *)((int)piVar20 + 0xa5) < 2)) {
//         uVar17 = piVar20[0x18];
//         iVar16 = piVar20[0x19];
//         puVar1 = (uint *)(piVar20 + 2);
//         uVar15 = *puVar1;
//         *puVar1 = *puVar1 + uVar17;
//         piVar20[3] = piVar20[3] + iVar16 + (uint)CARRY2(uVar15,uVar17);
//       }
//       if ((piVar20[0x1b] < 1) && ((piVar20[0x1b] < 0 || (piVar20[0x1a] == 0)))) {
//         bVar25 = false;
//       }
//       else {
//         bVar25 = true;
//       }
//       if (bVar25) {
//         if (*(byte *)(piVar20 + 0x52) < 2) {
//           uVar17 = piVar20[0x1a];
//           iVar16 = piVar20[0x1b];
//           puVar1 = (uint *)(piVar20 + 4);
//           uVar15 = *puVar1;
//           *puVar1 = *puVar1 + uVar17;
//           piVar20[5] = piVar20[5] + iVar16 + (uint)CARRY2(uVar15,uVar17);
//         }
//       }
//       else if ((!bVar25) && (*(byte *)(piVar20 + 0x51) < 2)) {
//         uVar17 = piVar20[0x1a];
//         iVar16 = piVar20[0x1b];
//         puVar1 = (uint *)(piVar20 + 4);
//         uVar15 = *puVar1;
//         *puVar1 = *puVar1 + uVar17;
//         piVar20[5] = piVar20[5] + iVar16 + (uint)CARRY2(uVar15,uVar17);
//       }
//       if ((*(char *)((int)piVar20 + piVar20[0x27] + 0x6f) == '\0') ||
//          ((*(char *)(*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) + 0xb3d) != '\x01' &&
//           (*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) != 0x1d)))) {
//         *(undefined1 *)((int)piVar20 + 0x97) = 0;
//       }
//       else {
//         uVar15 = piVar20[2];
//         iVar16 = piVar20[3];
//         uVar17 = piVar20[4];
//         iVar21 = piVar20[5];
//         iVar13 = *(int *)(piVar20[0x2b] * 8 + 0x15a0);
//         uVar18 = FUN_24dd_3d80();
//         local_18 = uVar15 + uVar18;
//         local_16 = iVar16 + iVar13 + (uint)CARRY2(uVar15,uVar18);
//         iVar16 = *(int *)(piVar20[0x2b] * 8 + 0x15a4);
//         uVar15 = FUN_24dd_3d80();
//         local_1c = uVar17 + uVar15;
//         local_1a = iVar21 + -1 + iVar16 + (uint)CARRY2(uVar17,uVar15);
//         do {
//           uVar15 = *(uint *)(piVar20[0x2b] * 8 + 0x159e);
//           bVar25 = CARRY2(local_18,uVar15);
//           local_18 = local_18 + uVar15;
//           local_16 = local_16 + *(int *)(piVar20[0x2b] * 8 + 0x15a0) + (uint)bVar25;
//           uVar15 = *(uint *)(piVar20[0x2b] * 8 + 0x15a2);
//           bVar25 = CARRY2(local_1c,uVar15);
//           local_1c = local_1c + uVar15;
//           local_1a = local_1a + *(int *)(piVar20[0x2b] * 8 + 0x15a4) + (uint)bVar25;
//           uVar9 = FUN_1000_0d70(local_1a,local_16,0,local_4 ^ 1);
//           *(undefined1 *)((int)piVar20 + 0x97) = uVar9;
//           iVar16 = 0x20;
//           bVar8 = FUN_24dd_4161();
//           if (((((*(byte *)(iVar16 + 0x14c0) & bVar8) == 0) ||
//                (*(char *)((int)piVar20 + 0x97) != '\0')) || (local_16 < 0)) ||
//              ((0x1f7 < local_16 || (local_1a < 0)))) break;
//         } while (local_1a < 0x15e);
//         *local_2e = local_16;
//         piVar20[1] = local_1a;
//       }
//       if (*(char *)(*(byte *)(local_4 * 7 + 0x6725) + 0x783b) == '\0') {
//         *(undefined1 *)(piVar20 + 0x4c) = 0;
//         if ((char)piVar20[0x50] != '\0') {
//           if ((*(char *)(*(byte *)(local_4 * 7 + 0x6723) + 0x783b) == '\0') &&
//              (*(char *)(*(byte *)(local_4 * 7 + 0x6722) + 0x783b) != '\0')) {
//             if (((uint)piVar20[0x19] < 0x8000) ||
//                ((-2 < piVar20[0x19] && (0x8e00 < (uint)piVar20[0x18])))) {
//               puVar1 = (uint *)(piVar20 + 0x18);
//               uVar15 = *puVar1;
//               *puVar1 = *puVar1 - 3000;
//               piVar20[0x19] = piVar20[0x19] - (uint)(uVar15 < 3000);
//             }
//             if (*(char *)((int)piVar20 + 0x9b) != '\0') {
//               piVar20[0x2c] = 0;
//               piVar20[0x2d] = 0;
//               if (0x40 < piVar20[0x2b]) {
//                 piVar20[0x2b] = 0x80 - piVar20[0x2b];
//               }
//               *(undefined1 *)((int)piVar20 + 0x9b) = 0;
//             }
//             *(undefined1 *)((int)piVar20 + 0x9d) = 1;
//           }
//           if ((*(char *)(*(byte *)(local_4 * 7 + 0x6722) + 0x783b) == '\0') &&
//              (*(char *)(*(byte *)(local_4 * 7 + 0x6723) + 0x783b) != '\0')) {
//             if ((piVar20[0x19] < 0) || ((piVar20[0x19] < 1 && ((uint)piVar20[0x18] < 0x7200)))) {
//               puVar1 = (uint *)(piVar20 + 0x18);
//               uVar15 = *puVar1;
//               *puVar1 = *puVar1 + 3000;
//               piVar20[0x19] = piVar20[0x19] + (uint)(0xf447 < uVar15);
//             }
//             if (*(char *)((int)piVar20 + 0x9b) == '\0') {
//               piVar20[0x2c] = 0;
//               piVar20[0x2d] = 0;
//               if (piVar20[0x2b] < 0x40) {
//                 piVar20[0x2b] = 0x80 - piVar20[0x2b];
//               }
//               *(undefined1 *)((int)piVar20 + 0x9b) = 1;
//             }
//             *(undefined1 *)((int)piVar20 + 0x9d) = 1;
//           }
//           if ((*(char *)(*(byte *)(local_4 * 7 + 0x6722) + 0x783b) == '\0') ||
//              (*(char *)(*(byte *)(local_4 * 7 + 0x6723) + 0x783b) == '\0')) {
//             *(undefined1 *)(piVar20 + 0x4f) = 1;
//           }
//           else if ((char)piVar20[0x4f] != '\0') {
//             *(undefined1 *)(piVar20 + 0x4f) = 0;
//             iVar16 = *(int *)(piVar20[0x2b] * 8 + 0x15a0);
//             uVar18 = FUN_24dd_3e7c();
//             uVar15 = piVar20[2];
//             iVar21 = iVar16 + piVar20[3] + (uint)CARRY2(uVar18,piVar20[2]);
//             iVar16 = *(int *)(piVar20[0x2b] * 8 + 0x15a4);
//             uVar19 = FUN_24dd_3e7c();
//             uVar17 = piVar20[4];
//             iVar16 = iVar16 + piVar20[5] + (uint)CARRY2(uVar19,piVar20[4]);
//             local_20 = 0xfffc;
//             local_1e = -1;
//             while( true ) {
//               local_24 = 0xfffc;
//               local_22 = -1;
//               while( true ) {
//                 iVar13 = iVar16 + local_24;
//                 iVar14 = 0x20;
//                 bVar8 = FUN_24dd_4161();
//                 if (((*(byte *)(iVar14 + 0x6624) & bVar8) != 0) &&
//                    (iVar14 = FUN_24dd_4654(3), iVar14 == 0)) {
//                   uVar32 = 3;
//                   uVar5 = *(undefined4 *)((int)*(undefined4 *)0x6674 + iVar13 * 4);
//                   uVar10 = (uint)*(byte *)((int)uVar5 + iVar21 + local_20);
//                   uVar33 = 0;
//                   uVar30 = 0;
//                   uVar11 = 0;
//                   uVar31 = 0;
//                   iVar14 = iVar21 + local_20;
//                   uVar24 = FUN_24dd_4654(0x80);
//                   FUN_202c_165d(uVar24,uVar31,uVar11,uVar30,uVar33,iVar13,iVar14,uVar10,uVar32);
//                 }
//                 if ((local_22 == 0) && (local_24 == 4)) break;
//                 bVar25 = 0xfffe < local_24;
//                 local_24 = local_24 + 1;
//                 local_22 = local_22 + (uint)bVar25;
//               }
//               if ((local_1e == 0) && (local_20 == 4)) break;
//               bVar25 = 0xfffe < local_20;
//               local_20 = local_20 + 1;
//               local_1e = local_1e + (uint)bVar25;
//             }
//             uVar24 = (undefined2)((ulong)*(undefined4 *)0x6678 >> 0x10);
//             iVar12 = (int)*(undefined4 *)0x6678 + (uint)*(byte *)0x1371 * 0x100;
//             iVar13 = iVar16 + -7;
//             iVar14 = iVar21 + -7;
//             iVar22 = FUN_24dd_4654(*(undefined1 *)0x1385);
//             FUN_202c_005a(1,(int)*(undefined4 *)0x6678 + ((uint)*(byte *)0x1376 + iVar22) * 0x100,
//                           (int)((ulong)*(undefined4 *)0x6678 >> 0x10),iVar12,uVar24,iVar13,iVar14);
//             if (*(char *)0x66af != '\0') {
//               local_e = iVar21 - 10;
//               if ((int)local_e <= (int)(iVar21 + 10U)) {
//                 do {
//                   if ((local_e < 0x8000) && ((int)local_e < 0x1f8)) {
//                     local_10 = iVar16 - 10;
//                     if ((int)local_10 <= (int)(iVar16 + 10U)) {
//                       do {
//                         if ((local_10 < 0x8000) && ((int)local_10 < 0x15e)) {
//                           iVar13 = 0x20;
//                           bVar8 = FUN_24dd_4161();
//                           if ((*(byte *)(iVar13 + 0x14e0) & bVar8) != 0) {
//                             iVar13 = 0x20;
//                             bVar8 = FUN_24dd_4161();
//                             if ((*(byte *)(iVar13 + 0x6604) & bVar8) != 0) {
//                               uVar5 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_10 * 4);
//                               pcVar3 = (char *)((int)uVar5 + local_e);
//                               *pcVar3 = *pcVar3 + '\x04';
//                               goto LAB_1000_2bde;
//                             }
//                           }
//                           uVar5 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_10 * 4);
//                           bVar8 = *(byte *)((int)uVar5 + local_e);
//                           if ((0xa3 < bVar8) && (bVar8 < 0xa8)) {
//                             iVar13 = 0x20;
//                             bVar8 = FUN_24dd_4161();
//                             if ((*(byte *)(iVar13 + 0x6604) & bVar8) != 0) {
//                               uVar5 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_10 * 4);
//                               pcVar3 = (char *)((int)uVar5 + local_e);
//                               *pcVar3 = *pcVar3 + -4;
//                             }
//                           }
//                         }
// LAB_1000_2bde:
//                         if (local_10 == iVar16 + 10U) break;
//                         local_10 = local_10 + 1;
//                       } while( true );
//                     }
//                   }
//                   if (local_e == iVar21 + 10U) break;
//                   local_e = local_e + 1;
//                 } while( true );
//               }
//             }
//             iVar13 = *(int *)(piVar20[0x2b] * 8 + 0x15a0);
//             uVar10 = FUN_24dd_3e7c();
//             iVar14 = iVar13 + iVar21 + -7 + (uint)CARRY2(uVar10,uVar18 + uVar15);
//             iVar21 = *(int *)(piVar20[0x2b] * 8 + 0x15a4);
//             uVar15 = FUN_24dd_3e7c();
//             iVar22 = iVar21 + iVar16 + -7 + (uint)CARRY2(uVar15,uVar19 + uVar17);
//             uVar24 = (undefined2)((ulong)*(undefined4 *)0x6678 >> 0x10);
//             iVar12 = (int)*(undefined4 *)0x6678 + (uint)*(byte *)0x1371 * 0x100;
//             iVar16 = iVar22;
//             iVar21 = iVar14;
//             iVar13 = FUN_24dd_4654(*(undefined1 *)0x1385);
//             FUN_202c_005a(1,(int)*(undefined4 *)0x6678 + ((uint)*(byte *)0x1376 + iVar13) * 0x100,
//                           (int)((ulong)*(undefined4 *)0x6678 >> 0x10),iVar12,uVar24,iVar16,iVar21);
//             if (*(char *)0x66af != '\0') {
//               local_e = iVar14 - 3;
//               if ((int)local_e <= (int)(iVar14 + 0x11U)) {
//                 do {
//                   if ((local_e < 0x8000) && ((int)local_e < 0x1f8)) {
//                     local_10 = iVar22 - 3;
//                     if ((int)local_10 <= (int)(iVar22 + 0x11U)) {
//                       do {
//                         if ((local_10 < 0x8000) && ((int)local_10 < 0x15e)) {
//                           iVar16 = 0x20;
//                           bVar8 = FUN_24dd_4161();
//                           if ((*(byte *)(iVar16 + 0x14e0) & bVar8) != 0) {
//                             iVar16 = 0x20;
//                             bVar8 = FUN_24dd_4161();
//                             if ((*(byte *)(iVar16 + 0x6604) & bVar8) != 0) {
//                               uVar5 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_10 * 4);
//                               pcVar3 = (char *)((int)uVar5 + local_e);
//                               *pcVar3 = *pcVar3 + '\x04';
//                               goto LAB_1000_2dcc;
//                             }
//                           }
//                           uVar5 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_10 * 4);
//                           bVar8 = *(byte *)((int)uVar5 + local_e);
//                           if ((0xa3 < bVar8) && (bVar8 < 0xa8)) {
//                             iVar16 = 0x20;
//                             bVar8 = FUN_24dd_4161();
//                             if ((*(byte *)(iVar16 + 0x6604) & bVar8) != 0) {
//                               uVar5 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_10 * 4);
//                               pcVar3 = (char *)((int)uVar5 + local_e);
//                               *pcVar3 = *pcVar3 + -4;
//                             }
//                           }
//                         }
// LAB_1000_2dcc:
//                         if (local_10 == iVar22 + 0x11U) break;
//                         local_10 = local_10 + 1;
//                       } while( true );
//                     }
//                   }
//                   if (local_e == iVar14 + 0x11U) break;
//                   local_e = local_e + 1;
//                 } while( true );
//               }
//             }
//           }
//           if ((*(char *)(*(byte *)(local_4 * 7 + 0x6722) + 0x783b) == '\0') &&
//              (*(char *)(*(byte *)(local_4 * 7 + 0x6723) + 0x783b) == '\0')) {
//             *(undefined1 *)((int)piVar20 + 0x9d) = 0;
//           }
//         }
//       }
//       else {
//         if ((char)piVar20[0x4c] == '\0') {
//           *(undefined1 *)(*(byte *)(local_4 * 7 + 0x6722) + 0x783b) = 0;
//           *(undefined1 *)(*(byte *)(local_4 * 7 + 0x6723) + 0x783b) = 0;
//           *(undefined1 *)(piVar20 + 0x4c) = 1;
//         }
//         *(undefined1 *)((int)piVar20 + 0x99) = 0;
//         *(undefined1 *)((int)piVar20 + 0x9d) = 0;
//         if ((*(byte *)(*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) + 0xb8d) & 1) == 1) {
//           FUN_235c_09eb(CONCAT11((char)((uint)(piVar20[0x27] * 2) >> 8),
//                                  *(undefined1 *)
//                                   (*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) + 0xb65)));
//         }
//         if ((*(char *)((int)piVar20 + piVar20[0x27] + 0x6f) != '\0') || (*(char *)0x6716 != '\0')) {
//           if (*(char *)(*(byte *)(local_4 * 7 + 0x6722) + 0x783b) != '\0') {
//             piVar20[0x27] = piVar20[0x27] + -1;
//             if (piVar20[0x27] < 1) {
//               piVar20[0x27] = 5;
//             }
//             piVar20[0x29] = 0;
//             *(undefined1 *)(*(byte *)(local_4 * 7 + 0x6722) + 0x783b) = 0;
//             *local_2e = piVar20[3];
//             piVar20[1] = piVar20[5];
//           }
//           if (*(char *)(*(byte *)(local_4 * 7 + 0x6723) + 0x783b) != '\0') {
//             piVar20[0x27] = piVar20[0x27] + 1;
//             if (5 < piVar20[0x27]) {
//               piVar20[0x27] = 1;
//             }
//             piVar20[0x29] = 0;
//             *(undefined1 *)(*(byte *)(local_4 * 7 + 0x6723) + 0x783b) = 0;
//             *local_2e = piVar20[3];
//             piVar20[1] = piVar20[5];
//           }
//         }
//       }
//       uVar15 = piVar20[0x28];
//       if ((((int)uVar15 >> 0xf < 0) ||
//           ((-1 < (int)uVar15 && (uVar15 < *(uint *)(local_4 * 2 + 0x66e8) >> 2)))) &&
//          (iVar16 = FUN_24dd_4654(piVar20[0x28] + 6), iVar16 == 0)) {
//         if (((*(char *)0x4b8 != '\0') && (iVar16 = FUN_24dd_4654(3), iVar16 == 0)) &&
//            (cVar7 = FUN_235c_0a1e(*(undefined1 *)(local_4 + 0x4b6)), cVar7 == '\0')) {
//           iVar16 = FUN_24dd_4654(3);
//           iVar21 = (iVar16 + 0x13) * 4;
//           FUN_235c_095c(0,CONCAT11((char)((uint)(iVar16 + 0x13) >> 8),
//                                    *(undefined1 *)(local_4 + 0x4b6)),
//                         *(undefined2 *)(iVar21 + 0x6734),*(undefined2 *)(iVar21 + 0x6736));
//         }
//         FUN_202c_14b6(piVar20[0x1a],piVar20[0x1b],piVar20[0x18],piVar20[0x19],piVar20[5],piVar20[3],
//                       0,7);
//       }
//       if (piVar20[0x28] < 1) {
//         if (*(char *)((int)piVar20 + 0x95) != '\0') {
//           if (local_4 == 0) {
//             local_8._0_1_ = 0x16;
//           }
//           else {
//             local_8._0_1_ = 0x15;
//           }
//           FUN_202c_14b6(piVar20[0x1a],piVar20[0x1b],piVar20[0x18],piVar20[0x19],piVar20[5],
//                         piVar20[3],0,(undefined1)local_8);
//           *(undefined1 *)((int)piVar20 + 0x95) = 0;
//         }
//         *(bool *)0x651e = *(byte *)0x651f != local_4;
//         if (*(char *)0x651e != '\0') {
//           *(undefined1 *)0x651f = (undefined1)local_4;
//         }
//         piVar20[0x25] = 0;
//         *(undefined1 *)((int)*(undefined4 *)0x6670 + (local_4 ^ 1) * 0xaa + 0x97) = 0;
//         *(undefined1 *)(local_4 + 0x652c) = 0xf8;
//         if (*(char *)0x4b8 != '\0') {
//           if ((*(byte *)(*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) + 0xb8d) & 1) == 1) {
//             FUN_235c_09eb(CONCAT11((char)((uint)(piVar20[0x27] * 2) >> 8),
//                                    *(undefined1 *)
//                                     (*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) + 0xb65)));
//           }
//           iVar16 = FUN_24dd_4654(3);
//           iVar16 = (iVar16 + 0x10) * 4;
//           FUN_235c_095c(0,0x10,*(undefined2 *)(iVar16 + 0x6734),*(undefined2 *)(iVar16 + 0x6736));
//         }
//         *(undefined1 *)((int)piVar20 + 0x99) = 0;
//         *(undefined1 *)(piVar20 + 0x4e) = 0;
//         piVar2 = piVar20 + 0x1c;
//         iVar16 = *piVar2;
//         *piVar2 = *piVar2 + -1;
//         piVar20[0x1d] = piVar20[0x1d] - (uint)(iVar16 == 0);
//         if ((char)piVar20[0x4b] != '\0') {
//           uVar24 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
//           iVar16 = (int)*(undefined4 *)0x6670 + (local_4 ^ 1) * 0xaa;
//           puVar1 = (uint *)(iVar16 + 0x3c);
//           uVar15 = *puVar1;
//           *puVar1 = *puVar1 + 1;
//           piVar2 = (int *)(iVar16 + 0x3e);
//           *piVar2 = *piVar2 + (uint)(0xfffe < uVar15);
//         }
//         *(undefined1 *)(piVar20 + 0x4d) = 0;
//         piVar20[0x26] = 0x96;
//         iVar16 = (*(int *)0x6e * *(int *)0x66aa) / 100;
//         if (0 < iVar16) {
//           local_c = 1;
//           while( true ) {
//             uVar33 = 7;
//             uVar30 = 0;
//             iVar21 = piVar20[3];
//             iVar13 = piVar20[5];
//             iVar14 = piVar20[0x19];
//             uVar24 = FUN_24dd_3dbd(iVar13,iVar21,0,7);
//             iVar22 = piVar20[0x1b];
//             uVar31 = FUN_24dd_3dbd(uVar24,iVar14);
//             uVar11 = FUN_24dd_4654(0x80);
//             FUN_202c_165d(uVar11,uVar31,iVar22,uVar24,iVar14,iVar13,iVar21,uVar30,uVar33);
//             if (local_c == iVar16) break;
//             local_c = local_c + 1;
//           }
//         }
//         local_c = 0;
//         while( true ) {
//           iVar22 = local_4 + 1;
//           uVar11 = 0;
//           iVar16 = piVar20[3];
//           iVar21 = piVar20[5];
//           iVar13 = piVar20[0x19];
//           uVar24 = FUN_24dd_3dbd(iVar21,iVar16,0,iVar22);
//           iVar14 = piVar20[0x1b];
//           uVar31 = FUN_24dd_3dbd(uVar24,iVar13);
//           iVar12 = FUN_24dd_4654(0xe);
//           FUN_202c_165d(local_c * 0xe + 7 + iVar12,uVar31,iVar14,uVar24,iVar13,iVar21,iVar16,uVar11,
//                         iVar22);
//           if (local_c == 7) break;
//           local_c = local_c + 1;
//         }
//         uVar15 = FUN_24dd_4654(100);
//         if (uVar15 < 0x33) {
//           piVar20[0x2b] = 0x60;
//         }
//         else {
//           piVar20[0x2b] = 0x20;
//         }
//         if (piVar20[0x2b] < 0x21) {
//           *(undefined1 *)((int)piVar20 + 0x9b) = 0;
//         }
//         else {
//           *(undefined1 *)((int)piVar20 + 0x9b) = 1;
//         }
//         *(undefined1 *)(*(byte *)(local_4 * 7 + 0x6724) + 0x783b) = 0;
//       }
//     }
//   }
//   if (*(char *)(local_4 + 0x66a7) != '\0') {
//     uVar15 = local_4 ^ 1;
//     if ((*(int *)(*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) * 2 + 0x1014) < 1) ||
//        (499 < *(int *)(*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) * 2 + 0x1014))) {
//       local_12 = *(int *)(*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) * 2 + 0xbdc) -
//                  *(int *)(*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) * 2 + 0xac4) / 10;
//     }
//     else {
//       local_12 = (int)(*(int *)(*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) * 2 + 0xbdc) *
//                       (*(int *)(*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) * 2 + 0x1014) -
//                       (*(uint *)(*(int *)((int)piVar20 + piVar20[0x27] * 2 + 0x73) * 2 + 0x1064) >>
//                       1))) / 0x82;
//     }
//     if (local_12 < 0x5a) {
//       local_12 = 0x5a;
//     }
//     iVar16 = *(int *)((int)*(undefined4 *)0x6670 + uVar15 * 0xaa + 6);
//     iVar21 = *(int *)((int)*(undefined4 *)0x6670 + uVar15 * 0xaa + 10);
//     iVar16 = FUN_202c_0000(iVar21,iVar21 >> 0xf,iVar16,iVar16 >> 0xf,piVar20[5],piVar20[5] >> 0xf,
//                            piVar20[3],piVar20[3] >> 0xf);
//     if ((local_12 < iVar16) && ((char)piVar20[0x4d] != '\0')) {
//       *(undefined1 *)(*(byte *)(local_4 * 7 + 0x6724) + 0x783b) = 0;
//     }
//     else {
//       iVar21 = FUN_24dd_4654(*(undefined2 *)
//                               (*(char *)(*(byte *)(local_4 * 7 + 0x6724) + 0x783b) * 0xe + 0x78));
//       if (iVar21 == 0) {
//         *(bool *)(*(byte *)(local_4 * 7 + 0x6724) + 0x783b) =
//              *(char *)(*(byte *)(local_4 * 7 + 0x6724) + 0x783b) == '\0';
//       }
//     }
//     local_6 = 5;
//     while( true ) {
//       iVar21 = FUN_24dd_4654(*(undefined2 *)
//                               (*(char *)(*(byte *)(local_4 * 7 + local_6 + 0x6720) + 0x783b) * 0xe +
//                                local_6 * 2 + 0x70));
//       if (iVar21 == 0) {
//         *(bool *)(*(byte *)(local_4 * 7 + local_6 + 0x6720) + 0x783b) =
//              *(char *)(*(byte *)(local_4 * 7 + local_6 + 0x6720) + 0x783b) == '\0';
//       }
//       if (local_6 == 6) break;
//       local_6 = local_6 + 1;
//     }
//     uVar17 = *(int *)((int)*(undefined4 *)0x6670 + uVar15 * 0xaa + 6) - piVar20[3];
//     uVar18 = *(int *)((int)*(undefined4 *)0x6670 + uVar15 * 0xaa + 10) - piVar20[5];
//     uVar24 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
//     iVar21 = (int)*(undefined4 *)0x6670 + uVar15 * 0xaa;
//     local_1e = (*(int *)(iVar21 + 6) - piVar20[3]) -
//                (uint)(*(uint *)(iVar21 + 4) < (uint)piVar20[2]);
//     uVar24 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
//     iVar21 = (int)*(undefined4 *)0x6670 + uVar15 * 0xaa;
//     local_22 = (*(int *)(iVar21 + 10) - piVar20[5]) -
//                (uint)(*(uint *)(iVar21 + 8) < (uint)piVar20[4]);
//     if (iVar16 < 1) {
//       local_20 = 0;
//       local_1e = 0;
//       local_24 = 0;
//       local_22 = 0;
//     }
//     else {
//       local_20 = FUN_24dd_3dbd();
//       local_24 = FUN_24dd_3dbd();
//     }
//     local_8 = 0;
//     while (local_8 = local_8 + 1, (int)local_8 < 0x80) {
//       uVar15 = *(uint *)(local_8 * 8 + 0x159e);
//       uVar19 = uVar15 - local_20;
//       uVar15 = (*(int *)(local_8 * 8 + 0x15a0) - local_1e) - (uint)(uVar15 < local_20);
//       if ((int)uVar15 < 0) {
//         bVar25 = uVar19 != 0;
//         uVar19 = -uVar19;
//         uVar15 = (~uVar15 + 1) - (uint)bVar25;
//       }
//       if (((int)uVar15 < 0) || (((int)uVar15 < 1 && (uVar19 < 0xc00)))) {
//         uVar15 = *(uint *)(local_8 * 8 + 0x15a2);
//         uVar19 = uVar15 - local_24;
//         uVar15 = (*(int *)(local_8 * 8 + 0x15a4) - local_22) - (uint)(uVar15 < local_24);
//         if ((int)uVar15 < 0) {
//           bVar25 = uVar19 != 0;
//           uVar19 = -uVar19;
//           uVar15 = (~uVar15 + 1) - (uint)bVar25;
//         }
//         if (((int)uVar15 < 0) || (((int)uVar15 < 1 && (uVar19 < 0xc00)))) break;
//       }
//     }
//     if ((local_8 == 0) || (local_8 == 0x80)) {
//       uVar15 = (int)uVar18 >> 0xf;
//       uVar19 = (int)uVar17 >> 0xf;
//       if ((int)uVar17 < 1) {
//         if ((int)uVar18 < 0) {
//           if ((int)((uVar17 ^ uVar19) - uVar19) < (int)((uVar18 ^ uVar15) - uVar15)) {
//             iVar21 = FUN_24dd_4654(0x10);
//             local_8 = iVar21 + 0x30;
//           }
//           if ((int)((uVar18 ^ uVar15) - uVar15) < (int)((uVar17 ^ uVar19) - uVar19)) {
//             iVar21 = FUN_24dd_4654(0x10);
//             local_8 = iVar21 + 0x20;
//           }
//           if ((uVar17 ^ uVar19) - uVar19 == (uVar18 ^ uVar15) - uVar15) {
//             local_8 = 0x38;
//           }
//         }
//         else {
//           if ((int)((uVar18 ^ uVar15) - uVar15) < (int)((uVar17 ^ uVar19) - uVar19)) {
//             iVar21 = FUN_24dd_4654(0x10);
//             local_8 = iVar21 + 0xc;
//           }
//           if ((int)((uVar17 ^ uVar19) - uVar19) <= (int)((uVar18 ^ uVar15) - uVar15)) {
//             local_8 = 0xc;
//           }
//         }
//       }
//       else if ((int)uVar18 < 0) {
//         if ((int)((uVar17 ^ uVar19) - uVar19) < (int)((uVar18 ^ uVar15) - uVar15)) {
//           iVar21 = FUN_24dd_4654(0x10);
//           local_8 = iVar21 + 0x40;
//         }
//         if ((int)((uVar18 ^ uVar15) - uVar15) < (int)((uVar17 ^ uVar19) - uVar19)) {
//           iVar21 = FUN_24dd_4654(0x10);
//           local_8 = iVar21 + 0x50;
//         }
//         if ((uVar17 ^ uVar19) - uVar19 == (uVar18 ^ uVar15) - uVar15) {
//           local_8 = 0x50;
//         }
//       }
//       else {
//         if ((int)((uVar18 ^ uVar15) - uVar15) < (int)((uVar17 ^ uVar19) - uVar19)) {
//           iVar21 = FUN_24dd_4654(0x10);
//           local_8 = iVar21 + 0x60;
//         }
//         if ((int)((uVar17 ^ uVar19) - uVar19) <= (int)((uVar18 ^ uVar15) - uVar15)) {
//           local_8 = 0x74;
//         }
//       }
//     }
//     while (iVar16 < local_12) {
//       if (0x3f < (int)local_8) goto LAB_1000_39f7;
//       pcVar4 = (code *)swi(0x3b);
//       uVar24 = (*pcVar4)();
//       if ('\0' < (char)((byte)uVar24 | (byte)((uint)uVar24 >> 8))) {
//         pcVar4 = (code *)swi(0x3b);
//         (*pcVar4)();
//         pcVar4 = (code *)swi(0x3b);
//         uVar9 = (*pcVar4)();
//         out(extraout_DX,uVar9);
//         pcVar4 = (code *)swi(0x3b);
//         (*pcVar4)();
//                     /* WARNING: Bad instruction - Truncating control flow here */
//         halt_baddata();
//       }
//     }
//     goto LAB_1000_3a56;
//   }
//   goto LAB_1000_3d2e;
// LAB_1000_39f7:
//   while (0x40 < (int)local_8) {
//     pcVar4 = (code *)swi(0x3b);
//     uVar24 = (*pcVar4)();
//     if ('\0' < (char)((byte)uVar24 | (byte)((uint)uVar24 >> 8))) {
//       pcVar4 = (code *)swi(0x3b);
//       (*pcVar4)();
//       pcVar4 = (code *)swi(0x3b);
//       uVar9 = (*pcVar4)();
//       out(extraout_DX_00,uVar9);
//       pcVar4 = (code *)swi(0x3b);
//       (*pcVar4)();
//                     /* WARNING: Bad instruction - Truncating control flow here */
//       halt_baddata();
//     }
//     if (0x40 < (int)local_8) {
//       local_8 = 0x40;
//     }
//   }
// LAB_1000_3a56:
//   if (*(char *)(*(byte *)(local_4 * 7 + 0x6725) + 0x783b) == '\0') {
//     if ((local_12 < iVar16) && (-1 < (int)uVar17)) {
//       uVar9 = 1;
//     }
//     else {
//       uVar9 = 0;
//     }
//     *(undefined1 *)(*(byte *)(local_4 * 7 + 0x6723) + 0x783b) = uVar9;
//     if ((local_12 < iVar16) && ((int)uVar17 < 1)) {
//       uVar9 = 1;
//     }
//     else {
//       uVar9 = 0;
//     }
//     *(undefined1 *)(*(byte *)(local_4 * 7 + 0x6722) + 0x783b) = uVar9;
//     if (*(char *)((int)piVar20 + 0x9b) == '\0') {
//       if (0x40 < (int)local_8) {
//         *(undefined1 *)(*(byte *)(local_4 * 7 + 0x6723) + 0x783b) = 1;
//       }
//       *(bool *)(*(byte *)(local_4 * 7 + 0x6720) + 0x783b) = piVar20[0x2b] < (int)(local_8 + -1);
//       *(bool *)(*(byte *)(local_4 * 7 + 0x6721) + 0x783b) = (int)(local_8 + 1) < piVar20[0x2b];
//     }
//     else {
//       if ((int)local_8 < 0x40) {
//         *(undefined1 *)(*(byte *)(local_4 * 7 + 0x6722) + 0x783b) = 1;
//       }
//       *(bool *)(*(byte *)(local_4 * 7 + 0x6720) + 0x783b) = (int)(local_8 + 1) < piVar20[0x2b];
//       *(bool *)(*(byte *)(local_4 * 7 + 0x6721) + 0x783b) = piVar20[0x2b] < (int)(local_8 + -1);
//     }
//     if ((*(char *)(*(byte *)(local_4 * 7 + 0x6722) + 0x783b) != '\0') &&
//        (*(char *)((int)piVar20 + 0xa5) != '\0')) {
//       if ((char)piVar20[0x51] == '\0') {
//         *(undefined1 *)(*(byte *)(local_4 * 7 + 0x6726) + 0x783b) = 1;
//       }
//       else {
//         *(undefined1 *)(*(byte *)(local_4 * 7 + 0x6723) + 0x783b) = 1;
//       }
//     }
//     if ((*(char *)(*(byte *)(local_4 * 7 + 0x6723) + 0x783b) != '\0') &&
//        (*(char *)((int)piVar20 + 0xa3) != '\0')) {
//       if ((char)piVar20[0x51] == '\0') {
//         *(undefined1 *)(*(byte *)(local_4 * 7 + 0x6726) + 0x783b) = 1;
//       }
//       else {
//         *(undefined1 *)(*(byte *)(local_4 * 7 + 0x6722) + 0x783b) = 1;
//       }
//     }
//   }
//   else {
//     local_6 = 2;
//     while( true ) {
//       iVar16 = FUN_24dd_4654(*(undefined2 *)
//                               (*(char *)(*(byte *)(local_4 * 7 + local_6 + 0x6720) + 0x783b) * 0xe +
//                                local_6 * 2 + 0x70));
//       if (iVar16 == 0) {
//         *(bool *)(*(byte *)(local_4 * 7 + local_6 + 0x6720) + 0x783b) =
//              *(char *)(*(byte *)(local_4 * 7 + local_6 + 0x6720) + 0x783b) == '\0';
//       }
//       if (local_6 == 3) break;
//       local_6 = local_6 + 1;
//     }
//     if (((char)piVar20[0x4e] == '\0') || ((char)piVar20[6] == '\0')) {
//       for (local_6 = 0; *(undefined1 *)(*(byte *)(local_4 * 7 + local_6 + 0x6720) + 0x783b) = 0,
//           local_6 != 1; local_6 = local_6 + 1) {
//       }
//     }
//     else {
//       local_6 = 0;
//       while( true ) {
//         iVar16 = FUN_24dd_4654(*(undefined2 *)
//                                 (*(char *)(*(byte *)(local_4 * 7 + local_6 + 0x6720) + 0x783b) * 0xe
//                                  + local_6 * 2 + 0x70));
//         if (iVar16 == 0) {
//           *(bool *)(*(byte *)(local_4 * 7 + local_6 + 0x6720) + 0x783b) =
//                *(char *)(*(byte *)(local_4 * 7 + local_6 + 0x6720) + 0x783b) == '\0';
//         }
//         if (local_6 == 1) break;
//         local_6 = local_6 + 1;
//       }
//     }
//   }
// LAB_1000_3d2e:
//   if (local_4 == 1) {
//     return;
//   }
//   local_4 = local_4 + 1;
//   goto LAB_1000_1104;
// }
// 
// --- end reference ---
procedure FUN_1000_10ec;
begin
  { TODO: translate from asm/FUN_1000_10ec.s — UNMATCHED until an oracle passes }
end;

