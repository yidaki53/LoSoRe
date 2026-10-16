{ liero::FUN_24dd_3e63 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_3e63.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_3e63.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// uint __cdecl16far FUN_24dd_3e63(void)
// 
// {
//   byte bVar1;
//   uint uVar2;
//   uint in_AX;
//   uint in_CX;
//   uint uVar3;
//   uint in_DX;
//   undefined2 unaff_DS;
//   
//   if (*(byte *)0x6420 < 2) {
//     for (uVar3 = in_CX & 0x1f; uVar3 != 0; uVar3 = uVar3 - 1) {
//       uVar2 = in_DX & 1;
//       in_DX = in_DX >> 1;
//       in_AX = (uint)(CONCAT12(uVar2 != 0,in_AX) >> 1);
//     }
//     return in_AX;
//   }
//   bVar1 = (byte)in_CX & 0x1f;
//   return in_AX >> bVar1 | in_DX << 0x10 - bVar1;
// }
// 
// --- end reference ---
procedure FUN_24dd_3e63;
begin
  { TODO: translate from asm/FUN_24dd_3e63.s — UNMATCHED until an oracle passes }
end;

