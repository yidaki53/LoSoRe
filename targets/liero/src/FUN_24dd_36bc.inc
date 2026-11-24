{ liero::FUN_24dd_36bc — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_36bc.s via asm->pascal+llm(qwen2.5-coder:14b-instruct-q4_K_M,Ghidra); UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_36bc.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void FUN_24dd_36bc(void)
// 
// {
//   FUN_24dd_36c4();
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_36bc(objectPointer: Pointer);
begin
  RegisterDX := $D7B2;
  FUN_24dd_36c4(objectPointer);
end;
