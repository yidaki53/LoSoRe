{ liero::FUN_2000_87bf — game Pascal draft (oracle: none).
  Drafted from asm/FUN_2000_87bf.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_2000_87bf.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// /* WARNING: Removing unreachable block (ram,0x000287df) */
// /* WARNING: Removing unreachable block (ram,0x000287e6) */
// /* WARNING: Removing unreachable block (ram,0x000287e8) */
// 
// undefined2 __cdecl16far FUN_2000_87bf(void)
// 
// {
//   FUN_24dd_37ec();
//   return 0;
// }
// 
// --- end reference ---
function FUN_2000_87bf: Word;
begin
  { TODO: not recovered. The retained 55-byte body branches into uncaptured
    blocks at 2000:87e8..87f2 and calls uncaptured routines at 2000:85bc and
    2000:9502; their effects and all return paths cannot be established. }
end;
