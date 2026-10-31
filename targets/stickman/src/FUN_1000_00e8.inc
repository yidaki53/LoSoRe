{ stickman::FUN_1000_00e8 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_00e8.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_00e8.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_1000_00e8(void)
// 
// {
//   undefined2 unaff_DS;
//   
//   FUN_42b5_04df();
//   if (*(char *)0x3b8 == '\0') {
//     *(undefined1 *)0x136 = 1;
//   }
//   else {
//     if (*(int *)0x3b6 == 1) {
//       FUN_42b5_0d75(1,1,0x3b8,unaff_DS);
//     }
//     else {
//       *(int *)0x3b6 = *(int *)0x3b6 + -1;
//     }
//     if (*(int *)0x3b6 == 1) {
//       FUN_42b5_0d75(1,1,0x3b8,unaff_DS);
//     }
//     else {
//       *(int *)0x3b6 = *(int *)0x3b6 + -1;
//     }
//     FUN_3de3_0b67(0x17,1);
//     FUN_3de3_002d(0x8d,0x3de3);
//     FUN_3de3_0b67(0x17,*(undefined2 *)0x3b6);
//     FUN_3de3_002d(0x3b8,unaff_DS);
//     FUN_3de3_002d(0xe3,0x3de3);
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_1000_00e8;
begin
  { TODO: translate from asm/FUN_1000_00e8.s — UNMATCHED until an oracle passes }
end;

