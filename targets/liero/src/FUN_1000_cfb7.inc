{ liero::FUN_1000_cfb7 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_cfb7.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_cfb7.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// int FUN_1000_cfb7(byte param_1)
// 
// {
//   char cVar1;
//   undefined2 uVar2;
//   int iVar3;
//   undefined2 unaff_SS;
//   undefined2 unaff_DS;
//   undefined1 *puVar4;
//   undefined2 uVar5;
//   char local_10d [255];
//   int local_e;
//   int local_c;
//   char local_a;
//   char local_9;
//   char local_8;
//   byte local_7;
//   uint local_6;
//   int local_4;
//   
//   local_4 = 0x1000;
//   local_6 = 0xcfc2;
//   FUN_24dd_0530();
//   local_a = '\0';
//   FUN_1ec2_10ea(0,0x5826,unaff_DS);
//   FUN_1000_5e66();
//   FUN_1ec2_0d5d(0,7,0xa0,(int)*(undefined4 *)0x6684 + -0x4340);
//   FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x6684,
//                 (int)((ulong)*(undefined4 *)0x6684 >> 0x10),0x13,0xcf23,0x1ec2,0x98);
//   local_7 = param_1;
//   local_8 = '\0';
//   local_e = 0;
//   local_9 = '\0';
//   FUN_24dd_4905(0,0xab,0x783c);
//   FUN_24dd_4905(0,0xff,local_10d);
//   do {
//     FUN_1ec2_0000(45000,(int)*(undefined4 *)0x65d7 + 0x1900,
//                   (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),(int)*(undefined4 *)0x6684 + 0x1900);
//     FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x65d7 + 0x1900,
//                   (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),0,0xcf4b,0x1ec2,0x36);
//     FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x65d7 + 0x1900,
//                   (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),0,0xcf5c,0x1ec2,0x3d);
//     FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x65d7 + 0x1900,
//                   (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),10,0xcf4b,0x1ec2,0x35);
//     FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x65d7 + 0x1900,
//                   (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),10,0xcf5c,0x1ec2,0x3c);
//     if (*(char *)0x6664 == '\0') {
//       FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x65d7 + 0x1900,
//                     (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),0,0xcf6d,0x1ec2,0x2e);
//       FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x65d7 + 0x1900,
//                     (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),0xff93,0xcf6d,0x1ec2,0x2d);
//     }
//     else {
//       uVar5 = 0x2e;
//       puVar4 = &stack0xfcee;
//       uVar2 = unaff_SS;
//       FUN_24dd_3e95(0xcf8a,0x1ec2);
//       FUN_24dd_3f14(0x6664,unaff_DS);
//       FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x65d7 + 0x1900,
//                     (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),0,puVar4,uVar2,uVar5);
//       uVar5 = 0x2d;
//       puVar4 = &stack0xfcee;
//       uVar2 = unaff_SS;
//       FUN_24dd_3e95(0xcf8a,0x1ec2);
//       FUN_24dd_3f14(0x6664,unaff_DS);
//       FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x65d7 + 0x1900,
//                     (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),0xff93,puVar4,uVar2,uVar5);
//     }
//     FUN_1000_bcca();
//     if (param_1 == 0) {
//       local_c = 0;
//       while( true ) {
//         if (((char)local_7 == local_c) && (local_9 == '\0')) {
//           iVar3 = (int)*(undefined4 *)0x65d7 + (local_c * 8 + 0x14) * 0x140 + 0x35;
//           uVar2 = FUN_202c_0673(local_c * 0xe + 0x20a,unaff_DS);
//           FUN_1ec2_0d88(0,7,uVar2,iVar3);
//         }
//         else {
//           FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x65d7 + 0x1b80,
//                         (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),0,local_c * 0xe + 0x20a,unaff_DS
//                         ,local_c << 3);
//         }
//         if (((char)local_7 == local_c) && (local_9 == '\0')) {
//           cVar1 = '\x01';
//         }
//         else {
//           cVar1 = '\0';
//         }
//         FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x65d7 + 0x1a40,
//                       (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),*(undefined1 *)(cVar1 + 0x37d),
//                       local_c * 0xe + 0x20a,unaff_DS,local_c << 3);
//         if (local_c == 3) break;
//         local_c = local_c + 1;
//       }
//     }
//     else {
//       local_c = 0;
//       while( true ) {
//         if ((local_c + 1 == (int)(char)local_7) && (local_9 == '\0')) {
//           iVar3 = (int)*(undefined4 *)0x65d7 + (local_c * 8 + 0x14) * 0x140 + 0x35;
//           uVar2 = FUN_202c_0673((local_c + 1) * 0xe + 0x20a,unaff_DS);
//           FUN_1ec2_0d88(0,7,uVar2,iVar3);
//         }
//         else {
//           FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x65d7 + 0x1b80,
//                         (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),0,(local_c + 1) * 0xe + 0x20a,
//                         unaff_DS,local_c << 3);
//         }
//         if ((local_c + 1 == (int)(char)local_7) && (local_9 == '\0')) {
//           cVar1 = '\x01';
//         }
//         else {
//           cVar1 = '\0';
//         }
//         FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x65d7 + 0x1a40,
//                       (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),*(undefined1 *)(cVar1 + 0x37d),
//                       (local_c + 1) * 0xe + 0x20a,unaff_DS,local_c << 3);
//         if (local_c == 2) break;
//         local_c = local_c + 1;
//       }
//     }
//     if (local_9 != '\0') {
//       local_6 = FUN_202c_0673(local_10d + local_8 * 0x11);
//       iVar3 = (int)*(undefined4 *)0x65d7 + (local_8 * 8 + 0x14) * 0x140 + 0xb2;
//       uVar2 = FUN_202c_0673(local_8 * 0x15 + 0x242,unaff_DS);
//       FUN_1ec2_0d88(0,7,uVar2,iVar3);
//       if (local_10d[local_8 * 0x11] != '\0') {
//         FUN_1ec2_0d88(0,7,local_6,
//                       (int)*(undefined4 *)0x65d7 + (local_8 * 8 + 0x14) * 0x140 +
//                       (0x116 - (local_6 >> 1)));
//       }
//     }
//     local_c = 0;
//     while( true ) {
//       iVar3 = local_c * 8;
//       local_6 = FUN_202c_0673(local_10d + local_c * 0x11);
//       FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x65d7 + 0x1900,
//                     (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),0,local_c * 0x15 + 0x242,unaff_DS,
//                     iVar3 + 2);
//       FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x65d7 + 0x1900,
//                     (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),0,local_10d + local_c * 0x11,
//                     unaff_SS,iVar3 + 2);
//       if ((local_8 == local_c) && (local_9 != '\0')) {
//         cVar1 = '\x01';
//       }
//       else {
//         cVar1 = '\0';
//       }
//       FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x65d7 + 0x1900,
//                     (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),
//                     CONCAT11(local_9 >> 7,*(undefined1 *)(local_9 * 2 + (int)cVar1 + 0x37f)),
//                     local_c * 0x15 + 0x242,unaff_DS,iVar3 + 1);
//       if ((local_8 == local_c) && (local_9 != '\0')) {
//         cVar1 = '\x01';
//       }
//       else {
//         cVar1 = '\0';
//       }
//       FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x65d7 + 0x1900,
//                     (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),
//                     CONCAT11(local_9 >> 7,*(undefined1 *)(local_9 * 2 + (int)cVar1 + 0x37f)),
//                     local_10d + local_c * 0x11,unaff_SS,iVar3 + 1);
//       if (local_c == 0xe) break;
//       local_c = local_c + 1;
//     }
//     if (*(char *)0x783c != '\0') {
//       *(undefined1 *)0x783c = 0;
//       if (local_9 == '\0') {
//         local_7 = 3;
//       }
//       else {
//         local_9 = '\0';
//       }
//     }
//     if (*(char *)0x78db != '\0') {
//       if (*(char *)0x4b8 != '\0') {
//         FUN_235c_095c(0,0,*(undefined2 *)0x67a0);
//       }
//       *(undefined1 *)0x78db = 0;
//       if (local_9 == '\0') {
//         local_7 = local_7 - 1;
//         if ((int)(char)local_7 < (int)(uint)param_1) {
//           local_7 = 3;
//         }
//       }
//       else {
//         local_8 = local_8 + -1;
//         if (local_8 < '\0') {
//           local_8 = '\x0e';
//         }
//       }
//     }
//     if (*(char *)0x78e3 != '\0') {
//       if (*(char *)0x4b8 != '\0') {
//         FUN_235c_095c(0,0,*(undefined2 *)0x679c);
//       }
//       *(undefined1 *)0x78e3 = 0;
//       if (local_9 == '\0') {
//         local_7 = local_7 + 1;
//         if ('\x03' < (char)local_7) {
//           local_7 = param_1;
//         }
//       }
//       else {
//         local_8 = local_8 + '\x01';
//         if ('\x0e' < local_8) {
//           local_8 = '\0';
//         }
//       }
//     }
//     if (*(char *)0x7857 != '\0') {
//       if (*(char *)0x4b8 != '\0') {
//         FUN_235c_095c(0,0,*(undefined2 *)0x67a4);
//       }
//       *(undefined1 *)0x7857 = 0;
//       if (local_9 == '\0') {
//         local_9 = local_7 == 2;
//         local_a = !(bool)local_9;
//       }
//       else {
//         FUN_1000_bfd7(&stack0xfffe);
//       }
//     }
//     if (*(char *)0x785a != '\0') {
//       FUN_1000_a9c1();
//     }
//     if (*(char *)0x7861 != '\0') {
//       FUN_1000_ab94();
//     }
//     if (local_9 != '\0') {
//       if (*(char *)0x78de != '\0') {
//         FUN_1000_ccf1(&stack0xfffe,0xffff);
//       }
//       if (*(char *)0x78e0 != '\0') {
//         FUN_1000_ccf1(&stack0xfffe,1);
//       }
//     }
//     FUN_1ec2_13c5();
//     FUN_1ec2_1619(0xffae);
//     if (local_e < 0x20) {
//       local_e = local_e + 1;
//       FUN_1ec2_10ea(local_e,0x5826);
//     }
//     FUN_1ec2_0000(45000,0x1900,0xa000,(int)*(undefined4 *)0x65d7 + 0x1900);
//   } while (local_a == '\0');
//   local_4 = (int)(char)local_7;
//   local_c = 0x20;
//   while( true ) {
//     FUN_1ec2_13c5();
//     FUN_1ec2_10ea(local_c,0x5826);
//     if (local_c == 0) break;
//     local_c = local_c + -1;
//   }
//   for (local_c = 1;
//       *(undefined1 *)(local_c + 0x6453) =
//            (char)((int)((uint)*(byte *)(local_c + 0x10dd) * *(int *)0x66aa) / 100), local_c != 0x28;
//       local_c = local_c + 1) {
//   }
//   for (local_c = 1;
//       *(undefined1 *)(local_c + 0x643b) =
//            (char)((int)((uint)*(byte *)(local_c + 0x62d) * *(int *)0x66aa) / 100), local_c != 0x18;
//       local_c = local_c + 1) {
//   }
//   local_c = 0;
//   while( true ) {
//     puVar4 = &stack0xfcee;
//     FUN_24dd_3e95(local_c * 0x15 + 0x66ec,unaff_DS);
//     FUN_24dd_3f14(0xcf9c,0x24dd);
//     FUN_24dd_3eaf(0x28,local_c * 0x52 + 0x652e,unaff_DS,puVar4);
//     puVar4 = &stack0xfcee;
//     FUN_24dd_3e95(0xcfaf,0x24dd);
//     FUN_24dd_3f14(local_c * 0x15 + 0x66ec,unaff_DS);
//     FUN_24dd_3eaf(0x28,local_c * 0x52 + 0x6557,unaff_DS,puVar4);
//     if (local_c == 1) break;
//     local_c = local_c + 1;
//   }
//   return local_4;
// }
// 
// --- end reference ---
procedure FUN_1000_cfb7;
begin
  { TODO: translate from asm/FUN_1000_cfb7.s — UNMATCHED until an oracle passes }
end;

