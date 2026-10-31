{ stickman::FUN_4170_0df2 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_4170_0df2.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_4170_0df2.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_4170_0df2(undefined4 param_1,undefined1 param_2,undefined1 *param_3)
// 
// {
//   undefined1 extraout_AH;
//   undefined2 uVar1;
//   undefined2 uVar2;
//   undefined2 unaff_SS;
//   undefined1 *puVar3;
//   undefined2 uVar4;
//   undefined1 local_204 [256];
//   undefined1 local_104 [254];
//   undefined2 uStack_6;
//   int local_4;
//   
//   local_4 = 0x4170;
//   uStack_6 = 0x24fd;
//   FUN_42b5_04df();
//   puVar3 = local_204;
//   uVar4 = unaff_SS;
//   FUN_42b5_0cf4(CONCAT11(extraout_AH,param_2));
//   uVar2 = (undefined2)((ulong)param_1 >> 0x10);
//   uVar1 = (undefined2)param_1;
//   local_4 = FUN_42b5_0c7d(uVar1,uVar2,puVar3,uVar4);
//   if (local_4 == 0) {
//     *param_3 = 0;
//   }
//   else {
//     FUN_42b5_0bde(0xff,local_104,unaff_SS,uVar1,uVar2);
//     FUN_42b5_0d75(0xff,local_4,local_104,unaff_SS);
//     FUN_42b5_0d75(local_4,1,uVar1,uVar2);
//     FUN_42b5_0bde(0xff,(undefined1 *)param_3,(int)((ulong)param_3 >> 0x10),local_104,unaff_SS);
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_4170_0df2(param_1: Longint; param_2: Byte; param_3: Pointer);
begin
  { TODO: translate from asm/FUN_4170_0df2.s — UNMATCHED until an oracle passes }
end;

