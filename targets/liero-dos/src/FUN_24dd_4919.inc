{ liero-dos::FUN_24dd_4919 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_4919.s via c->pascal+llm(http://localhost:8080,Ghidra); UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_4919.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// byte __stdcall16far FUN_24dd_4919(byte param_1)
// 
// {
//   if ((0x60 < param_1) && (param_1 < 0x7b)) {
//     param_1 = param_1 - 0x20;
//   }
//   return param_1;
// }
// 
// --- end reference ---
function FUN_24dd_4919(param_1: Byte): Byte;
begin
  if (param_1 > 96) and (param_1 < 123) then
    param_1 := param_1 - 32;
  FUN_24dd_4919 := param_1;
end;
