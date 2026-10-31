{ liero::FUN_235c_04f3 — assembly-derived Pascal reconstruction
  (oracle: raw assembly review; guarded host memory test).
  Original assembly retained in asm/FUN_235c_04f3.s.
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
//
// void __cdecl16far FUN_235c_04f3(void)
//
// {
//   undefined2 unaff_DS;
//
//   *(undefined1 *)0x7690 = 0;
//   *(undefined1 *)0x7692 = 0;
//   return;
// }
//
// --- end reference ---
procedure FUN_235c_04f3;
begin
  DosMemory[$7690] := 0;
  DosMemory[$7692] := 0;
end;
