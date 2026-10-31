{ liero::FUN_235c_0361 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_235c_0361.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_235c_0361.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined2 __cdecl16far FUN_235c_0361(void)
// 
// {
//   undefined2 uVar1;
//   
//   uVar1 = FUN_2494_001e();
//   return uVar1;
// }
// 
// --- end reference ---
function FUN_235c_0361: Word;
begin
  FUN_235c_0361 := FUN_2494_001e;
  RegisterAX := FUN_235c_0361;
end;
