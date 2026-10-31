{ liero::FUN_24dd_0232 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_0232.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_0232.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_24dd_0232(void)
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
procedure FUN_24dd_0232(param_1: Word);
begin
  DosOutputBuffer[DosOutputCount] := Byte(param_1);
  Inc(DosOutputCount);
  RegisterDX := (RegisterDX and $FF00) or Byte(param_1);
  RegisterAX := $0600 or Byte(param_1);
end;
