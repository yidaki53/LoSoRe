{ liero::FUN_2494_001e — game Pascal draft (oracle: none).
  Drafted from asm/FUN_2494_001e.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_2494_001e.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined2 __cdecl16far FUN_2494_001e(void)
// 
// {
//   undefined2 extraout_DX;
//   undefined2 unaff_DS;
//   
//   (*(code *)*(undefined2 *)0x7838)(0x2494);
//   return extraout_DX;
// }
// 
// --- end reference ---
function FUN_2494_001e: Word;
begin
  { TODO: Not recovered. The routine invokes the DOS input service through the
    interrupt vector at DS:7838; no DOS interrupt/vector model is available. }
end;
