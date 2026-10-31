{ stickman::FUN_42b5_1b2f — game Pascal draft (oracle: none).
  Drafted from asm/FUN_42b5_1b2f.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_42b5_1b2f.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_42b5_1b2f(void)
// 
// {
//   code *pcVar1;
//   char cVar2;
//   char extraout_DL;
//   undefined2 unaff_DS;
//   undefined2 local_82;
//   char local_80;
//   
//   FUN_42b5_1b9a();
//   if ((char)local_82 == '\0') {
//     return;
//   }
//   if ((char)((uint)local_82 >> 8) == ':') {
//     pcVar1 = (code *)swi(0x21);
//     (*pcVar1)();
//     pcVar1 = (code *)swi(0x21);
//     cVar2 = (*pcVar1)();
//     if (cVar2 != extraout_DL) {
//       *(undefined2 *)0x39c = 0xf;
//       return;
//     }
//     if (local_80 == '\0') {
//       return;
//     }
//   }
//   FUN_42b5_1bb5();
//   return;
// }
// 
// --- end reference ---
procedure FUN_42b5_1b2f;
begin
  { TODO: translate from asm/FUN_42b5_1b2f.s — UNMATCHED until an oracle passes }
end;

