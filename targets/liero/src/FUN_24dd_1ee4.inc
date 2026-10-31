{ liero::FUN_24dd_1ee4 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_1ee4.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_1ee4.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_24dd_1ee4(void)
// 
// {
//   int in_BX;
//   undefined2 unaff_DS;
//   char in_CF;
//   
//   *(char *)(in_BX + 0x5e) = (*(char *)(in_BX + 0x5e) - (char)in_BX) - in_CF;
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_1ee4;
var
  memoryOffset: Word;
  borrow: Byte;
begin
  memoryOffset := RegisterBX + $5E;
  if RegisterCarryFlag then
    borrow := 1
  else
    borrow := 0;
  DosMemory[memoryOffset] :=
    Byte(DosMemory[memoryOffset] - Byte(RegisterBX) - borrow);
end;
