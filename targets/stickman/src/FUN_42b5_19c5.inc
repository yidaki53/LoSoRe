{ stickman::FUN_42b5_19c5 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_42b5_19c5.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_42b5_19c5.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// ulong __stdcall16far FUN_42b5_19c5(void)
// 
// {
//   uint uVar1;
//   uint uVar2;
//   int iVar3;
//   uint in_CX;
//   uint uVar4;
//   int iVar5;
//   uint in_BX;
//   undefined1 in_CF;
//   ulong uVar6;
//   
//   uVar6 = FUN_42b5_19da();
//   uVar4 = (uint)(uVar6 >> 0x10);
//   if (!(bool)in_CF) {
//     iVar3 = (uint)uVar6 - in_CX;
//     uVar1 = (uint)((uint)uVar6 < in_CX);
//     uVar2 = uVar4 - in_BX;
//     iVar5 = uVar2 - uVar1;
//     uVar6 = CONCAT22(iVar5,iVar3);
//     if (in_BX <= uVar4 && uVar1 <= uVar2) {
//       return CONCAT22(iVar5,CONCAT11((char)((uint)iVar3 >> 8),1));
//     }
//   }
//   return uVar6 & 0xffffff00;
// }
// 
// --- end reference ---
function FUN_42b5_19c5: Word;
begin
  { TODO: translate from asm/FUN_42b5_19c5.s — UNMATCHED until an oracle passes }
end;

