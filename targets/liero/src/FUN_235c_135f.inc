{ liero::FUN_235c_135f — reviewed Pascal reconstruction (oracle: host-test).
  Host behavior passed; original-binary parity remains unverified.
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C ---
// 
// void __cdecl16far FUN_235c_135f(void)
// 
// {
//   undefined2 unaff_DS;
//   
//   *(undefined1 *)0x67fa = 0;
//   *(undefined1 *)0x7688 = 0;
//   *(undefined1 *)0x7690 = 0;
//   return;
// }
// 
// --- end reference ---
procedure FUN_235c_135f;
begin
  DosMemory[$67FA] := 0;
  DosMemory[$7688] := 0;
  DosMemory[$7690] := 0;
end;
