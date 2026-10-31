{ stickman::FUN_1000_374b — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_374b.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_374b.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_1000_374b(void)
// 
// {
//   undefined1 extraout_AH;
//   undefined2 unaff_SS;
//   undefined1 *puVar1;
//   undefined2 uVar2;
//   undefined1 local_4b8 [187];
//   byte abStack_3fd [65];
//   undefined2 auStack_3bc [347];
//   undefined1 local_106 [256];
//   int local_6;
//   int local_4;
//   
//   local_4 = 0x1000;
//   local_6 = 0x3756;
//   FUN_42b5_04df();
//   FUN_3de3_0c99(0x3717,0x42b5);
//   local_6 = FUN_4170_01b8(CONCAT11(extraout_AH,0x40),0x371f,0x3de3);
//   if (local_6 == -1) {
//     FUN_42b5_1a42(0x200,0x2b2,auStack_3bc + 2,unaff_SS);
//   }
//   else {
//     FUN_4170_024c(0x2b2,auStack_3bc + 2,unaff_SS,local_6);
//     FUN_4170_049d(local_6);
//   }
//   FUN_3de3_0b67(10,1);
//   FUN_3de3_002d(0x372a,0x3de3);
//   local_4 = 1;
//   while( true ) {
//     if ((bool)((byte)local_4 & 1)) {
//       FUN_3de3_002d(0x3731,0x3de3);
//     }
//     else {
//       FUN_3de3_002d(0x3737,0x3de3);
//     }
//     FUN_42b5_1766(0xff,local_106,unaff_SS,2,local_4,local_4 >> 0xf);
//     puVar1 = local_4b8;
//     uVar2 = unaff_SS;
//     FUN_42b5_0bc4(local_106,unaff_SS);
//     FUN_42b5_0c51(0x373d,0x42b5);
//     FUN_3de3_002d(puVar1,uVar2);
//     FUN_42b5_1766(0xff,local_106,unaff_SS,0xb,*(undefined2 *)((int)auStack_3bc + local_4 * 0x45),
//                   *(undefined2 *)((int)auStack_3bc + local_4 * 0x45 + 2));
//     while (abStack_3fd[local_4 * 0x45] < 0x40) {
//       puVar1 = local_4b8;
//       uVar2 = unaff_SS;
//       FUN_42b5_0bc4(abStack_3fd + local_4 * 0x45,unaff_SS);
//       FUN_42b5_0c51(0x373d,0x42b5);
//       FUN_42b5_0bde(0x40,abStack_3fd + local_4 * 0x45,unaff_SS,puVar1,uVar2);
//     }
//     puVar1 = local_4b8;
//     uVar2 = unaff_SS;
//     FUN_42b5_0bc4(local_106,unaff_SS);
//     FUN_42b5_0c51(0x373d,0x42b5);
//     FUN_42b5_0c51(abStack_3fd + local_4 * 0x45,unaff_SS);
//     FUN_42b5_0c51(0x373f,0x42b5);
//     FUN_42b5_0c51(0x3741,0x42b5);
//     FUN_3de3_002d(puVar1,uVar2);
//     if (local_4 == 10) break;
//     local_4 = local_4 + 1;
//   }
//   FUN_3de3_0b37();
//   FUN_3de3_0c99(0x3743,0x3de3);
//   return;
// }
// 
// --- end reference ---
procedure FUN_1000_374b;
begin
  { TODO: translate from asm/FUN_1000_374b.s — UNMATCHED until an oracle passes }
end;

