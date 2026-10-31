{ stickman::FUN_428f_00f7 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_428f_00f7.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_428f_00f7.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// long __stdcall16far FUN_428f_00f7(void)
// 
// {
//   code *pcVar1;
//   long lVar2;
//   int iVar3;
//   int in_CX;
//   ulong uVar4;
//   
//   pcVar1 = (code *)swi(0x21);
//   uVar4 = (*pcVar1)();
//   iVar3 = (int)uVar4;
//   lVar2 = CONCAT22(iVar3,iVar3);
//   if (iVar3 != -1) {
//     lVar2 = (ulong)(uint)(iVar3 * in_CX) * (uVar4 >> 0x10);
//   }
//   return lVar2;
// }
// 
// --- end reference ---
function FUN_428f_00f7: Longint;
begin
  { TODO: translate from asm/FUN_428f_00f7.s — UNMATCHED until an oracle passes }
end;

