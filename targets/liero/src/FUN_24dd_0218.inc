{ liero::FUN_24dd_0218 — scoped original-error-exit formatting oracle.
  Both original fall-through byte conversions print four hexadecimal digits.
  Finite corpus and host output port are not full native register/ABI parity.
  Original assembly retained in asm/FUN_24dd_0218.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void FUN_24dd_0218(void)
// 
// {
//   code *pcVar1;
//   
//   FUN_24dd_021f();
//   FUN_24dd_022a();
//   pcVar1 = (code *)swi(0x21);
//   (*pcVar1)();
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_0218;
var
  originalAX: Word;
begin
  originalAX := RegisterAX;
  RegisterAX := (originalAX and $FF00) or (originalAX shr 8);
  FUN_24dd_021f;
  RegisterAX := originalAX;
  FUN_24dd_021f;
end;
