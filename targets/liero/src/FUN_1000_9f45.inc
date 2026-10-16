{ liero::FUN_1000_9f45 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_9f45.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_9f45.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void FUN_1000_9f45(byte param_1)
// 
// {
//   char *pcVar1;
//   uint *puVar2;
//   int *piVar3;
//   undefined4 uVar4;
//   byte bVar5;
//   char cVar6;
//   int iVar7;
//   int iVar8;
//   uint uVar9;
//   int iVar10;
//   int iVar11;
//   int iVar12;
//   undefined2 unaff_DS;
//   undefined2 uVar13;
//   uint local_a;
//   uint local_8;
//   int local_6;
//   uint local_4;
//   
//   FUN_24dd_0530();
//   if (*(char *)0x66af == '\0') {
//     local_8 = 0;
//     while( true ) {
//       local_a = 3;
//       while( true ) {
//         uVar4 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_a * 4);
//         bVar5 = *(byte *)((int)uVar4 + local_8);
//         if ((0xa3 < bVar5) && (bVar5 < 0xa8)) {
//           uVar4 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_a * 4);
//           pcVar1 = (char *)((int)uVar4 + local_8);
//           *pcVar1 = *pcVar1 + -4;
//         }
//         if (local_a == 0x15d) break;
//         local_a = local_a + 1;
//       }
//       if (local_8 == 500) break;
//       local_8 = local_8 + 1;
//     }
//   }
//   else {
//     local_8 = 0;
//     while( true ) {
//       local_a = 3;
//       while( true ) {
//         iVar10 = 0x20;
//         bVar5 = FUN_24dd_4161();
//         if ((*(byte *)(iVar10 + 0x14e0) & bVar5) != 0) {
//           iVar10 = 0x20;
//           bVar5 = FUN_24dd_4161();
//           if ((*(byte *)(iVar10 + 0x6604) & bVar5) != 0) {
//             uVar4 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_a * 4);
//             pcVar1 = (char *)((int)uVar4 + local_8);
//             *pcVar1 = *pcVar1 + '\x04';
//           }
//         }
//         if (local_a == 0x15d) break;
//         local_a = local_a + 1;
//       }
//       if (local_8 == 500) break;
//       local_8 = local_8 + 1;
//     }
//   }
//   local_4 = 0;
//   while( true ) {
//     FUN_1ec2_10cf(0,0,0,local_4 & 0xff);
//     if (local_4 == 0xff) break;
//     local_4 = local_4 + 1;
//   }
//   if (param_1 != 0) {
//     if ((1 < *(byte *)0x66ac) && (*(byte *)0x66ac < 4)) {
//       FUN_1000_0ebe(0xff60,0xff60,0);
//       FUN_1000_0ebe(0xff60,0xff60,1);
//       *(undefined1 *)0x6426 = 1;
//       do {
//         do {
//           iVar10 = FUN_24dd_4654(0x1e7);
//           *(int *)0x6427 = iVar10 + 8;
//           iVar10 = FUN_24dd_4654(0x14d);
//           *(int *)0x642b = iVar10 + 8;
//           cVar6 = FUN_1000_0c7f(0xff60,0xff60,0xff60,0xff60,*(undefined2 *)0x642b,
//                                 *(int *)0x6427 + -6);
//         } while (cVar6 == '\0');
//         cVar6 = FUN_1000_0c7f(0xff60,0xff60,0xff60,0xff60,*(int *)0x642b + -6,*(undefined2 *)0x6427)
//         ;
//       } while (((cVar6 == '\0') ||
//                (cVar6 = FUN_1000_0c7f(0xff60,0xff60,0xff60,0xff60,*(int *)0x642b + 6,
//                                       *(undefined2 *)0x6427), cVar6 == '\0')) ||
//               (cVar6 = FUN_1000_0c7f(0xff60,0xff60,0xff60,0xff60,*(undefined2 *)0x642b,
//                                      *(int *)0x6427 + 6), cVar6 == '\0'));
//       iVar10 = *(int *)0x6427 + -5;
//       iVar12 = *(int *)0x642b + -7;
//       uVar13 = (undefined2)((ulong)*(undefined4 *)0x6678 >> 0x10);
//       iVar11 = (int)*(undefined4 *)0x6678 + (uint)*(byte *)0x136a * 0x100;
//       iVar7 = FUN_24dd_4654(*(undefined1 *)0x137e);
//       iVar8 = ((uint)*(byte *)0x1374 + iVar7) * 0x100;
//       if (*(char *)0x1388 == '\x01') {
//         iVar8 = iVar8 + 1;
//       }
//       FUN_202c_005a(iVar8,(int)*(undefined4 *)0x6678 + ((uint)*(byte *)0x1374 + iVar7) * 0x100,
//                     (int)((ulong)*(undefined4 *)0x6678 >> 0x10),iVar11,uVar13,iVar12,iVar10);
//       iVar10 = *(int *)0x6427 + -9;
//       iVar12 = *(int *)0x642b + -7;
//       uVar13 = (undefined2)((ulong)*(undefined4 *)0x6678 >> 0x10);
//       iVar11 = (int)*(undefined4 *)0x6678 + (uint)*(byte *)0x136a * 0x100;
//       iVar7 = FUN_24dd_4654(*(undefined1 *)0x137e);
//       iVar8 = ((uint)*(byte *)0x1374 + iVar7) * 0x100;
//       if (*(char *)0x1388 == '\x01') {
//         iVar8 = iVar8 + 1;
//       }
//       FUN_202c_005a(iVar8,(int)*(undefined4 *)0x6678 + ((uint)*(byte *)0x1374 + iVar7) * 0x100,
//                     (int)((ulong)*(undefined4 *)0x6678 >> 0x10),iVar11,uVar13,iVar12,iVar10);
//       iVar10 = *(int *)0x6427 + -7;
//       iVar12 = *(int *)0x642b + -5;
//       uVar13 = (undefined2)((ulong)*(undefined4 *)0x6678 >> 0x10);
//       iVar11 = (int)*(undefined4 *)0x6678 + (uint)*(byte *)0x136a * 0x100;
//       iVar7 = FUN_24dd_4654(*(undefined1 *)0x137e);
//       iVar8 = ((uint)*(byte *)0x1374 + iVar7) * 0x100;
//       if (*(char *)0x1388 == '\x01') {
//         iVar8 = iVar8 + 1;
//       }
//       FUN_202c_005a(iVar8,(int)*(undefined4 *)0x6678 + ((uint)*(byte *)0x1374 + iVar7) * 0x100,
//                     (int)((ulong)*(undefined4 *)0x6678 >> 0x10),iVar11,uVar13,iVar12,iVar10);
//       if (*(char *)0x66af != '\0') {
//         iVar10 = *(int *)0x6427;
//         local_8 = *(int *)0x6427 - 0x14;
//         if ((int)local_8 <= (int)(iVar10 + 0x14U)) {
//           do {
//             if ((local_8 < 0x8000) && ((int)local_8 < 0x1f8)) {
//               uVar9 = *(int *)0x642b + 0x14;
//               local_a = *(int *)0x642b - 0x14;
//               if ((int)local_a <= (int)uVar9) {
//                 do {
//                   if ((local_a < 0x8000) && ((int)local_a < 0x15e)) {
//                     iVar12 = 0x20;
//                     bVar5 = FUN_24dd_4161();
//                     if ((*(byte *)(iVar12 + 0x14e0) & bVar5) != 0) {
//                       iVar12 = 0x20;
//                       bVar5 = FUN_24dd_4161();
//                       if ((*(byte *)(iVar12 + 0x6604) & bVar5) != 0) {
//                         uVar4 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_a * 4);
//                         pcVar1 = (char *)((int)uVar4 + local_8);
//                         *pcVar1 = *pcVar1 + '\x04';
//                         goto LAB_1000_a36e;
//                       }
//                     }
//                     uVar4 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_a * 4);
//                     bVar5 = *(byte *)((int)uVar4 + local_8);
//                     if ((0xa3 < bVar5) && (bVar5 < 0xa8)) {
//                       iVar12 = 0x20;
//                       bVar5 = FUN_24dd_4161();
//                       if ((*(byte *)(iVar12 + 0x6604) & bVar5) != 0) {
//                         uVar4 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_a * 4);
//                         pcVar1 = (char *)((int)uVar4 + local_8);
//                         *pcVar1 = *pcVar1 + -4;
//                       }
//                     }
//                   }
// LAB_1000_a36e:
//                   if (local_a == uVar9) break;
//                   local_a = local_a + 1;
//                 } while( true );
//               }
//             }
//             if (local_8 == iVar10 + 0x14U) break;
//             local_8 = local_8 + 1;
//           } while( true );
//         }
//       }
//       *(undefined1 *)0x6431 = 1;
//       do {
//         do {
//           iVar10 = FUN_24dd_4654(0x1e7);
//           *(int *)0x6432 = iVar10 + 8;
//           iVar10 = FUN_24dd_4654(0x14d);
//           *(int *)0x6436 = iVar10 + 8;
//           cVar6 = FUN_1000_0c7f(0xff60,0xff60,0xff60,0xff60,*(undefined2 *)0x6436,
//                                 *(int *)0x6432 + -6);
//         } while (cVar6 == '\0');
//         cVar6 = FUN_1000_0c7f(0xff60,0xff60,0xff60,0xff60,*(int *)0x6436 + -6,*(undefined2 *)0x6432)
//         ;
//       } while (((cVar6 == '\0') ||
//                (cVar6 = FUN_1000_0c7f(0xff60,0xff60,0xff60,0xff60,*(int *)0x6436 + 6,
//                                       *(undefined2 *)0x6432), cVar6 == '\0')) ||
//               (cVar6 = FUN_1000_0c7f(0xff60,0xff60,0xff60,0xff60,*(undefined2 *)0x6436,
//                                      *(int *)0x6432 + 6), cVar6 == '\0'));
//       iVar10 = *(int *)0x6432 + -5;
//       iVar12 = *(int *)0x6436 + -7;
//       uVar13 = (undefined2)((ulong)*(undefined4 *)0x6678 >> 0x10);
//       iVar11 = (int)*(undefined4 *)0x6678 + (uint)*(byte *)0x136a * 0x100;
//       iVar7 = FUN_24dd_4654(*(undefined1 *)0x137e);
//       iVar8 = ((uint)*(byte *)0x1374 + iVar7) * 0x100;
//       if (*(char *)0x1388 == '\x01') {
//         iVar8 = iVar8 + 1;
//       }
//       FUN_202c_005a(iVar8,(int)*(undefined4 *)0x6678 + ((uint)*(byte *)0x1374 + iVar7) * 0x100,
//                     (int)((ulong)*(undefined4 *)0x6678 >> 0x10),iVar11,uVar13,iVar12,iVar10);
//       iVar10 = *(int *)0x6432 + -9;
//       iVar12 = *(int *)0x6436 + -7;
//       uVar13 = (undefined2)((ulong)*(undefined4 *)0x6678 >> 0x10);
//       iVar11 = (int)*(undefined4 *)0x6678 + (uint)*(byte *)0x136a * 0x100;
//       iVar7 = FUN_24dd_4654(*(undefined1 *)0x137e);
//       iVar8 = ((uint)*(byte *)0x1374 + iVar7) * 0x100;
//       if (*(char *)0x1388 == '\x01') {
//         iVar8 = iVar8 + 1;
//       }
//       FUN_202c_005a(iVar8,(int)*(undefined4 *)0x6678 + ((uint)*(byte *)0x1374 + iVar7) * 0x100,
//                     (int)((ulong)*(undefined4 *)0x6678 >> 0x10),iVar11,uVar13,iVar12,iVar10);
//       iVar10 = *(int *)0x6432 + -7;
//       iVar12 = *(int *)0x6436 + -5;
//       uVar13 = (undefined2)((ulong)*(undefined4 *)0x6678 >> 0x10);
//       iVar11 = (int)*(undefined4 *)0x6678 + (uint)*(byte *)0x136a * 0x100;
//       iVar7 = FUN_24dd_4654(*(undefined1 *)0x137e);
//       iVar8 = ((uint)*(byte *)0x1374 + iVar7) * 0x100;
//       if (*(char *)0x1388 == '\x01') {
//         iVar8 = iVar8 + 1;
//       }
//       FUN_202c_005a(iVar8,(int)*(undefined4 *)0x6678 + ((uint)*(byte *)0x1374 + iVar7) * 0x100,
//                     (int)((ulong)*(undefined4 *)0x6678 >> 0x10),iVar11,uVar13,iVar12,iVar10);
//       if (*(char *)0x66af != '\0') {
//         iVar10 = *(int *)0x6432;
//         local_8 = *(int *)0x6432 - 0x14;
//         if ((int)local_8 <= (int)(iVar10 + 0x14U)) {
//           do {
//             if ((local_8 < 0x8000) && ((int)local_8 < 0x1f8)) {
//               uVar9 = *(int *)0x6436 + 0x14;
//               local_a = *(int *)0x6436 - 0x14;
//               if ((int)local_a <= (int)uVar9) {
//                 do {
//                   if ((local_a < 0x8000) && ((int)local_a < 0x15e)) {
//                     iVar12 = 0x20;
//                     bVar5 = FUN_24dd_4161();
//                     if ((*(byte *)(iVar12 + 0x14e0) & bVar5) != 0) {
//                       iVar12 = 0x20;
//                       bVar5 = FUN_24dd_4161();
//                       if ((*(byte *)(iVar12 + 0x6604) & bVar5) != 0) {
//                         uVar4 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_a * 4);
//                         pcVar1 = (char *)((int)uVar4 + local_8);
//                         *pcVar1 = *pcVar1 + '\x04';
//                         goto LAB_1000_a653;
//                       }
//                     }
//                     uVar4 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_a * 4);
//                     bVar5 = *(byte *)((int)uVar4 + local_8);
//                     if ((0xa3 < bVar5) && (bVar5 < 0xa8)) {
//                       iVar12 = 0x20;
//                       bVar5 = FUN_24dd_4161();
//                       if ((*(byte *)(iVar12 + 0x6604) & bVar5) != 0) {
//                         uVar4 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_a * 4);
//                         pcVar1 = (char *)((int)uVar4 + local_8);
//                         *pcVar1 = *pcVar1 + -4;
//                       }
//                     }
//                   }
// LAB_1000_a653:
//                   if (local_a == uVar9) break;
//                   local_a = local_a + 1;
//                 } while( true );
//               }
//             }
//             if (local_8 == iVar10 + 0x14U) break;
//             local_8 = local_8 + 1;
//           } while( true );
//         }
//       }
//     }
//     *(undefined1 *)0x651f = 2;
//     *(undefined2 *)0x67b0 = 0;
//     *(undefined2 *)0x67b2 = 0;
//     *(undefined2 *)0x67b4 = 0;
//     *(undefined2 *)0x67b6 = 0;
//     FUN_1000_929a();
//     local_4 = 0;
//     while( true ) {
//       uVar13 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
//       iVar12 = (int)*(undefined4 *)0x6670 + local_4 * 0xaa;
//       *(undefined1 *)(iVar12 + 0x97) = 0;
//       iVar10 = *(int *)0x669f;
//       *(int *)(iVar12 + 0x38) = iVar10;
//       *(int *)(iVar12 + 0x3a) = iVar10 >> 0xf;
//       *(undefined1 *)(iVar12 + 0x9f) = 1;
//       *(undefined1 *)(iVar12 + 0xa0) = 1;
//       if (local_4 == 1) break;
//       local_4 = local_4 + 1;
//     }
//     if (*(char *)0x4b8 != '\0') {
//       FUN_235c_095c(0,0x17,*(undefined2 *)0x6790,*(undefined2 *)0x6792);
//     }
//     *(undefined2 *)0x6520 = 0;
//     local_4 = 1;
//     while( true ) {
//       iVar10 = *(int *)(local_4 * 2 + 0xdbc) >> 0xf;
//       FUN_24dd_3d80();
//       uVar13 = FUN_24dd_3dbd();
//       *(undefined2 *)(local_4 * 4 + 0x6478) = uVar13;
//       *(int *)(local_4 * 4 + 0x647a) = iVar10;
//       if (*(int *)(local_4 * 4 + 0x6478) == 0 && *(int *)(local_4 * 4 + 0x647a) == 0) {
//         *(undefined2 *)(local_4 * 4 + 0x6478) = 1;
//         *(undefined2 *)(local_4 * 4 + 0x647a) = 0;
//       }
//       if (local_4 == 0x28) break;
//       local_4 = local_4 + 1;
//     }
//   }
//   *(int *)0x6524 = (uint)param_1 * 0xb4;
//   *(undefined1 *)0x651c = 0;
//   do {
//     *(int *)0x6520 = *(int *)0x6520 + 1;
//     if ((*(char *)0x669c != '\0') && (iVar10 = FUN_24dd_4654(0x6a4), iVar10 == 0)) {
//       FUN_1000_0ac7();
//     }
//     FUN_1000_10ec();
//     FUN_1000_8c03();
//     uVar13 = 0xa771;
//     FUN_1000_5e66();
//     cVar6 = FUN_1000_9e7a(uVar13);
//     if (cVar6 != '\0') {
//       *(undefined1 *)0x651d = 1;
//       *(undefined1 *)0x651c = 1;
//     }
//     local_6 = 0;
//     while( true ) {
//       if (0 < *(int *)(local_6 * 4 + 0x67ba)) {
//         puVar2 = (uint *)(local_6 * 4 + 0x67b8);
//         uVar9 = *puVar2;
//         *puVar2 = *puVar2 - 4000;
//         piVar3 = (int *)(local_6 * 4 + 0x67ba);
//         *piVar3 = *piVar3 - (uint)(uVar9 < 4000);
//       }
//       if (local_6 == 1) break;
//       local_6 = local_6 + 1;
//     }
//     if ((*(char *)0x783c != '\0') && (*(char *)0x651c == '\0')) {
//       *(undefined1 *)0x651d = 0;
//       *(undefined1 *)0x783c = 0;
//       *(undefined2 *)0x6524 = 0x1f;
//       *(undefined1 *)0x651c = 1;
//     }
//     if (*(char *)0x651c == '\0') {
//       if (((param_1 == 0) && (*(int *)0x6524 < 0x21)) &&
//          (*(int *)0x6524 = *(int *)0x6524 + 1, *(int *)0x6524 == 0x21)) {
//         *(undefined2 *)0x6524 = 0xb4;
//       }
//     }
//     else {
//       *(int *)0x6524 = *(int *)0x6524 + -1;
//     }
//   } while (*(int *)0x6524 != 0);
//   return;
// }
// 
// --- end reference ---
procedure FUN_1000_9f45;
begin
  { TODO: translate from asm/FUN_1000_9f45.s — UNMATCHED until an oracle passes }
end;

