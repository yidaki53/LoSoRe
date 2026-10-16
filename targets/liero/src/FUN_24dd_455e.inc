{ liero::FUN_24dd_455e — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_455e.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_455e.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_24dd_455e(void)
// 
// {
//   uint uVar1;
//   uint in_AX;
//   uint in_DX;
//   bool bVar2;
//   
//   if (in_AX != 0 || in_DX != 0) {
//     if ((int)in_DX < 0) {
//       bVar2 = in_AX != 0;
//       in_AX = -in_AX;
//       in_DX = -(uint)bVar2 - in_DX;
//     }
//     uVar1 = in_AX;
//     if ((in_DX == 0) && (uVar1 = 0, in_DX = in_AX, (char)(in_AX >> 8) == '\0')) {
//       in_DX = in_AX << 8;
//     }
//     while (-1 < (int)in_DX) {
//       in_DX = in_DX * 2 + (uint)CARRY2(uVar1,uVar1);
//       uVar1 = uVar1 * 2;
//     }
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_455e;
begin
  { TODO: translate from asm/FUN_24dd_455e.s — UNMATCHED until an oracle passes }
end;

