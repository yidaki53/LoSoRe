{ liero::FUN_24dd_021f — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_021f.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_021f.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void FUN_24dd_021f(void)
// 
// {
//   code *pcVar1;
//   
//   FUN_24dd_022a();
//   pcVar1 = (code *)swi(0x21);
//   (*pcVar1)();
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_021f;
var
  originalAX: Word;
begin
  originalAX := RegisterAX;
  RegisterAX := (originalAX and $FF00) or ((originalAX and $00FF) shr 4);
  FUN_24dd_022a;
  RegisterAX := (originalAX and $FF00) or (originalAX and $000F);
  FUN_24dd_022a;
end;
