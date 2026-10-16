{ liero::FUN_1000_b04a — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_b04a.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_b04a.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void FUN_1000_b04a(int param_1,byte *param_2,int param_3,int param_4,int param_5,undefined4 param_6)
// 
// {
//   byte *pbVar1;
//   byte *pbVar2;
//   int iVar3;
//   int iVar4;
//   undefined1 extraout_AH;
//   uint uVar5;
//   byte *pbVar6;
//   undefined2 unaff_SS;
//   undefined2 unaff_DS;
//   undefined1 *puVar7;
//   undefined1 *puVar8;
//   undefined2 uVar9;
//   undefined2 uVar10;
//   undefined1 local_309 [256];
//   undefined1 local_209 [256];
//   uint local_109;
//   char local_107;
//   byte local_102;
//   byte abStack_101 [251];
//   undefined2 uStack_6;
//   undefined2 uStack_4;
//   
//   uStack_4 = 0x1000;
//   uStack_6 = 0xb055;
//   FUN_24dd_0530();
//   pbVar6 = (byte *)param_2;
//   local_102 = *param_2;
//   pbVar2 = abStack_101;
//   for (uVar5 = (uint)local_102; pbVar6 = pbVar6 + 1, uVar5 != 0; uVar5 = uVar5 - 1) {
//     pbVar1 = pbVar2;
//     pbVar2 = pbVar2 + 1;
//     *pbVar1 = *pbVar6;
//   }
//   *(undefined1 *)(param_1 + -0x20e) = 1;
//   FUN_24ba_00c4();
//   do {
//     puVar7 = local_209;
//     uVar9 = unaff_SS;
//     FUN_24dd_3e95(&local_102,unaff_SS);
//     FUN_24dd_3f14(0xb048,0x24dd);
//     local_109 = FUN_202c_0673(puVar7,uVar9);
//     FUN_1ec2_00a5(8,(0x14a - param_4) + (local_109 >> 1),
//                   (int)*(undefined4 *)0x65d7 + param_5 * 0x140 +
//                   ((param_4 + -10) - (local_109 >> 1)),(int)((ulong)*(undefined4 *)0x65d7 >> 0x10),
//                   (int)*(undefined4 *)0x6684 + param_5 * 0x140 +
//                   ((param_4 + -10) - (local_109 >> 1)),(int)((ulong)*(undefined4 *)0x6684 >> 0x10));
//     FUN_1ec2_0d88(0,7,local_109,
//                   (int)*(undefined4 *)0x65d7 + param_5 * 0x140 + ((param_4 + -2) - (local_109 >> 1))
//                   ,(int)((ulong)*(undefined4 *)0x65d7 >> 0x10));
//     iVar3 = param_4 - (local_109 >> 1);
//     iVar4 = param_5 + 1;
//     puVar7 = local_209;
//     uVar9 = unaff_SS;
//     FUN_24dd_3e95(&local_102,unaff_SS);
//     FUN_24dd_3f14(0xb048,0x24dd);
//     FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x65d7,
//                   (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),0x32,puVar7,uVar9,iVar4,iVar3);
//     FUN_1ec2_00a5(8,(0x14a - param_4) + (local_109 >> 1),
//                   param_5 * 0x140 + ((param_4 + -10) - (local_109 >> 1)),0xa000,
//                   (int)*(undefined4 *)0x65d7 + param_5 * 0x140 +
//                   ((param_4 + -10) - (local_109 >> 1)),(int)((ulong)*(undefined4 *)0x65d7 >> 0x10));
//     local_107 = FUN_249c_019d();
//     if (local_107 == '\b') {
//       FUN_24dd_403d(1,local_102,&local_102,unaff_SS);
//     }
//     else if (((local_107 != '\r') && (local_107 != '\x1b')) && ((int)(uint)local_102 < param_3)) {
//       puVar7 = local_309;
//       uVar10 = unaff_SS;
//       FUN_24dd_3e95(&local_102,unaff_SS);
//       puVar8 = local_209;
//       uVar9 = unaff_SS;
//       FUN_24dd_3fb1(CONCAT11(extraout_AH,local_107));
//       FUN_24dd_3f14(puVar8,uVar9);
//       FUN_24dd_3eaf(0xff,&local_102,unaff_SS,puVar7,uVar10);
//     }
//   } while ((local_107 != '\r') && (local_107 != '\x1b'));
//   FUN_24ba_0090();
//   FUN_24dd_3eaf(0xff,(int)param_6,(int)((ulong)param_6 >> 0x10),&local_102,unaff_SS);
//   if (local_107 == '\x1b') {
//     *(undefined1 *)(param_1 + -0x10c) = 0;
//   }
//   else {
//     *(undefined1 *)(param_1 + -0x10c) = 1;
//   }
//   FUN_235c_095c(0,0,*(undefined2 *)0x67a4,*(undefined2 *)0x67a6);
//   return;
// }
// 
// --- end reference ---
procedure FUN_1000_b04a;
begin
  { TODO: translate from asm/FUN_1000_b04a.s — UNMATCHED until an oracle passes }
end;

