{ stickman::FUN_410e_030d — game Pascal draft (oracle: none).
  Drafted from asm/FUN_410e_030d.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_410e_030d.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16far FUN_410e_030d(void)
// 
// {
//   code *pcVar1;
//   char cVar2;
//   undefined1 extraout_AH;
//   undefined2 unaff_DS;
//   
//   cVar2 = *(char *)0xeb13;
//   *(undefined1 *)0xeb13 = 0;
//   if (cVar2 == '\0') {
//     pcVar1 = (code *)swi(0x16);
//     cVar2 = (*pcVar1)();
//     if (cVar2 == '\0') {
//       *(undefined1 *)0xeb13 = extraout_AH;
//     }
//   }
//   FUN_410e_0143();
//   return;
// }
// 
// --- end reference ---
procedure FUN_410e_030d;
begin
  { TODO: translate from asm/FUN_410e_030d.s — UNMATCHED until an oracle passes }
end;

