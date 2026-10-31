{ stickman::FUN_410e_0143 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_410e_0143.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_410e_0143.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_410e_0143(void)
// 
// {
//   code *pcVar1;
//   undefined2 unaff_DS;
//   undefined1 uVar2;
//   
//   if (*(char *)0xeb14 == '\0') {
//     return;
//   }
//   *(undefined1 *)0xeb14 = 0;
//   uVar2 = 0;
//   while( true ) {
//     pcVar1 = (code *)swi(0x16);
//     (*pcVar1)();
//     if ((bool)uVar2) break;
//     pcVar1 = (code *)swi(0x16);
//     (*pcVar1)();
//   }
//   FUN_410e_047c();
//   FUN_410e_047c();
//   FUN_410e_0475();
//   pcVar1 = (code *)swi(0x23);
//   (*pcVar1)();
//   FUN_410e_0097();
//   FUN_410e_00e5();
//   *(undefined1 *)0xeb08 = *(undefined1 *)0xeb12;
//   return;
// }
// 
// --- end reference ---
procedure FUN_410e_0143;
begin
  { TODO: translate from asm/FUN_410e_0143.s — UNMATCHED until an oracle passes }
end;

