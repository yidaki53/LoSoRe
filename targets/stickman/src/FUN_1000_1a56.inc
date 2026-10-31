{ stickman::FUN_1000_1a56 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_1a56.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_1a56.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_1000_1a56(void)
// 
// {
//   char cVar1;
//   undefined2 unaff_DS;
//   
//   FUN_42b5_04df();
//   if ((*(int *)0x3ac == 0) &&
//      (cVar1 = FUN_1000_10fa(*(undefined2 *)0x3b0,*(int *)0x3ae + -2), cVar1 == '\0')) {
//     if (*(char *)0x3a6 == '\0') {
//       FUN_3de3_0b67(*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
//       FUN_3de3_002d(0x1a30,0x3de3);
//       *(int *)0x3ae = *(int *)0x3ae + -1;
//       if (*(char *)0x6 == '\0') {
//         FUN_3de3_0bea(0x1a4b,0x3de3,*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
//       }
//       else {
//         FUN_3de3_0bea(0x1a3f,0x3de3,*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
//       }
//       FUN_1000_1619(10);
//       FUN_3de3_0b67(*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
//       FUN_3de3_002d(0x1a30,0x3de3);
//       cVar1 = FUN_1000_10fa(*(undefined2 *)0x3b0,*(int *)0x3ae + -2);
//       if (cVar1 == '\0') {
//         *(int *)0x3ae = *(int *)0x3ae + -1;
//       }
//       FUN_3de3_0bea(0x1a21,0x3de3,*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
//       FUN_1000_1619(10);
//       *(bool *)6 = *(char *)0x6 == '\0';
//     }
//     else {
//       cVar1 = FUN_1000_10fa(*(undefined2 *)0x3b0,*(int *)0x3ae + -3);
//       if ((cVar1 == '\0') &&
//          (cVar1 = FUN_1000_10fa(*(undefined2 *)0x3b0,*(int *)0x3ae + -4), cVar1 == '\0')) {
//         FUN_1000_0614();
//         *(int *)0x3ae = *(int *)0x3ae + -3;
//         FUN_3de3_0bea(0x1a21,0x42b5,*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
//         *(undefined1 *)0x3a6 = 0;
//       }
//     }
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_1000_1a56;
begin
  { TODO: translate from asm/FUN_1000_1a56.s — UNMATCHED until an oracle passes }
end;

