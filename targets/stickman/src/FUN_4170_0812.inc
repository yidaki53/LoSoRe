{ stickman::FUN_4170_0812 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_4170_0812.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_4170_0812.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined1 __stdcall16far FUN_4170_0812(undefined4 param_1)
// 
// {
//   int iVar1;
//   undefined2 unaff_SS;
//   undefined1 local_204 [256];
//   byte local_104 [254];
//   undefined2 uStack_6;
//   undefined2 uStack_4;
//   
//   uStack_4 = 0x4170;
//   uStack_6 = 0x1f1d;
//   FUN_42b5_04df();
//   FUN_42b5_0bde(0xff,local_104,unaff_SS,(int)param_1,(int)((ulong)param_1 >> 0x10));
//   if (local_104[local_104[0]] == 0x5c) {
//     local_104[0] = local_104[0] - 1;
//   }
//   FUN_42b5_1ade(0xff,local_204,unaff_SS,0);
//   FUN_42b5_1b2f(local_104,unaff_SS);
//   iVar1 = FUN_42b5_04a2();
//   uStack_4._1_1_ = iVar1 == 0;
//   FUN_42b5_1b2f(local_204,unaff_SS);
//   FUN_42b5_04a9();
//   return uStack_4._1_1_;
// }
// 
// --- end reference ---
function FUN_4170_0812(param_1: Longint): Byte;
begin
  { TODO: translate from asm/FUN_4170_0812.s — UNMATCHED until an oracle passes }
end;

