{ liero::FUN_1000_929a — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_929a.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_929a.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_1000_929a(void)
// 
// {
//   char *pcVar1;
//   char cVar2;
//   byte bVar3;
//   undefined2 uVar4;
//   int iVar5;
//   undefined2 unaff_SS;
//   undefined2 unaff_DS;
//   undefined1 *puVar6;
//   undefined1 *puVar7;
//   undefined2 uVar8;
//   undefined1 local_72 [32];
//   undefined1 local_52 [32];
//   byte local_32 [32];
//   char local_12 [2];
//   int aiStack_10 [7];
//   
//   aiStack_10[6] = 0x1000;
//   aiStack_10[5] = -0x6d5b;
//   FUN_24dd_0530();
//   aiStack_10[2] = 0;
//   aiStack_10[6] = 1;
//   while( true ) {
//     if (*(char *)(aiStack_10[6] + 0x66af) == '\0') {
//       aiStack_10[2] = aiStack_10[2] + 1;
//     }
//     if (aiStack_10[6] == 0x25) break;
//     aiStack_10[6] = aiStack_10[6] + 1;
//   }
//   aiStack_10[6] = 0;
//   while( true ) {
//     puVar7 = local_52;
//     uVar4 = unaff_SS;
//     FUN_24dd_40d6(1);
//     FUN_24dd_4141(0x20,local_32,unaff_SS,puVar7,uVar4);
//     aiStack_10[5] = 1;
//     while( true ) {
//       if ((*(char *)(aiStack_10[6] * 5 + aiStack_10[5] + 0x66dd) == '\0') ||
//          (*(char *)(aiStack_10[6] + 0x66a7) != '\0')) {
//         cVar2 = FUN_24dd_4654(0x28);
//         *(char *)(aiStack_10[6] * 5 + aiStack_10[5] + 0x66dd) = cVar2 + '\x01';
//       }
//       if (aiStack_10[2] < 5) {
//         while ('\0' < *(char *)(*(byte *)(*(byte *)(aiStack_10[6] * 5 + aiStack_10[5] + 0x66dd) +
//                                          0xa9d) + 0x66af)) {
//           cVar2 = FUN_24dd_4654(0x28);
//           *(char *)(aiStack_10[6] * 5 + aiStack_10[5] + 0x66dd) = cVar2 + '\x01';
//         }
//       }
//       else {
//         while( true ) {
//           iVar5 = 0x20;
//           bVar3 = FUN_24dd_4161();
//           if (((local_32[iVar5] & bVar3) == 0) &&
//              (*(char *)(*(byte *)(*(byte *)(aiStack_10[6] * 5 + aiStack_10[5] + 0x66dd) + 0xa9d) +
//                        0x66af) < '\x01')) break;
//           cVar2 = FUN_24dd_4654(0x28);
//           *(char *)(aiStack_10[6] * 5 + aiStack_10[5] + 0x66dd) = cVar2 + '\x01';
//         }
//       }
//       puVar7 = local_72;
//       uVar8 = unaff_SS;
//       FUN_24dd_40ac(0x20,local_32,unaff_SS);
//       puVar6 = local_52;
//       uVar4 = unaff_SS;
//       FUN_24dd_40d6(0);
//       FUN_24dd_40ec(*(undefined1 *)(aiStack_10[6] * 5 + aiStack_10[5] + 0x66dd));
//       FUN_24dd_4181(puVar6,uVar4);
//       FUN_24dd_4141(0x20,local_32,unaff_SS,puVar7,uVar8);
//       *(undefined2 *)((int)*(undefined4 *)0x6670 + aiStack_10[6] * 0xaa + aiStack_10[5] * 2 + 0x7d)
//            = 0;
//       *(uint *)((int)*(undefined4 *)0x6670 + aiStack_10[6] * 0xaa + aiStack_10[5] * 2 + 0x73) =
//            (uint)*(byte *)(*(byte *)(aiStack_10[6] * 5 + aiStack_10[5] + 0x66dd) + 0xa9d);
//       if (aiStack_10[5] == 5) break;
//       aiStack_10[5] = aiStack_10[5] + 1;
//     }
//     *(undefined2 *)((int)*(undefined4 *)0x6670 + aiStack_10[6] * 0xaa + 0x4e) = 1;
//     iVar5 = aiStack_10[6] * 2;
//     (local_12 + iVar5 + 2)[0] = '\0';
//     (local_12 + iVar5 + 2)[1] = '\0';
//     local_12[aiStack_10[6]] = *(char *)(aiStack_10[6] + 0x66a7);
//     if (aiStack_10[6] == 1) break;
//     aiStack_10[6] = aiStack_10[6] + 1;
//   }
//   FUN_1000_5e66();
//   FUN_1ec2_0000(50000,(int)*(undefined4 *)0x65d7,(int)((ulong)*(undefined4 *)0x65d7 >> 0x10),
//                 (int)*(undefined4 *)0x6684);
//   uVar8 = 0x2f2;
//   uVar4 = FUN_202c_0673(0x9250,0x1ec2);
//   FUN_1ec2_0d88(0,7,uVar4,uVar8);
//   FUN_1ec2_13e9(0x19a6,unaff_DS,0,0xa000,0x32,0x9250,0x1ec2,3);
//   aiStack_10[4] = FUN_202c_0673(0x66ec);
//   FUN_1ec2_0d88(0,7,aiStack_10[4],(*(int *)0x24 - ((uint)aiStack_10[4] >> 1)) + 0x155d);
//   FUN_1ec2_13e9(0x19a6,unaff_DS,0,0xa000,*(byte *)0x68 + 2,0x66ec,unaff_DS,0x12);
//   aiStack_10[4] = FUN_202c_0673(0x6701);
//   FUN_1ec2_0d88(0,7,aiStack_10[4],(*(int *)0x26 - ((uint)aiStack_10[4] >> 1)) + 0x155d);
//   FUN_1ec2_13e9(0x19a6,unaff_DS,0,0xa000,*(byte *)0x69 + 2,0x6701,unaff_DS,0x12);
//   if (*(char *)0x66a9 == '\0') {
//     uVar8 = 0xa2;
//     puVar7 = &stack0xfece;
//     uVar4 = unaff_SS;
//     FUN_24dd_3e95(0x9273,0x1ec2);
//     FUN_24dd_3f14(0x672e,unaff_DS);
//     FUN_24dd_3f14(0x927c,0x24dd);
//     FUN_1ec2_13e9(0x19a6,unaff_DS,0,0xa000,0x32,puVar7,uVar4,uVar8);
//   }
//   else {
//     FUN_1ec2_13e9(0x19a6,unaff_DS,0,0xa000,0x32,0x9265,0x1ec2,0xa2);
//   }
//   aiStack_10[3] = 0;
//   do {
//     FUN_1ec2_0000(20000,(int)*(undefined4 *)0x6684 + 0x21c0,
//                   (int)((ulong)*(undefined4 *)0x6684 >> 0x10),(int)*(undefined4 *)0x65d7 + 0x21c0);
//     aiStack_10[6] = 0;
//     while( true ) {
//       if (local_12[aiStack_10[6]] == '\0') {
//         aiStack_10[5] = 1;
//         while( true ) {
//           aiStack_10[4] =
//                FUN_202c_0673(*(int *)((int)*(undefined4 *)0x6670 + aiStack_10[6] * 0xaa +
//                                       aiStack_10[5] * 2 + 0x73) * 0xe + 0x7e8);
//           if (aiStack_10[5] == *(int *)(local_12 + aiStack_10[6] * 2 + 2)) {
//             FUN_1ec2_0d88(0,7,aiStack_10[4],
//                           (int)*(undefined4 *)0x6684 + (aiStack_10[5] * 8 + 0x1c) * 0x140 +
//                           *(int *)(aiStack_10[6] * 2 + 0x24) + -2);
//           }
//           else {
//             FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x6684 + 0x2581,
//                           (int)((ulong)*(undefined4 *)0x6684 >> 0x10),0,
//                           *(int *)((int)*(undefined4 *)0x6670 + aiStack_10[6] * 0xaa +
//                                    aiStack_10[5] * 2 + 0x73) * 0xe + 0x7e8,unaff_DS,
//                           aiStack_10[5] << 3);
//           }
//           FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x6684 + 0x2440,
//                         (int)((ulong)*(undefined4 *)0x6684 >> 0x10),
//                         *(undefined1 *)
//                          ((aiStack_10[5] == *(int *)(local_12 + aiStack_10[6] * 2 + 2)) + 0x206),
//                         *(int *)((int)*(undefined4 *)0x6670 + aiStack_10[6] * 0xaa +
//                                  aiStack_10[5] * 2 + 0x73) * 0xe + 0x7e8,unaff_DS,aiStack_10[5] << 3
//                        );
//           if (aiStack_10[5] == 5) break;
//           aiStack_10[5] = aiStack_10[5] + 1;
//         }
//         aiStack_10[4] = FUN_202c_0673(0x927e);
//         if (*(int *)(local_12 + aiStack_10[6] * 2 + 2) == 6) {
//           FUN_1ec2_0d88(0,7,aiStack_10[4],
//                         (int)*(undefined4 *)0x6684 + *(int *)(aiStack_10[6] * 2 + 0x24) + 0x5efe);
//         }
//         else {
//           FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x6684 + 0x2581,
//                         (int)((ulong)*(undefined4 *)0x6684 >> 0x10),0,0x927e,0x202c,0x30);
//         }
//         FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x6684 + 0x2440,
//                       (int)((ulong)*(undefined4 *)0x6684 >> 0x10),
//                       *(undefined1 *)((*(int *)(local_12 + aiStack_10[6] * 2 + 2) == 6) + 0x208),
//                       0x927e,0x1ec2,0x30);
//         aiStack_10[4] = FUN_202c_0673(0x9284);
//         if (*(int *)(local_12 + aiStack_10[6] * 2 + 2) == 0) {
//           FUN_1ec2_0d88(0,7,aiStack_10[4],
//                         (int)*(undefined4 *)0x6684 + *(int *)(aiStack_10[6] * 2 + 0x24) + 0x22fe);
//         }
//         else {
//           FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x6684 + 0x2581,
//                         (int)((ulong)*(undefined4 *)0x6684 >> 0x10),0,0x9284,0x202c,0);
//         }
//         FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x6684 + 0x2440,
//                       (int)((ulong)*(undefined4 *)0x6684 >> 0x10),
//                       (uint)(*(int *)(local_12 + aiStack_10[6] * 2 + 2) == 0) * 0xa7 + 1,0x928e,
//                       0x1ec2,0);
//         if (*(char *)(*(byte *)(aiStack_10[6] * 7 + 0x6722) + 0x783b) != '\0') {
//           *(undefined1 *)(*(byte *)(aiStack_10[6] * 7 + 0x6722) + 0x783b) = 0;
//           if (*(char *)0x4b8 != '\0') {
//             FUN_235c_095c(0,0,*(undefined2 *)0x679c);
//           }
//           do {
//             pcVar1 = (char *)(aiStack_10[6] * 5 + *(int *)(local_12 + aiStack_10[6] * 2 + 2) +
//                              0x66dd);
//             *pcVar1 = *pcVar1 + -1;
//             if (*(char *)(aiStack_10[6] * 5 + *(int *)(local_12 + aiStack_10[6] * 2 + 2) + 0x66dd)
//                 == '\0') {
//               *(undefined1 *)
//                (aiStack_10[6] * 5 + *(int *)(local_12 + aiStack_10[6] * 2 + 2) + 0x66dd) = 0x28;
//             }
//           } while (*(char *)(*(byte *)(*(byte *)(aiStack_10[6] * 5 +
//                                                  *(int *)(local_12 + aiStack_10[6] * 2 + 2) + 0x66dd
//                                                 ) + 0xa9d) + 0x66af) != '\0');
//           *(uint *)((int)*(undefined4 *)0x6670 + aiStack_10[6] * 0xaa +
//                     *(int *)(local_12 + aiStack_10[6] * 2 + 2) * 2 + 0x73) =
//                (uint)*(byte *)(*(byte *)(aiStack_10[6] * 5 +
//                                          *(int *)(local_12 + aiStack_10[6] * 2 + 2) + 0x66dd) +
//                               0xa9d);
//         }
//         if (*(char *)(*(byte *)(aiStack_10[6] * 7 + 0x6723) + 0x783b) != '\0') {
//           *(undefined1 *)(*(byte *)(aiStack_10[6] * 7 + 0x6723) + 0x783b) = 0;
//           if (*(char *)0x4b8 != '\0') {
//             FUN_235c_095c(0,0,*(undefined2 *)0x67a0);
//           }
//           do {
//             pcVar1 = (char *)(aiStack_10[6] * 5 + *(int *)(local_12 + aiStack_10[6] * 2 + 2) +
//                              0x66dd);
//             *pcVar1 = *pcVar1 + '\x01';
//             if (0x28 < *(byte *)(aiStack_10[6] * 5 + *(int *)(local_12 + aiStack_10[6] * 2 + 2) +
//                                 0x66dd)) {
//               *(undefined1 *)
//                (aiStack_10[6] * 5 + *(int *)(local_12 + aiStack_10[6] * 2 + 2) + 0x66dd) = 1;
//             }
//           } while (*(char *)(*(byte *)(*(byte *)(aiStack_10[6] * 5 +
//                                                  *(int *)(local_12 + aiStack_10[6] * 2 + 2) + 0x66dd
//                                                 ) + 0xa9d) + 0x66af) != '\0');
//           *(uint *)((int)*(undefined4 *)0x6670 + aiStack_10[6] * 0xaa +
//                     *(int *)(local_12 + aiStack_10[6] * 2 + 2) * 2 + 0x73) =
//                (uint)*(byte *)(*(byte *)(aiStack_10[6] * 5 +
//                                          *(int *)(local_12 + aiStack_10[6] * 2 + 2) + 0x66dd) +
//                               0xa9d);
//         }
//         if (*(char *)(*(byte *)(aiStack_10[6] * 7 + 0x6720) + 0x783b) != '\0') {
//           *(undefined1 *)(*(byte *)(aiStack_10[6] * 7 + 0x6720) + 0x783b) = 0;
//           if (*(char *)0x4b8 != '\0') {
//             FUN_235c_095c(0,0,*(undefined2 *)0x67a0);
//           }
//           *(int *)(local_12 + aiStack_10[6] * 2 + 2) =
//                *(int *)(local_12 + aiStack_10[6] * 2 + 2) + -1;
//           if (*(int *)(local_12 + aiStack_10[6] * 2 + 2) < 0) {
//             iVar5 = aiStack_10[6] * 2;
//             (local_12 + iVar5 + 2)[0] = '\x06';
//             (local_12 + iVar5 + 2)[1] = '\0';
//           }
//         }
//         if (*(char *)(*(byte *)(aiStack_10[6] * 7 + 0x6721) + 0x783b) != '\0') {
//           *(undefined1 *)(*(byte *)(aiStack_10[6] * 7 + 0x6721) + 0x783b) = 0;
//           if (*(char *)0x4b8 != '\0') {
//             FUN_235c_095c(0,0,*(undefined2 *)0x679c);
//           }
//           *(int *)(local_12 + aiStack_10[6] * 2 + 2) =
//                *(int *)(local_12 + aiStack_10[6] * 2 + 2) + 1;
//           if (6 < *(int *)(local_12 + aiStack_10[6] * 2 + 2)) {
//             iVar5 = aiStack_10[6] * 2;
//             (local_12 + iVar5 + 2)[0] = '\0';
//             (local_12 + iVar5 + 2)[1] = '\0';
//           }
//         }
//         if (*(char *)(*(byte *)(aiStack_10[6] * 7 + 0x6724) + 0x783b) != '\0') {
//           if (*(int *)(local_12 + aiStack_10[6] * 2 + 2) == 0) {
//             puVar7 = local_52;
//             FUN_24dd_40d6(1);
//             FUN_24dd_4141(0x20,local_32,unaff_SS,puVar7);
//             aiStack_10[5] = 1;
//             while( true ) {
//               cVar2 = FUN_24dd_4654();
//               *(char *)(aiStack_10[6] * 5 + aiStack_10[5] + 0x66dd) = cVar2 + '\x01';
//               if (aiStack_10[2] < 5) {
//                 while ('\0' < *(char *)(*(byte *)(*(byte *)(aiStack_10[6] * 5 + aiStack_10[5] +
//                                                            0x66dd) + 0xa9d) + 0x66af)) {
//                   cVar2 = FUN_24dd_4654();
//                   *(char *)(aiStack_10[6] * 5 + aiStack_10[5] + 0x66dd) = cVar2 + '\x01';
//                 }
//               }
//               else {
//                 while( true ) {
//                   iVar5 = 0x20;
//                   bVar3 = FUN_24dd_4161();
//                   if (((local_32[iVar5] & bVar3) == 0) &&
//                      (*(char *)(*(byte *)(*(byte *)(aiStack_10[6] * 5 + aiStack_10[5] + 0x66dd) +
//                                          0xa9d) + 0x66af) < '\x01')) break;
//                   cVar2 = FUN_24dd_4654();
//                   *(char *)(aiStack_10[6] * 5 + aiStack_10[5] + 0x66dd) = cVar2 + '\x01';
//                 }
//               }
//               puVar7 = local_72;
//               FUN_24dd_40ac(0x20,local_32,unaff_SS);
//               puVar6 = local_52;
//               uVar4 = unaff_SS;
//               FUN_24dd_40d6(0);
//               FUN_24dd_40ec(*(undefined1 *)(aiStack_10[6] * 5 + aiStack_10[5] + 0x66dd));
//               FUN_24dd_4181(puVar6,uVar4);
//               FUN_24dd_4141(0x20,local_32,unaff_SS,puVar7);
//               *(undefined2 *)
//                ((int)*(undefined4 *)0x6670 + aiStack_10[6] * 0xaa + aiStack_10[5] * 2 + 0x7d) = 0;
//               *(uint *)((int)*(undefined4 *)0x6670 + aiStack_10[6] * 0xaa + aiStack_10[5] * 2 + 0x73
//                        ) = (uint)*(byte *)(*(byte *)(aiStack_10[6] * 5 + aiStack_10[5] + 0x66dd) +
//                                           0xa9d);
//               if (aiStack_10[5] == 5) break;
//               aiStack_10[5] = aiStack_10[5] + 1;
//             }
//           }
//           if (*(int *)(local_12 + aiStack_10[6] * 2 + 2) == 6) {
//             *(undefined1 *)(*(byte *)(aiStack_10[6] * 7 + 0x6724) + 0x783b) = 0;
//             if (*(char *)0x4b8 != '\0') {
//               FUN_235c_095c(0,0,*(undefined2 *)0x67a4);
//             }
//             local_12[aiStack_10[6]] = '\x01';
//           }
//         }
//       }
//       if (aiStack_10[6] == 1) break;
//       aiStack_10[6] = aiStack_10[6] + 1;
//     }
//     FUN_1ec2_13c5();
//     if (aiStack_10[3] < 0x21) {
//       FUN_1ec2_10ea(aiStack_10[3],0x5826);
//       aiStack_10[3] = aiStack_10[3] + 1;
//     }
//     FUN_1ec2_1619(0xffae);
//     FUN_1ec2_0000(20000,0x21c0,0xa000,(int)*(undefined4 *)0x6684 + 0x21c0);
//   } while (((local_12[0] == '\0') || (local_12[1] == '\0')) && (*(char *)0x783c == '\0'));
//   aiStack_10[6] = 0;
//   while( true ) {
//     *(undefined2 *)((int)*(undefined4 *)0x6670 + aiStack_10[6] * 0xaa + 0x4e) = 1;
//     for (aiStack_10[5] = 1;
//         *(uint *)((int)*(undefined4 *)0x6670 + aiStack_10[6] * 0xaa + aiStack_10[5] * 2 + 0x7d) =
//              (uint)*(byte *)(*(int *)((int)*(undefined4 *)0x6670 + aiStack_10[6] * 0xaa +
//                                       aiStack_10[5] * 2 + 0x73) + 0xe0d), aiStack_10[5] != 5;
//         aiStack_10[5] = aiStack_10[5] + 1) {
//     }
//     if (aiStack_10[6] == 1) break;
//     aiStack_10[6] = aiStack_10[6] + 1;
//   }
//   aiStack_10[6] = 0;
//   while( true ) {
//     for (aiStack_10[4] = 0;
//         *(undefined1 *)(*(byte *)(aiStack_10[6] * 7 + aiStack_10[4] + 0x6720) + 0x783b) = 0,
//         aiStack_10[4] != 6; aiStack_10[4] = aiStack_10[4] + 1) {
//     }
//     if (aiStack_10[6] == 1) break;
//     aiStack_10[6] = aiStack_10[6] + 1;
//   }
//   FUN_1ec2_155e(0x5826);
//   return;
// }
// 
// --- end reference ---
procedure FUN_1000_929a;
begin
  { TODO: translate from asm/FUN_1000_929a.s — UNMATCHED until an oracle passes }
end;

