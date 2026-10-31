{ stickman::FUN_1000_01cf — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_01cf.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_01cf.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_1000_01cf(void)
// 
// {
//   char cVar1;
//   undefined1 extraout_AH;
//   undefined2 unaff_SS;
//   undefined2 unaff_DS;
//   undefined1 *puVar2;
//   undefined1 local_190 [256];
//   undefined1 local_90 [138];
//   int local_6;
//   undefined1 uStack_4;
//   char local_3;
//   
//   uStack_4 = 0;
//   local_3 = 0x10;
//   local_6 = 0x1da;
//   FUN_42b5_04df();
//   local_6 = FUN_4170_01b8(CONCAT11(extraout_AH,0x42),0x178,0x42b5);
//   if (local_6 == -1) {
//     FUN_3de3_0278(0x185,0x4170);
//   }
//   local_3 = '\0';
//   while ((cVar1 = FUN_4170_03dd(local_6), cVar1 == '\0' && (cVar1 = local_3 == '\0', (bool)cVar1)))
//   {
//     FUN_4170_024c(0x8a,local_90,unaff_SS,local_6);
//     FUN_42b5_0cc9(0x4b8,unaff_DS,local_90,unaff_SS);
//     local_3 = cVar1;
//   }
//   if (local_3 == '\0') {
//     puVar2 = local_190;
//     FUN_42b5_0bc4(0x1af,0x4170);
//     FUN_42b5_0c51(0x4b8,unaff_DS);
//     FUN_42b5_0c51(0x1b6,0x42b5);
//     FUN_3de3_0278(puVar2,unaff_SS);
//   }
//   FUN_4170_02fc(0xff76,0xffff,1,local_6);
//   FUN_4170_02a4(0x8a,0x4b8,unaff_DS,local_6);
//   FUN_4170_049d(local_6);
//   return;
// }
// 
// --- end reference ---
procedure FUN_1000_01cf;
begin
  { TODO: translate from asm/FUN_1000_01cf.s — UNMATCHED until an oracle passes }
end;

