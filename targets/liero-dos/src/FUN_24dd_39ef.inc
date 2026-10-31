{ liero-dos::FUN_24dd_39ef — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_39ef.s via c->pascal+llm(http://localhost:8080,Ghidra); UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_39ef.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// /* WARNING: Removing unreachable block (ram,0x000287df) */
// /* WARNING: Removing unreachable block (ram,0x000287e6) */
// /* WARNING: Removing unreachable block (ram,0x000287e8) */
// 
// undefined2 __cdecl16far FUN_24dd_39ef(void)
// 
// {
//   FUN_24dd_37ec();
//   return 0;
// }
// 
// --- end reference ---
function FUN_24dd_39ef: Word;
begin
  FUN_24dd_37ec;
  FUN_24dd_39ef := 0;
end;
