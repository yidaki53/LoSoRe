{ liero::FUN_249c_0180 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_249c_0180.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_249c_0180.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// uint __cdecl16far FUN_249c_0180(void)
// 
// {
//   code *pcVar1;
//   uint uVar2;
//   uint uVar3;
//   
//   pcVar1 = (code *)swi(0x21);
//   uVar2 = (*pcVar1)();
//   uVar3 = uVar2 & 0xff00;
//   if ((char)uVar2 == -1) {
//     uVar3 = uVar3 + 1;
//   }
//   return uVar3;
// }
// 
// --- end reference ---
function FUN_249c_0180: Word;
begin
  { TODO: Not recovered. INT 21h AH=0Bh reads live DOS keyboard status, which
    the host runtime does not model; no synthetic result is assigned. }
end;
