{ stickman::FUN_405f_017d — game Pascal draft (oracle: none).
  Drafted from asm/FUN_405f_017d.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_405f_017d.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16far FUN_405f_017d(void)
// 
// {
//   code *pcVar1;
//   char cVar2;
//   undefined2 unaff_DS;
//   
//   FUN_42b5_04df();
//   if (*(int *)0xaaec != 0) {
//     do {
//       pcVar1 = (code *)swi(0x14);
//       (*pcVar1)();
//       while ((*(int *)0x156 != *(int *)0x158 &&
//              (cVar2 = FUN_405f_0067(CONCAT11((char)((uint)*(int *)0x156 >> 8),
//                                              *(undefined1 *)(*(int *)0x158 + -0x54fe))),
//              cVar2 != '\0'))) {
//         *(int *)0x158 = *(int *)0x158 + 1;
//         if (0x3fff < *(int *)0x158) {
//           *(int *)0x158 = *(int *)0x158 + -0x4000;
//         }
//       }
//     } while (*(int *)0x156 != *(int *)0x158);
//     pcVar1 = (code *)swi(0x14);
//     (*pcVar1)();
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_405f_017d;
begin
  { TODO: translate from asm/FUN_405f_017d.s — UNMATCHED until an oracle passes }
end;

