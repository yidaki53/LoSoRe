{ liero::FUN_24dd_047d — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_047d.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_047d.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_24dd_047d(void)
// 
// {
//   int iVar1;
//   int iVar2;
//   byte bVar3;
//   int iVar4;
//   undefined2 *in_CX;
//   int in_BX;
//   undefined2 *unaff_DI;
//   int unaff_ES;
//   undefined2 unaff_DS;
//   
//   bVar3 = (byte)((int)in_CX + in_CX[2]);
//   if ((in_BX + in_CX[3] + (uint)(0xf < bVar3) != unaff_ES) ||
//      ((undefined2 *)(CONCAT11((char)((uint)((int)in_CX + in_CX[2]) >> 8),bVar3 - 0x10) & 0xff0f) !=
//       unaff_DI)) {
//     *in_CX = unaff_DI;
//     in_CX[1] = unaff_ES;
//     return;
//   }
//   if ((unaff_ES == *(int *)0x63f0) && (unaff_DI == (undefined2 *)*(undefined2 *)0x63ee)) {
//     *(undefined2 *)0x63ee = in_CX;
//     *(int *)0x63f0 = in_BX;
//     return;
//   }
//   *in_CX = *unaff_DI;
//   in_CX[1] = unaff_DI[1];
//   iVar1 = unaff_DI[3];
//   iVar4 = unaff_DI[2] + in_CX[2];
//   iVar2 = in_CX[3];
//   bVar3 = (byte)iVar4;
//   in_CX[2] = CONCAT11((char)((uint)iVar4 >> 8),bVar3 - 0x10) & 0xff0f;
//   in_CX[3] = iVar1 + iVar2 + (uint)(0xf < bVar3);
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_047d;
begin
  { TODO: translate from asm/FUN_24dd_047d.s — UNMATCHED until an oracle passes }
end;

