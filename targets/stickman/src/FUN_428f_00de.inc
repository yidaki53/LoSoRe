{ stickman::FUN_428f_00de — game Pascal draft (oracle: none).
  Drafted from asm/FUN_428f_00de.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_428f_00de.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// long __stdcall16far FUN_428f_00de(void)
// 
// {
//   code *pcVar1;
//   long lVar2;
//   int iVar3;
//   int in_CX;
//   uint in_BX;
//   
//   pcVar1 = (code *)swi(0x21);
//   iVar3 = (*pcVar1)();
//   lVar2 = CONCAT22(iVar3,iVar3);
//   if (iVar3 != -1) {
//     lVar2 = (ulong)(uint)(iVar3 * in_CX) * (ulong)in_BX;
//   }
//   return lVar2;
// }
// 
// --- end reference ---
function FUN_428f_00de: Longint;
begin
  { TODO: translate from asm/FUN_428f_00de.s — UNMATCHED until an oracle passes }
end;

