{ liero::FUN_1000_8c03 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_8c03.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_8c03.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_1000_8c03(void)
// 
// {
//   uint *puVar1;
//   int *piVar2;
//   uint uVar3;
//   int iVar4;
//   undefined1 uVar5;
//   byte bVar6;
//   uint uVar7;
//   int iVar8;
//   int iVar9;
//   int iVar10;
//   int iVar11;
//   int iVar12;
//   undefined2 uVar13;
//   undefined2 uVar14;
//   undefined2 uVar15;
//   undefined2 unaff_DS;
//   undefined4 uVar16;
//   undefined2 uVar17;
//   undefined2 uVar18;
//   undefined2 uVar19;
//   undefined2 uVar20;
//   undefined2 uVar21;
//   undefined4 uVar22;
//   uint local_c;
//   uint local_8;
//   uint local_6;
//   uint local_4;
//   
//   local_4 = 0x1000;
//   FUN_24dd_0530();
//   local_6 = 0;
//   while( true ) {
//     if (*(char *)((int)*(undefined4 *)0x6670 + local_6 * 0xaa + 0x9c) != '\0') {
//       uVar13 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
//       iVar11 = (int)*(undefined4 *)0x6670 + local_6 * 0xaa;
//       uVar22 = CONCAT22(uVar13,iVar11);
//       uVar3 = *(uint *)(iVar11 + 0x16);
//       iVar10 = *(int *)(iVar11 + 0x18);
//       puVar1 = (uint *)(iVar11 + 0xe);
//       uVar7 = *puVar1;
//       *puVar1 = *puVar1 + uVar3;
//       *(int *)(iVar11 + 0x10) = *(int *)(iVar11 + 0x10) + iVar10 + (uint)CARRY2(uVar7,uVar3);
//       uVar3 = *(uint *)(iVar11 + 0x1a);
//       iVar10 = *(int *)(iVar11 + 0x1c);
//       puVar1 = (uint *)(iVar11 + 0x12);
//       uVar7 = *puVar1;
//       *puVar1 = *puVar1 + uVar3;
//       *(int *)(iVar11 + 0x14) = *(int *)(iVar11 + 0x14) + iVar10 + (uint)CARRY2(uVar7,uVar3);
//       uVar5 = FUN_1000_0d70(*(undefined2 *)(iVar11 + 0x14),*(undefined2 *)(iVar11 + 0x10),1,
//                             local_6 ^ 1);
//       *(undefined1 *)((int)uVar22 + 0xd) = uVar5;
//       iVar10 = 0x20;
//       bVar6 = FUN_24dd_4161();
//       iVar11 = (int)uVar22;
//       uVar13 = (undefined2)((ulong)uVar22 >> 0x10);
//       if (((((*(byte *)(iVar10 + 0x6604) & bVar6) == 0) && (0 < *(int *)(iVar11 + 0x10))) &&
//           (*(int *)(iVar11 + 0x10) < 0x1f7)) &&
//          ((0 < *(int *)(iVar11 + 0x14) && (*(int *)(iVar11 + 0x14) < 0x15d)))) {
//         if (*(char *)(iVar11 + 0xd) == '\0') {
//           *(undefined1 *)(iVar11 + 0xc) = 0;
//         }
//         else {
//           local_4 = local_6 ^ 1;
//           uVar15 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
//           iVar10 = (int)*(undefined4 *)0x6670 + local_4 * 0xaa;
//           local_c = (*(int *)(iVar10 + 6) - *(int *)(iVar11 + 6)) -
//                     (uint)(*(uint *)(iVar10 + 4) < *(uint *)(iVar11 + 4));
//           FUN_24dd_3e7c();
//           iVar8 = FUN_24dd_3dbd();
//           uVar13 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
//           iVar10 = (int)*(undefined4 *)0x6670 + local_4 * 0xaa;
//           uVar15 = (undefined2)((ulong)uVar22 >> 0x10);
//           local_8 = (*(int *)(iVar10 + 10) - *(int *)((int)uVar22 + 10)) -
//                     (uint)(*(uint *)(iVar10 + 8) < *(uint *)((int)uVar22 + 8));
//           FUN_24dd_3e7c();
//           iVar9 = FUN_24dd_3dbd();
//           iVar10 = *(int *)((int)*(undefined4 *)0x6670 + local_4 * 0xaa + 6);
//           iVar11 = *(int *)((int)*(undefined4 *)0x6670 + local_4 * 0xaa + 10);
//           uVar13 = (undefined2)((ulong)uVar22 >> 0x10);
//           iVar12 = *(int *)((int)uVar22 + 6);
//           iVar4 = *(int *)((int)uVar22 + 10);
//           uVar16 = FUN_202c_0000(iVar4,iVar4 >> 0xf,iVar12,iVar12 >> 0xf,iVar11,iVar11 >> 0xf,iVar10
//                                  ,iVar10 >> 0xf);
//           iVar10 = (int)((ulong)uVar16 >> 0x10) + (uint)(0xfffe < (uint)uVar16);
//           uVar13 = FUN_24dd_3e7c();
//           uVar15 = (undefined2)((ulong)uVar22 >> 0x10);
//           iVar11 = (int)uVar22;
//           *(undefined2 *)(iVar11 + 0x2a) = uVar13;
//           *(int *)(iVar11 + 0x2c) = iVar10;
//           if (*(char *)(iVar11 + 0xc) == '\0') {
//             *(undefined2 *)(iVar11 + 0x2e) = 0;
//             *(undefined2 *)(iVar11 + 0x26) = 0x1c2;
//             *(undefined2 *)(iVar11 + 0x28) = 0;
//             *(undefined1 *)(iVar11 + 0xc) = 1;
//           }
//           iVar10 = (~local_c + 1) - (uint)(iVar8 != 0);
//           uVar13 = FUN_24dd_3dbd();
//           uVar15 = (undefined2)((ulong)uVar22 >> 0x10);
//           *(undefined2 *)((int)uVar22 + 0x1e) = uVar13;
//           *(int *)((int)uVar22 + 0x20) = iVar10;
//           iVar10 = (~local_8 + 1) - (uint)(iVar9 != 0);
//           uVar13 = FUN_24dd_3dbd();
//           uVar15 = (undefined2)((ulong)uVar22 >> 0x10);
//           iVar11 = (int)uVar22;
//           *(undefined2 *)(iVar11 + 0x22) = uVar13;
//           *(int *)(iVar11 + 0x24) = iVar10;
//           if ((*(int *)(iVar11 + 0x28) < *(int *)(iVar11 + 0x2c)) ||
//              ((*(int *)(iVar11 + 0x28) <= *(int *)(iVar11 + 0x2c) &&
//               (*(uint *)(iVar11 + 0x26) < *(uint *)(iVar11 + 0x2a))))) {
//             uVar3 = *(uint *)(iVar11 + 0x1e);
//             iVar10 = *(int *)(iVar11 + 0x20);
//             uVar13 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
//             iVar12 = (int)*(undefined4 *)0x6670 + local_4 * 0xaa;
//             puVar1 = (uint *)(iVar12 + 0x30);
//             uVar7 = *puVar1;
//             *puVar1 = *puVar1 + uVar3;
//             piVar2 = (int *)(iVar12 + 0x32);
//             *piVar2 = *piVar2 + iVar10 + (uint)CARRY2(uVar7,uVar3);
//             uVar3 = *(uint *)(iVar11 + 0x22);
//             iVar10 = *(int *)(iVar11 + 0x24);
//             uVar13 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
//             iVar12 = (int)*(undefined4 *)0x6670 + local_4 * 0xaa;
//             puVar1 = (uint *)(iVar12 + 0x34);
//             uVar7 = *puVar1;
//             *puVar1 = *puVar1 + uVar3;
//             piVar2 = (int *)(iVar12 + 0x36);
//             *piVar2 = *piVar2 + iVar10 + (uint)CARRY2(uVar7,uVar3);
//           }
//           uVar14 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
//           iVar10 = (int)*(undefined4 *)0x6670 + local_4 * 0xaa;
//           uVar13 = *(undefined2 *)(iVar10 + 0x32);
//           *(undefined2 *)(iVar11 + 0x16) = *(undefined2 *)(iVar10 + 0x30);
//           *(undefined2 *)(iVar11 + 0x18) = uVar13;
//           uVar14 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
//           iVar10 = (int)*(undefined4 *)0x6670 + local_4 * 0xaa;
//           uVar13 = *(undefined2 *)(iVar10 + 0x36);
//           *(undefined2 *)(iVar11 + 0x1a) = *(undefined2 *)(iVar10 + 0x34);
//           *(undefined2 *)(iVar11 + 0x1c) = uVar13;
//           *(undefined2 *)(iVar11 + 0x10) =
//                *(undefined2 *)((int)*(undefined4 *)0x6670 + local_4 * 0xaa + 6);
//           *(undefined2 *)(iVar11 + 0x14) =
//                *(undefined2 *)((int)*(undefined4 *)0x6670 + local_4 * 0xaa + 10);
//         }
//       }
//       else {
//         local_c = (*(int *)(iVar11 + 0x10) - *(int *)(iVar11 + 6)) -
//                   (uint)(*(uint *)(iVar11 + 0xe) < *(uint *)(iVar11 + 4));
//         FUN_24dd_3e7c();
//         uVar13 = FUN_24dd_3dbd();
//         uVar15 = (undefined2)((ulong)uVar22 >> 0x10);
//         iVar10 = (int)uVar22;
//         local_8 = (*(int *)(iVar10 + 0x14) - *(int *)(iVar10 + 10)) -
//                   (uint)(*(uint *)(iVar10 + 0x12) < *(uint *)(iVar10 + 8));
//         FUN_24dd_3e7c(uVar22,uVar13);
//         FUN_24dd_3dbd();
//         uVar13 = (undefined2)((ulong)uVar22 >> 0x10);
//         iVar10 = (int)uVar22;
//         uVar16 = FUN_202c_0000(*(int *)(iVar10 + 10),*(int *)(iVar10 + 10) >> 0xf,
//                                *(int *)(iVar10 + 6),*(int *)(iVar10 + 6) >> 0xf,
//                                *(int *)(iVar10 + 0x14),*(int *)(iVar10 + 0x14) >> 0xf,
//                                *(int *)(iVar10 + 0x10),*(int *)(iVar10 + 0x10) >> 0xf);
//         iVar10 = (int)((ulong)uVar16 >> 0x10) + (uint)(0xfffe < (uint)uVar16);
//         uVar13 = FUN_24dd_3e7c();
//         uVar15 = (undefined2)((ulong)uVar22 >> 0x10);
//         iVar11 = (int)uVar22;
//         *(undefined2 *)(iVar11 + 0x2a) = uVar13;
//         *(int *)(iVar11 + 0x2c) = iVar10;
//         if (*(char *)(iVar11 + 0xc) == '\0') {
//           *(undefined2 *)(iVar11 + 0x2e) = 0;
//           *(undefined2 *)(iVar11 + 0x26) = 0x1c2;
//           *(undefined2 *)(iVar11 + 0x28) = 0;
//           iVar10 = 0x20;
//           bVar6 = FUN_24dd_4161();
//           if ((*(byte *)(iVar10 + 0x6624) & bVar6) != 0) {
//             local_4 = 0;
//             while( true ) {
//               uVar21 = 3;
//               uVar15 = (undefined2)((ulong)uVar22 >> 0x10);
//               iVar10 = (int)uVar22;
//               uVar16 = *(undefined4 *)((int)*(undefined4 *)0x6674 + *(int *)(iVar10 + 0x14) * 4);
//               uVar7 = (uint)*(byte *)((int)uVar16 + *(int *)(iVar10 + 0x10));
//               uVar13 = *(undefined2 *)(iVar10 + 0x10);
//               uVar15 = *(undefined2 *)(iVar10 + 0x14);
//               uVar20 = 0;
//               uVar19 = 0;
//               uVar18 = 0;
//               uVar17 = 0;
//               uVar14 = FUN_24dd_4654(0x80);
//               FUN_202c_165d(uVar14,uVar17,uVar18,uVar19,uVar20,uVar15,uVar13,uVar7,uVar21);
//               if (local_4 == 10) break;
//               local_4 = local_4 + 1;
//             }
//           }
//         }
//         uVar13 = (undefined2)((ulong)uVar22 >> 0x10);
//         iVar10 = (int)uVar22;
//         *(undefined1 *)(iVar10 + 0xc) = 1;
//         *(undefined2 *)(iVar10 + 0x16) = 0;
//         *(undefined2 *)(iVar10 + 0x18) = 0;
//         *(undefined2 *)(iVar10 + 0x1a) = 0;
//         *(undefined2 *)(iVar10 + 0x1c) = 0;
//       }
//       uVar13 = (undefined2)((ulong)uVar22 >> 0x10);
//       iVar10 = (int)uVar22;
//       if (*(char *)(iVar10 + 0xc) == '\0') {
//         puVar1 = (uint *)(iVar10 + 0x1a);
//         uVar7 = *puVar1;
//         *puVar1 = *puVar1 + 1000;
//         *(int *)(iVar10 + 0x1c) = *(int *)(iVar10 + 0x1c) + (uint)(0xfc17 < uVar7);
//         local_c = (*(int *)(iVar10 + 0x10) - *(int *)(iVar10 + 6)) -
//                   (uint)(*(uint *)(iVar10 + 0xe) < *(uint *)(iVar10 + 4));
//         FUN_24dd_3e7c();
//         iVar10 = FUN_24dd_3dbd();
//         uVar13 = (undefined2)((ulong)uVar22 >> 0x10);
//         iVar11 = (int)uVar22;
//         local_8 = (*(int *)(iVar11 + 0x14) - *(int *)(iVar11 + 10)) -
//                   (uint)(*(uint *)(iVar11 + 0x12) < *(uint *)(iVar11 + 8));
//         FUN_24dd_3e7c();
//         iVar11 = FUN_24dd_3dbd();
//         uVar13 = (undefined2)((ulong)uVar22 >> 0x10);
//         iVar12 = (int)uVar22;
//         uVar16 = FUN_202c_0000(*(int *)(iVar12 + 10),*(int *)(iVar12 + 10) >> 0xf,
//                                *(int *)(iVar12 + 6),*(int *)(iVar12 + 6) >> 0xf,
//                                *(int *)(iVar12 + 0x14),*(int *)(iVar12 + 0x14) >> 0xf,
//                                *(int *)(iVar12 + 0x10),*(int *)(iVar12 + 0x10) >> 0xf);
//         iVar12 = (int)((ulong)uVar16 >> 0x10) + (uint)(0xfffe < (uint)uVar16);
//         uVar13 = FUN_24dd_3e7c();
//         uVar15 = (undefined2)((ulong)uVar22 >> 0x10);
//         *(undefined2 *)((int)uVar22 + 0x2a) = uVar13;
//         *(int *)((int)uVar22 + 0x2c) = iVar12;
//         iVar10 = (~local_c + 1) - (uint)(iVar10 != 0);
//         uVar13 = FUN_24dd_3dbd();
//         uVar15 = (undefined2)((ulong)uVar22 >> 0x10);
//         *(undefined2 *)((int)uVar22 + 0x1e) = uVar13;
//         *(int *)((int)uVar22 + 0x20) = iVar10;
//         iVar10 = (~local_8 + 1) - (uint)(iVar11 != 0);
//         uVar13 = FUN_24dd_3dbd();
//         uVar15 = (undefined2)((ulong)uVar22 >> 0x10);
//         iVar11 = (int)uVar22;
//         *(undefined2 *)(iVar11 + 0x22) = uVar13;
//         *(int *)(iVar11 + 0x24) = iVar10;
//         if ((*(int *)(iVar11 + 0x28) < *(int *)(iVar11 + 0x2c)) ||
//            ((*(int *)(iVar11 + 0x28) <= *(int *)(iVar11 + 0x2c) &&
//             (*(uint *)(iVar11 + 0x26) < *(uint *)(iVar11 + 0x2a))))) {
//           uVar3 = *(uint *)(iVar11 + 0x1e);
//           iVar10 = *(int *)(iVar11 + 0x20);
//           puVar1 = (uint *)(iVar11 + 0x16);
//           uVar7 = *puVar1;
//           *puVar1 = *puVar1 + uVar3;
//           *(int *)(iVar11 + 0x18) = *(int *)(iVar11 + 0x18) + iVar10 + (uint)CARRY2(uVar7,uVar3);
//           uVar3 = *(uint *)(iVar11 + 0x22);
//           iVar10 = *(int *)(iVar11 + 0x24);
//           puVar1 = (uint *)(iVar11 + 0x1a);
//           uVar7 = *puVar1;
//           *puVar1 = *puVar1 + uVar3;
//           *(int *)(iVar11 + 0x1c) = *(int *)(iVar11 + 0x1c) + iVar10 + (uint)CARRY2(uVar7,uVar3);
//         }
//       }
//       else {
//         uVar7 = local_c;
//         uVar13 = FUN_24dd_3dbd();
//         uVar15 = (undefined2)((ulong)uVar22 >> 0x10);
//         *(undefined2 *)((int)uVar22 + 0x1e) = uVar13;
//         *(uint *)((int)uVar22 + 0x20) = uVar7;
//         uVar7 = local_8;
//         uVar13 = FUN_24dd_3dbd();
//         uVar15 = (undefined2)((ulong)uVar22 >> 0x10);
//         iVar10 = (int)uVar22;
//         *(undefined2 *)(iVar10 + 0x22) = uVar13;
//         *(uint *)(iVar10 + 0x24) = uVar7;
//         if ((*(int *)(iVar10 + 0x28) < *(int *)(iVar10 + 0x2c)) ||
//            ((*(int *)(iVar10 + 0x28) <= *(int *)(iVar10 + 0x2c) &&
//             (*(uint *)(iVar10 + 0x26) < *(uint *)(iVar10 + 0x2a))))) {
//           uVar3 = *(uint *)(iVar10 + 0x1e);
//           iVar11 = *(int *)(iVar10 + 0x20);
//           puVar1 = (uint *)(iVar10 + 0x30);
//           uVar7 = *puVar1;
//           *puVar1 = *puVar1 + uVar3;
//           *(int *)(iVar10 + 0x32) = *(int *)(iVar10 + 0x32) + iVar11 + (uint)CARRY2(uVar7,uVar3);
//           uVar3 = *(uint *)(iVar10 + 0x22);
//           iVar11 = *(int *)(iVar10 + 0x24);
//           puVar1 = (uint *)(iVar10 + 0x34);
//           uVar7 = *puVar1;
//           *puVar1 = *puVar1 + uVar3;
//           *(int *)(iVar10 + 0x36) = *(int *)(iVar10 + 0x36) + iVar11 + (uint)CARRY2(uVar7,uVar3);
//         }
//         if (*(char *)(iVar10 + 0xd) != '\0') {
//           uVar14 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
//           iVar11 = (int)*(undefined4 *)0x6670 + local_4 * 0xaa;
//           uVar13 = *(undefined2 *)(iVar11 + 0x32);
//           *(undefined2 *)(iVar10 + 0x16) = *(undefined2 *)(iVar11 + 0x30);
//           *(undefined2 *)(iVar10 + 0x18) = uVar13;
//           uVar14 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
//           iVar11 = (int)*(undefined4 *)0x6670 + local_4 * 0xaa;
//           uVar13 = *(undefined2 *)(iVar11 + 0x36);
//           *(undefined2 *)(iVar10 + 0x1a) = *(undefined2 *)(iVar11 + 0x34);
//           *(undefined2 *)(iVar10 + 0x1c) = uVar13;
//           *(undefined2 *)(iVar10 + 0x10) =
//                *(undefined2 *)((int)*(undefined4 *)0x6670 + local_4 * 0xaa + 6);
//           *(undefined2 *)(iVar10 + 0x14) =
//                *(undefined2 *)((int)*(undefined4 *)0x6670 + local_4 * 0xaa + 10);
//         }
//       }
//     }
//     if (local_6 == 1) break;
//     local_6 = local_6 + 1;
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_1000_8c03;
begin
  { TODO: translate from asm/FUN_1000_8c03.s — UNMATCHED until an oracle passes }
end;

