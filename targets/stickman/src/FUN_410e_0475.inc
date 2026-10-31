{ stickman::FUN_410e_0475 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_410e_0475.s via c->pascal+llm(qwen2.5-coder:14b-instruct,Ghidra); UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_410e_0475.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// /* WARNING: Removing unreachable block (ram,0x000415a4) */
// /* WARNING: Removing unreachable block (ram,0x0004159a) */
// /* WARNING: Removing unreachable block (ram,0x000415a0) */
// /* WARNING: Removing unreachable block (ram,0x00041575) */
// /* WARNING: Removing unreachable block (ram,0x0004158d) */
// /* WARNING: Removing unreachable block (ram,0x00041593) */
// 
// void FUN_410e_0475(void)
// 
// {
//   FUN_410e_047c();
//   thunk_FUN_410e_0609();
//   FUN_410e_04d5();
//   thunk_FUN_410e_0609();
//   return;
// }
// 
// --- end reference ---
procedure FUN_410e_0475;
begin
  FUN_410e_047c;
  FUN_410e_04d5;
end;
