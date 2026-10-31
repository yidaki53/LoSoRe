{ stickman::FUN_410e_028f — game Pascal draft (oracle: none).
  Drafted from asm/FUN_410e_028f.s via c->pascal+llm(qwen2.5-coder:14b-instruct,Ghidra); UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_410e_028f.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16far FUN_410e_028f(void)
// 
// {
//   undefined2 unaff_DS;
//   
//   *(byte *)0xeb08 = *(byte *)0xeb08 | 8;
//   return;
// }
// 
// --- end reference ---
procedure FUN_410e_028f;
var
  p: ^Byte;
begin
  p := ^Byte($EB08);
  p^ := p^ or $08;
end;
