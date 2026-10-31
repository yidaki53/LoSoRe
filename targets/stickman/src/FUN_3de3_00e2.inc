{ stickman::FUN_3de3_00e2 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_3de3_00e2.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_3de3_00e2.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_3de3_00e2(undefined4 param_1)
// 
// {
//   undefined1 extraout_AH;
//   undefined2 unaff_SS;
//   undefined2 unaff_DS;
//   undefined1 *puVar1;
//   undefined2 uVar2;
//   undefined1 *puVar3;
//   undefined2 uVar4;
//   undefined1 local_404 [256];
//   undefined1 local_304 [256];
//   undefined1 local_204;
//   undefined1 local_203 [255];
//   int local_104;
//   undefined1 local_102;
//   undefined1 local_101 [251];
//   undefined2 uStack_6;
//   undefined2 uStack_4;
//   
//   uStack_4 = 0x3de3;
//   uStack_6 = 0xdf1d;
//   FUN_42b5_04df();
//   FUN_42b5_0bde(0xff,&local_102,unaff_SS,(int)param_1,(int)((ulong)param_1 >> 0x10));
//   puVar3 = local_304;
//   uVar2 = unaff_SS;
//   FUN_42b5_0bc4(0x138,unaff_DS);
//   FUN_42b5_0c51(0x91,0x42b5);
//   local_104 = FUN_4170_01b8(CONCAT11(extraout_AH,0x42),puVar3,uVar2);
//   if (local_104 == -1) {
//     puVar3 = local_304;
//     uVar2 = unaff_SS;
//     FUN_42b5_0bc4(0x138,unaff_DS);
//     FUN_42b5_0c51(0x91,0x42b5);
//     local_104 = FUN_4170_0123(puVar3,uVar2);
//   }
//   if (local_104 != -1) {
//     FUN_4170_02fc(0,0,2,local_104);
//     FUN_42b5_0bde(0xff,&local_204,unaff_SS,0x96,0x4170);
//     FUN_4170_02a4(local_204,local_203,unaff_SS,local_104);
//     puVar3 = local_304;
//     uVar4 = unaff_SS;
//     FUN_4170_1088(puVar3);
//     FUN_42b5_0c51(0xda,0x4170);
//     puVar1 = local_404;
//     uVar2 = unaff_SS;
//     FUN_4170_11bc(puVar1);
//     FUN_42b5_0c51(puVar1,uVar2);
//     FUN_42b5_0c51(0xde,0x42b5);
//     FUN_42b5_0c51(0xe0,0x42b5);
//     FUN_42b5_0bde(0xff,&local_204,unaff_SS,puVar3,uVar4);
//     FUN_4170_02a4(local_204,local_203,unaff_SS,local_104);
//     puVar3 = local_304;
//     uVar2 = unaff_SS;
//     FUN_42b5_0bc4(&local_102,unaff_SS);
//     FUN_42b5_0c51(0xde,0x42b5);
//     FUN_42b5_0c51(0xe0,0x42b5);
//     FUN_42b5_0bde(0xff,&local_102,unaff_SS,puVar3,uVar2);
//     FUN_4170_02a4(local_102,local_101,unaff_SS,local_104);
//     FUN_4170_049d(local_104);
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_3de3_00e2(param_1: Longint);
begin
  { TODO: translate from asm/FUN_3de3_00e2.s — UNMATCHED until an oracle passes }
end;

