{ stickman::FUN_1000_390b — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_390b.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_390b.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_1000_390b(void)
// 
// {
//   undefined2 uVar1;
//   undefined2 uVar2;
//   undefined2 unaff_SS;
//   undefined2 unaff_DS;
//   undefined1 local_104 [254];
//   undefined2 uStack_6;
//   int local_4;
//   
//   local_4 = 0x1000;
//   uStack_6 = 0x3916;
//   FUN_42b5_04df();
//   FUN_3de3_0c99(0x38f0,0x42b5);
//   FUN_3de3_002d(0x38f8,0x3de3);
//   FUN_42b5_1766(0xff,local_104,unaff_SS,9,*(undefined2 *)0x505,*(undefined2 *)0x507);
//   FUN_3de3_0bea(local_104,unaff_SS,10,0x20);
//   FUN_42b5_1766(0xff,local_104,unaff_SS,5,*(undefined2 *)0x501,*(undefined2 *)0x503);
//   FUN_3de3_0bea(local_104,unaff_SS,0xc,0x24);
//   if ((*(int *)0x503 < 1) && ((*(int *)0x503 < 0 || (*(int *)0x501 == 0)))) {
//     FUN_42b5_0bde(0xff,local_104,unaff_SS,0x38ff,0x3de3);
//   }
//   else {
//     uVar2 = *(undefined2 *)0x507;
//     uVar1 = FUN_42b5_0b2f();
//     FUN_42b5_1766(0xff,local_104,unaff_SS,3,uVar1,uVar2);
//   }
//   FUN_3de3_0bea(local_104,unaff_SS,0xe,0x26);
//   local_4 = 1;
//   while( true ) {
//     FUN_42b5_1766(0xff,local_104,unaff_SS,7,*(undefined2 *)(local_4 * 2 + 0x509),0);
//     FUN_3de3_0bea(local_104,unaff_SS,local_4 + 9,0x3e);
//     if (local_4 == 10) break;
//     local_4 = local_4 + 1;
//   }
//   FUN_3de3_0b37();
//   FUN_3de3_0c99(0x3903,0x3de3);
//   return;
// }
// 
// --- end reference ---
procedure FUN_1000_390b;
begin
  { TODO: translate from asm/FUN_1000_390b.s — UNMATCHED until an oracle passes }
end;

