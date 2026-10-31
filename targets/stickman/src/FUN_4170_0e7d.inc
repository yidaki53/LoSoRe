{ stickman::FUN_4170_0e7d — game Pascal draft (oracle: none).
  Drafted from asm/FUN_4170_0e7d.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_4170_0e7d.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_4170_0e7d(undefined4 param_1,undefined4 param_2)
// 
// {
//   byte bVar1;
//   uint uVar2;
//   undefined2 unaff_SS;
//   uint local_104;
//   byte local_102 [252];
//   undefined2 uStack_6;
//   undefined2 uStack_4;
//   
//   uStack_4 = 0x4170;
//   uStack_6 = 0x2588;
//   FUN_42b5_04df();
//   FUN_42b5_0bde(0xff,local_102,unaff_SS,(int)param_1,(int)((ulong)param_1 >> 0x10));
//   if (local_102[0] != 0) {
//     if (local_102[0] != 0) {
//       local_104 = 1;
//       uVar2 = 0;
//       while( true ) {
//         bVar1 = FUN_42b5_1bc4(CONCAT11((char)(uVar2 >> 8),local_102[local_104]));
//         local_102[local_104] = bVar1;
//         if (local_104 == local_102[0]) break;
//         uVar2 = local_104;
//         local_104 = local_104 + 1;
//       }
//     }
//   }
//   FUN_42b5_0bde(0xff,(int)param_2,(int)((ulong)param_2 >> 0x10),local_102,unaff_SS);
//   return;
// }
// 
// --- end reference ---
procedure FUN_4170_0e7d(param_1, param_2: Longint);
begin
  { TODO: translate from asm/FUN_4170_0e7d.s — UNMATCHED until an oracle passes }
end;

