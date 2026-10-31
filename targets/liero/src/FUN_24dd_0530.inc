{ liero::FUN_24dd_0530 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_0530.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_0530.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16far FUN_24dd_0530(void)
// 
// {
//   uint in_AX;
//   undefined2 unaff_DS;
//   
//   if (((in_AX < 0xfe00) && ((undefined1 *)(in_AX + 0x200) < &stack0x0000)) &&
//      (*(uint *)0x640e <= (uint)-((int)(in_AX + 0x200) - (int)&stack0x0000))) {
//     return;
//   }
//   FUN_24dd_010f();
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_0530;
var
  requestedStack: Word;
  availableStack: Word;
  minimumStack: Word;
begin
  if RegisterAX > $FDFF then
  begin
    RunError(202);
    Exit;
  end;
  requestedStack := RegisterAX + $0200;
  if requestedStack >= RegisterSP then
  begin
    RunError(202);
    Exit;
  end;
  availableStack := RegisterSP - requestedStack;
  minimumStack := Word(DosMemory[$640E]) or
    (Word(DosMemory[$640F]) shl 8);
  if availableStack < minimumStack then
  begin
    RunError(202);
    Exit;
  end;
end;
