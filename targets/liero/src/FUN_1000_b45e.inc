{ liero::FUN_1000_b45e — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_b45e.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_b45e.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void FUN_1000_b45e(int param_1,byte param_2)
// 
// {
//   int *piVar1;
//   char *pcVar2;
//   undefined2 uVar3;
//   undefined1 extraout_AH;
//   int iVar4;
//   undefined2 uVar5;
//   undefined2 unaff_SS;
//   undefined2 unaff_DS;
//   undefined1 *puVar6;
//   undefined1 local_1cf [256];
//   char local_cf [31];
//   undefined1 auStack_b0 [10];
//   undefined2 local_a6;
//   byte local_a4;
//   undefined1 local_a3 [156];
//   byte local_7;
//   int local_6;
//   int local_4;
//   
//   local_4 = 0x1000;
//   local_6 = 0xb469;
//   FUN_24dd_0530();
//   local_7 = 0;
//   local_6 = 0;
//   FUN_24dd_4905(0,0x9c,local_a3,unaff_SS);
//   do {
//     *(undefined1 *)(param_1 + -0x20e) = 0;
//     FUN_1000_b28f(&stack0xfffe);
//     FUN_1ec2_00a5(0x82,0x9d,(int)*(undefined4 *)0x65d7 + 0x19a3,
//                   (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),(int)*(undefined4 *)0x6684 + 0x19a3,
//                   (int)((ulong)*(undefined4 *)0x6684 >> 0x10));
//     uVar5 = (undefined2)((ulong)*(undefined4 *)0x65d7 >> 0x10);
//     iVar4 = (int)*(undefined4 *)0x65d7 + (local_6 * 8 + 0x14) * 0x140 + 0xb2;
//     uVar3 = FUN_202c_0673(local_6 * 0xd + 0x390,unaff_DS);
//     FUN_1ec2_0d88(0,7,uVar3,iVar4,uVar5);
//     if (((byte)local_6 != 0) && ((byte)local_6 < 0xd)) {
//       local_a4 = FUN_202c_0673(auStack_b0 + local_6 * 0xd,unaff_SS);
//       FUN_1ec2_0d88(0,7,local_a4,
//                     (int)*(undefined4 *)0x65d7 + (local_6 * 8 + 0x14) * 0x140 +
//                     (0x111 - (uint)(local_a4 >> 1)),(int)((ulong)*(undefined4 *)0x65d7 >> 0x10));
//     }
//     local_a4 = FUN_202c_0673((uint)param_2 * 0x15 + 0x66ec,unaff_DS);
//     if (local_6 == 0) {
//       FUN_1ec2_0d88(0,7,local_a4,((int)*(undefined4 *)0x65d7 - (uint)(local_a4 >> 1)) + 0x1a11,
//                     (int)((ulong)*(undefined4 *)0x65d7 >> 0x10));
//     }
//     FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x65d7,
//                   (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),0,(uint)param_2 * 0x15 + 0x66ec,
//                   unaff_DS,0x16,0x114 - (uint)(local_a4 >> 1));
//     FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x65d7,
//                   (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),
//                   *(undefined1 *)((local_6 == 0) + 0x381),(uint)param_2 * 0x15 + 0x66ec,unaff_DS,
//                   0x15,0x113 - (uint)(local_a4 >> 1));
//     local_4 = 0;
//     while( true ) {
//       FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x65d7 + 0x1b80,
//                     (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),0,local_4 * 0xd + 0x390,unaff_DS,
//                     local_4 << 3,0xb5);
//       if (((byte)local_4 != 0) && ((byte)local_4 < 0xd)) {
//         local_a4 = FUN_202c_0673(auStack_b0 + local_4 * 0xd,unaff_SS);
//         FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x65d7 + 0x1b80,
//                       (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),0,auStack_b0 + local_4 * 0xd,
//                       unaff_SS,local_4 << 3,0x114 - (uint)(local_a4 >> 1));
//         FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x65d7 + 0x1a40,
//                       (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),
//                       *(undefined1 *)((local_4 == local_6) + 0x381),auStack_b0 + local_4 * 0xd,
//                       unaff_SS,local_4 << 3,0x113 - (uint)(local_a4 >> 1));
//       }
//       if ((1 < (byte)local_4) && ((byte)local_4 < 5)) {
//         if (local_4 == local_6) {
//           FUN_1ec2_0d88(0xffa8,7,*(byte *)((uint)param_2 * 3 + local_4 + 0x66d6) + 2,
//                         (int)*(undefined4 *)0x65d7 + (local_4 * 8 + 0x14) * 0x140 + 0xca,
//                         (int)((ulong)*(undefined4 *)0x65d7 >> 0x10));
//         }
//         else {
//           FUN_1ec2_0d88(0,7,*(byte *)((uint)param_2 * 3 + local_4 + 0x66d6) + 2,
//                         (int)*(undefined4 *)0x65d7 + (local_4 * 8 + 0x14) * 0x140 + 0xca,
//                         (int)((ulong)*(undefined4 *)0x65d7 >> 0x10));
//         }
//         FUN_1ec2_0d5d(*(undefined1 *)(param_2 + 0x68),5,
//                       *(undefined1 *)((uint)param_2 * 3 + local_4 + 0x66d6),
//                       (int)*(undefined4 *)0x65d7 + (local_4 * 8 + 0x15) * 0x140 + 0xcb,
//                       (int)((ulong)*(undefined4 *)0x65d7 >> 0x10));
//       }
//       FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x65d7 + 0x1a40,
//                     (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),
//                     *(undefined1 *)((local_6 == local_4) + 0x381),local_4 * 0xd + 0x390,unaff_DS,
//                     local_4 << 3,0xb4);
//       if (local_4 == 0xc) break;
//       local_4 = local_4 + 1;
//     }
//     FUN_1ec2_0d88(0,0xc,0xc,(int)*(undefined4 *)0x65d7 + 0x1fe3,
//                   (int)((ulong)*(undefined4 *)0x65d7 >> 0x10));
//     FUN_1ec2_01df(CONCAT11(extraout_AH,param_2),1,(int)*(undefined4 *)0x65d7 + 0xa0,
//                   (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),(int)*(undefined4 *)0x6678 + 0x1200,
//                   (int)((ulong)*(undefined4 *)0x6678 >> 0x10),0x1a,2);
//     if (*(char *)0x78db != '\0') {
//       if (*(char *)0x4b8 != '\0') {
//         FUN_235c_095c(0,0,*(undefined2 *)0x67a0,*(undefined2 *)0x67a2);
//       }
//       *(undefined1 *)0x78db = 0;
//       local_6 = local_6 + -1;
//       if (local_6 < 0) {
//         local_6 = 0xc;
//       }
//     }
//     if (*(char *)0x78e3 != '\0') {
//       if (*(char *)0x4b8 != '\0') {
//         FUN_235c_095c(0,0,*(undefined2 *)0x679c,*(undefined2 *)0x679e);
//       }
//       *(undefined1 *)0x78e3 = 0;
//       local_6 = local_6 + 1;
//       if (0xc < local_6) {
//         local_6 = 0;
//       }
//     }
//     if (local_7 == 0) {
//       if (local_6 == 1) {
//         if ((*(char *)0x78de != '\0') && (1 < *(uint *)((uint)param_2 * 2 + 0x66e8))) {
//           piVar1 = (int *)((uint)param_2 * 2 + 0x66e8);
//           *piVar1 = *piVar1 + -1;
//         }
//         if ((*(char *)0x78e0 != '\0') && (*(uint *)((uint)param_2 * 2 + 0x66e8) < 10000)) {
//           piVar1 = (int *)((uint)param_2 * 2 + 0x66e8);
//           *piVar1 = *piVar1 + 1;
//         }
//       }
//       else if ((local_6 < 2) || (4 < local_6)) {
//         if (local_6 == 0xd) {
//           if (*(char *)0x78de != '\0') {
//             if (*(char *)0x4b8 != '\0') {
//               FUN_235c_095c(0,0,*(undefined2 *)0x679c,*(undefined2 *)0x679e);
//             }
//             *(undefined1 *)0x78de = 0;
//             *(bool *)(param_2 + 0x66a7) = *(char *)(param_2 + 0x66a7) == '\0';
//           }
//           if (*(char *)0x78e0 != '\0') {
//             if (*(char *)0x4b8 != '\0') {
//               FUN_235c_095c(0,0,*(undefined2 *)0x67a0,*(undefined2 *)0x67a2);
//             }
//             *(undefined1 *)0x78e0 = 0;
//             *(bool *)(param_2 + 0x66a7) = *(char *)(param_2 + 0x66a7) == '\0';
//           }
//         }
//       }
//       else {
//         if ((*(char *)0x78de != '\0') &&
//            (pcVar2 = (char *)((uint)param_2 * 3 + local_6 + 0x66d6), *pcVar2 = *pcVar2 + -1,
//            0x3f < *(byte *)((uint)param_2 * 3 + local_6 + 0x66d6))) {
//           *(undefined1 *)((uint)param_2 * 3 + local_6 + 0x66d6) = 0;
//         }
//         if ((*(char *)0x78e0 != '\0') &&
//            (pcVar2 = (char *)((uint)param_2 * 3 + local_6 + 0x66d6), *pcVar2 = *pcVar2 + '\x01',
//            0x3f < *(byte *)((uint)param_2 * 3 + local_6 + 0x66d6))) {
//           *(undefined1 *)((uint)param_2 * 3 + local_6 + 0x66d6) = 0x3f;
//         }
//       }
//     }
//     if (*(char *)0x7857 != '\0') {
//       if (*(char *)0x4b8 != '\0') {
//         FUN_235c_095c(0,0,*(undefined2 *)0x67a4,*(undefined2 *)0x67a6);
//       }
//       *(undefined1 *)0x7857 = 0;
//       if (local_6 == 0) {
//         *(undefined1 *)(param_2 + 0x666e) = 0;
//         puVar6 = local_1cf;
//         uVar3 = unaff_SS;
//         FUN_1000_b04a(param_1,(uint)param_2 * 0x15 + 0x66ec,unaff_DS,0x14,0x113,0x14);
//         FUN_24dd_3eaf(0x28,local_cf,unaff_SS,puVar6,uVar3);
//         if (local_cf[0] == '\0') {
//           *(undefined1 *)(param_2 + 0x666e) = 1;
//         }
//         if (*(char *)(param_2 + 0x666e) == '\0') {
//           FUN_24dd_3eaf(0x14,(uint)param_2 * 0x15 + 0x66ec,unaff_DS,local_cf,unaff_SS);
//         }
//         else {
//           FUN_1000_a816(param_2);
//         }
//       }
//       else if (local_6 == 1) {
//         local_a6 = FUN_1000_ad8b(param_1,*(undefined2 *)((uint)param_2 * 2 + 0x66e8),10000,1,0x113,
//                                  0x1c);
//         if (*(char *)(param_1 + -0x10c) != '\0') {
//           *(undefined2 *)((uint)param_2 * 2 + 0x66e8) = local_a6;
//         }
//       }
//       else if ((local_6 < 5) || (0xb < local_6)) {
//         if ((local_6 < 2) || (4 < local_6)) {
//           if (local_6 == 0xc) {
//             *(bool *)(param_2 + 0x66a7) = *(char *)(param_2 + 0x66a7) == '\0';
//           }
//         }
//         else {
//           local_a6 = FUN_1000_ad8b(param_1,*(undefined1 *)((uint)param_2 * 3 + local_6 + 0x66d6),
//                                    0x3f,0,0x113,local_6 * 8 + 0x14);
//           if (*(char *)(param_1 + -0x10c) != '\0') {
//             *(undefined1 *)((uint)param_2 * 3 + local_6 + 0x66d6) = (undefined1)local_a6;
//           }
//         }
//       }
//       else {
//         local_a4 = FUN_202c_0673(auStack_b0 + local_6 * 0xd,unaff_SS);
//         do {
//           do {
//             local_a4 = FUN_1000_b3fe(&stack0xfffe);
//           } while (local_a4 == 0x82);
//         } while (local_a4 == 0x8f);
//         if (local_a4 != 1) {
//           *(byte *)((uint)param_2 * 7 + local_6 + 0x671b) = local_a4;
//         }
//       }
//     }
//     FUN_1000_05eb(param_2);
//     FUN_1ec2_13c5();
//     FUN_1ec2_1619(0xffae,0xffa8);
//     if (*(char *)(param_1 + -0x20e) == '\0') {
//       FUN_1ec2_00a5(0x82,0x9d,0x19a3,0xa000,(int)*(undefined4 *)0x65d7 + 0x19a3,
//                     (int)((ulong)*(undefined4 *)0x65d7 >> 0x10));
//     }
//     local_7 = local_7 + 1 & 3;
//   } while (*(char *)0x783c == '\0');
//   *(undefined1 *)0x783c = 0;
//   return;
// }
// 
// --- end reference ---
procedure FUN_1000_b45e;
begin
  { TODO: translate from asm/FUN_1000_b45e.s — UNMATCHED until an oracle passes }
end;

