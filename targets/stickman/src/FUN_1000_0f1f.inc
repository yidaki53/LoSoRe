{ stickman::FUN_1000_0f1f — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_0f1f.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_0f1f.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined2 FUN_1000_0f1f(int param_1,int param_2)
// 
// {
//   byte bVar1;
//   undefined2 uVar2;
//   undefined1 uVar4;
//   undefined1 extraout_AH;
//   undefined1 extraout_AH_00;
//   undefined1 extraout_AH_01;
//   undefined1 extraout_AH_02;
//   int iVar3;
//   undefined1 extraout_AH_03;
//   undefined1 extraout_AH_04;
//   undefined2 unaff_DS;
//   undefined2 uVar5;
//   undefined1 local_3;
//   
//   uVar5 = 0xf2a;
//   FUN_42b5_04df();
//   local_3 = 1;
//   bVar1 = *(byte *)(param_1 * 0x50 + param_2 + 0x1f6f);
//   uVar4 = (undefined1)((uint)(param_1 * 0x50) >> 8);
//   if (bVar1 == 0xb) {
//     *(undefined1 *)(param_1 * 0x50 + param_2 + 0x1f6f) = 0;
//     *(int *)0x3b4 = *(int *)0x3b4 + 1;
//     if (*(int *)0x3b4 < 0xb) {
//       FUN_1000_0007(0xeff,0x42b5);
//     }
//     else {
//       *(undefined2 *)0x3b4 = 10;
//     }
//     FUN_3de3_0b67(param_1 + 1,param_2);
//     FUN_3de3_002d(0xf10,0x3de3);
//     FUN_1000_06a1();
//     uVar4 = extraout_AH;
//   }
//   else if (bVar1 == 0xc) {
//     *(undefined1 *)(param_1 * 0x50 + param_2 + 0x1f6f) = 0;
//     *(int *)0x3b2 = *(int *)0x3b2 + 3;
//     FUN_3de3_0b67(param_1 + 1,param_2);
//     FUN_3de3_002d(0xf10,0x3de3);
//     FUN_1000_0007(0xf12,0x3de3);
//     FUN_1000_0759();
//     uVar4 = extraout_AH_00;
//   }
//   else if (bVar1 == 0xd) {
//     *(undefined1 *)(param_1 * 0x50 + param_2 + 0x1f6f) = 0;
//     FUN_3de3_0b67(param_1 + 1,param_2);
//     FUN_3de3_002d(0xf10,0x3de3);
//     *(undefined1 *)0x3a7 = 1;
//     uVar4 = extraout_AH_01;
//   }
//   else if (bVar1 == 0xe) {
//     *(undefined1 *)(param_1 * 0x50 + param_2 + 0x1f6f) = 0;
//     *(int *)0x3aa = *(int *)0x3aa + 1;
//     FUN_3de3_0b67(param_1 + 1,param_2);
//     FUN_3de3_002d(0xf10,0x3de3);
//     FUN_1000_0007(0xf18,0x3de3);
//     FUN_1000_07df(uVar5);
//     uVar4 = extraout_AH_02;
//   }
//   else if ((bVar1 < 0xf) || (0x13 < bVar1)) {
//     local_3 = 0;
//   }
//   else {
//     iVar3 = *(byte *)(param_1 * 0x50 + param_2 + 0x1f6f) - 0xe;
//     uVar5 = *(undefined2 *)(iVar3 * 6 + 0x1f5a);
//     uVar2 = *(undefined2 *)(iVar3 * 6 + 0x1f5c);
//     FUN_1000_0d44(*(undefined2 *)(iVar3 * 6 + 0x1f5e),*(int *)0x4fd * 0x80 + 0x2687,unaff_DS);
//     *(undefined2 *)0x3ac = 0;
//     *(undefined1 *)0x3a6 = 0;
//     *(undefined1 *)0x3b8 = 0;
//     FUN_42b5_1a42(0,0xc3,0x2600,unaff_DS);
//     param_2._0_1_ = (undefined1)uVar5;
//     *(undefined1 *)0x6cc = (undefined1)param_2;
//     param_1._0_1_ = (undefined1)uVar2;
//     *(undefined1 *)0x6cd = (undefined1)param_1;
//     FUN_1000_09dd(CONCAT11(extraout_AH_03,1));
//     uVar4 = extraout_AH_04;
//   }
//   return CONCAT11(uVar4,local_3);
// }
// 
// --- end reference ---
function FUN_1000_0f1f(param_1, param_2: Integer): Word;
begin
  { TODO: translate from asm/FUN_1000_0f1f.s — UNMATCHED until an oracle passes }
end;

