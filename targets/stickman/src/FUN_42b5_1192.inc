{ stickman::FUN_42b5_1192 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_42b5_1192.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_42b5_1192.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_42b5_1192(void)
// 
// {
//   uint in_AX;
//   uint uVar1;
//   uint in_DX;
//   
//   if (in_AX != 0 || in_DX != 0) {
//     if ((int)in_DX < 0) {
//       uVar1 = ~in_AX;
//       in_AX = uVar1 + 1;
//       in_DX = ~in_DX + (uint)(0xfffe < uVar1);
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
procedure FUN_42b5_1192;
begin
  { TODO: translate from asm/FUN_42b5_1192.s — UNMATCHED until an oracle passes }
end;

