{ liero::FUN_235c_1380 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_235c_1380.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_235c_1380.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// bool __cdecl16far FUN_235c_1380(void)
// 
// {
//   code *pcVar1;
//   char cVar2;
//   
//   pcVar1 = (code *)swi(0x2f);
//   cVar2 = (*pcVar1)();
//   return cVar2 == -0x80;
// }
// 
// --- end reference ---
function FUN_235c_1380: Boolean;
begin
  { TODO: Not recovered. INT 2Fh AX=4300h availability semantics are not
    provided by the host runtime; no synthetic result is assigned. }
end;
