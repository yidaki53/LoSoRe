{ liero::FUN_249c_019d — game Pascal draft (oracle: none).
  Drafted from asm/FUN_249c_019d.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_249c_019d.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// char __cdecl16far FUN_249c_019d(void)
// 
// {
//   code *pcVar1;
//   char cVar2;
//   undefined2 unaff_DS;
//   
//   pcVar1 = (code *)swi(0x21);
//   cVar2 = (*pcVar1)();
//   if ((*(char *)0x159c != '\0') && (cVar2 == '\x03')) {
//     pcVar1 = (code *)swi(0x23);
//     (*pcVar1)();
//   }
//   return cVar2;
// }
// 
// --- end reference ---
function FUN_249c_019d: Char;
begin
  { TODO: Not recovered. INT 21h AH=07h reads the DOS console, and INT 23h
    performs the Ctrl-C handler transfer; neither interrupt is modeled here. }
end;
