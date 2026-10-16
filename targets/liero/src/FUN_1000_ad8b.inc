{ liero::FUN_1000_ad8b — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_ad8b.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_ad8b.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// uint FUN_1000_ad8b(int param_1,int param_2,uint param_3,uint param_4,int param_5,int param_6)
// 
// {
//   int iVar1;
//   int iVar2;
//   undefined1 extraout_AH;
//   int iVar3;
//   undefined2 unaff_SS;
//   undefined2 unaff_DS;
//   byte *pbVar4;
//   undefined2 uVar5;
//   undefined1 *puVar6;
//   undefined2 uVar7;
//   undefined1 local_313 [256];
//   byte local_213 [256];
//   uint local_113;
//   byte local_111 [256];
//   byte local_11;
//   uint local_10;
//   uint local_e;
//   uint local_8;
//   int local_6;
//   uint local_4;
//   
//   local_4 = 0x1000;
//   local_6 = -0x526a;
//   FUN_24dd_0530();
//   *(undefined1 *)(param_1 + -0x20e) = 1;
//   FUN_24ba_00c4();
//   pbVar4 = local_213;
//   uVar5 = unaff_SS;
//   FUN_202c_076d(param_2,param_2 >> 0xf);
//   FUN_24dd_3eaf(0xff,local_111,unaff_SS,pbVar4,uVar5);
//   pbVar4 = local_213;
//   iVar3 = (int)param_3 >> 0xf;
//   uVar5 = unaff_SS;
//   FUN_202c_076d(param_3,iVar3);
//   local_10 = (uint)*pbVar4;
//   local_e = 0;
//   do {
//     pbVar4 = local_213;
//     uVar5 = unaff_SS;
//     FUN_24dd_3e95(local_111,unaff_SS);
//     FUN_24dd_3f14(0xad89,0x24dd);
//     local_113 = FUN_202c_0673(pbVar4,uVar5);
//     FUN_1ec2_00a5(8,(0x14a - param_5) + (local_113 >> 1),
//                   (int)*(undefined4 *)0x65d7 + param_6 * 0x140 +
//                   ((param_5 + -10) - (local_113 >> 1)),(int)((ulong)*(undefined4 *)0x65d7 >> 0x10),
//                   (int)*(undefined4 *)0x6684 + param_6 * 0x140 +
//                   ((param_5 + -10) - (local_113 >> 1)),(int)((ulong)*(undefined4 *)0x6684 >> 0x10));
//     FUN_1ec2_0d88(0,7,local_113,
//                   (int)*(undefined4 *)0x65d7 + param_6 * 0x140 + ((param_5 + -2) - (local_113 >> 1))
//                   ,(int)((ulong)*(undefined4 *)0x65d7 >> 0x10));
//     iVar1 = param_5 - (local_113 >> 1);
//     iVar2 = param_6 + 1;
//     pbVar4 = local_213;
//     uVar5 = unaff_SS;
//     FUN_24dd_3e95(local_111,unaff_SS);
//     FUN_24dd_3f14(0xad89,0x24dd);
//     FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x65d7,
//                   (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),0x32,pbVar4,uVar5,iVar2,iVar1);
//     FUN_1ec2_00a5(8,(0x14a - param_5) + (local_113 >> 1),
//                   param_6 * 0x140 + ((param_5 + -10) - (local_113 >> 1)),0xa000,
//                   (int)*(undefined4 *)0x65d7 + param_6 * 0x140 +
//                   ((param_5 + -10) - (local_113 >> 1)),(int)((ulong)*(undefined4 *)0x65d7 >> 0x10));
//     local_11 = FUN_249c_019d();
//     if ((local_11 < 0x30) || (0x39 < local_11)) {
//       if (local_11 == 8) {
//         FUN_24dd_403d(1,local_111[0],local_111,unaff_SS);
//       }
//     }
//     else if ((0 < (int)local_e) || ((local_e < 0x8000 && (local_111[0] < local_10)))) {
//       puVar6 = local_313;
//       uVar7 = unaff_SS;
//       FUN_24dd_3e95(local_111,unaff_SS);
//       pbVar4 = local_213;
//       uVar5 = unaff_SS;
//       FUN_24dd_3fb1(CONCAT11(extraout_AH,local_11));
//       FUN_24dd_3f14(pbVar4,uVar5);
//       FUN_24dd_3eaf(0xff,local_111,unaff_SS,puVar6,uVar7);
//     }
//     iVar1 = (int)param_4 >> 0xf;
//     if (local_111[0] == 0) {
//       local_8 = param_4;
//       local_6 = iVar1;
//     }
//     else {
//       FUN_1000_a8f7(param_1,&local_8,unaff_SS,local_111,unaff_SS);
//     }
//   } while (local_11 != 0xd);
//   FUN_24ba_0090();
//   if ((local_6 < iVar1) || ((local_6 <= iVar1 && (local_8 < param_4)))) {
//     local_8 = param_4;
//     local_6 = iVar1;
//   }
//   if ((iVar3 < local_6) || ((iVar3 <= local_6 && (param_3 < local_8)))) {
//     local_8 = param_3;
//     local_6 = iVar3;
//   }
//   local_4 = local_8;
//   if (local_111[0] == 0) {
//     *(undefined1 *)(param_1 + -0x10c) = 0;
//   }
//   else {
//     *(undefined1 *)(param_1 + -0x10c) = 1;
//   }
//   if (*(char *)0x4b8 != '\0') {
//     FUN_235c_095c(0,0,*(undefined2 *)0x67a4,*(undefined2 *)0x67a6);
//   }
//   return local_4;
// }
// 
// --- end reference ---
procedure FUN_1000_ad8b;
begin
  { TODO: translate from asm/FUN_1000_ad8b.s — UNMATCHED until an oracle passes }
end;

