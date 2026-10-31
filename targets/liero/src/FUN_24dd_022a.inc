{ liero::FUN_24dd_022a — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_022a.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_022a.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void FUN_24dd_022a(void)
// 
// {
//   code *pcVar1;
//   
//   pcVar1 = (code *)swi(0x21);
//   (*pcVar1)();
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_022a;
var
  digit: Byte;
begin
  digit := Byte(RegisterAX) + Ord('0');
  if digit >= Ord(':') then
    Inc(digit, 7);
  FUN_24dd_0232(digit);
end;
