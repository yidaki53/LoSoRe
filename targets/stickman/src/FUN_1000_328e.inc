{ stickman::FUN_1000_328e — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_328e.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_328e.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void FUN_1000_328e(int param_1)
// 
// {
//   undefined1 extraout_AH;
//   undefined2 uVar1;
//   undefined2 unaff_DS;
//   
//   FUN_42b5_04df();
//   FUN_1000_0d44(1,param_1 * 0x80 + 0x2687,unaff_DS);
//   *(undefined2 *)0x3b4 = 10;
//   *(undefined1 *)0x3a5 = 0;
//   *(undefined2 *)0x3b2 = 0;
//   *(undefined1 *)0x3a8 = 0;
//   *(undefined2 *)0x3ac = 0;
//   *(undefined1 *)0x3a6 = 0;
//   *(undefined2 *)0x3aa = 0;
//   *(undefined1 *)0x3a7 = 0;
//   *(undefined1 *)0x3b8 = 0;
//   *(int *)0x4fd = param_1;
//   *(int *)0x4ff = param_1 >> 0xf;
//   uVar1 = 0x42b5;
//   FUN_42b5_1a42(0,0xc3,0x2600,unaff_DS);
//   FUN_1000_09dd(CONCAT11(extraout_AH,1));
//   do {
//     FUN_1000_2c4d();
//     if ((*(char *)0x3a5 != '\0') || (*(int *)0x3b4 < 1)) break;
//   } while (*(char *)0x3a7 == '\0');
//   *(undefined1 *)0x136 = 1;
//   if (*(int *)0x3b4 < 1) {
//     *(undefined1 *)0x3a8 = 1;
//   }
//   if (*(char *)0x3a8 == '\0') {
//     if (*(char *)0x3a7 != '\0') {
//       FUN_3de3_0b67(9,0x19);
//       FUN_3de3_002d(0x31ce,0x3de3);
//       FUN_3de3_0b67(10,0x19);
//       FUN_3de3_002d(0x31f5,0x3de3);
//       FUN_3de3_0b67(0xb,0x19);
//       FUN_3de3_002d(0x3212,0x3de3);
//       FUN_3de3_0b67(0xc,0x19);
//       FUN_3de3_002d(0x322f,0x3de3);
//       FUN_3de3_0b67(0xd,0x19);
//       FUN_3de3_002d(0x324c,0x3de3);
//       FUN_3de3_0b67(0xe,0x19);
//       FUN_3de3_002d(0x3269,0x3de3);
//       FUN_1000_30c3();
//       uVar1 = 0x3de3;
//       FUN_3de3_0b37();
//     }
//   }
//   else {
//     FUN_3de3_0b67(9,0x19);
//     FUN_3de3_002d(0x3146,0x3de3);
//     FUN_3de3_0b67(10,0x19);
//     FUN_3de3_002d(0x3165,0x3de3);
//     FUN_3de3_0b67(0xb,0x19);
//     FUN_3de3_002d(0x317a,0x3de3);
//     FUN_3de3_0b67(0xc,0x19);
//     FUN_3de3_002d(0x318f,0x3de3);
//     FUN_3de3_0b67(0xd,0x19);
//     FUN_3de3_002d(0x31a4,0x3de3);
//     FUN_3de3_0b67(0xe,0x19);
//     FUN_3de3_002d(0x31b9,0x3de3);
//     uVar1 = 0x3de3;
//     FUN_3de3_0b37();
//   }
//   FUN_3de3_0c99(0x3286,uVar1);
//   FUN_1000_01cf();
//   FUN_1000_2d1f();
//   return;
// }
// 
// --- end reference ---
procedure FUN_1000_328e(param_1: Integer);
begin
  { TODO: translate from asm/FUN_1000_328e.s — UNMATCHED until an oracle passes }
end;

