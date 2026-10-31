{ stickman::FUN_410e_0097 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_410e_0097.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_410e_0097.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_410e_0097(void)
// 
// {
//   undefined2 in_AX;
//   char extraout_DL;
//   
//   DAT_0000_0487 = DAT_0000_0487 & 0xfe;
//   if (((byte)in_AX != 7) && (3 < (byte)in_AX)) {
//     in_AX = CONCAT11((char)((uint)in_AX >> 8),3);
//   }
//   FUN_410e_0609();
//   if ((char)((uint)in_AX >> 8) != '\0') {
//     FUN_410e_0609();
//     FUN_410e_0609();
//     if (extraout_DL == '*') {
//       DAT_0000_0487 = DAT_0000_0487 | 1;
//       FUN_410e_0609();
//       FUN_410e_0609();
//     }
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_410e_0097;
begin
  { TODO: translate from asm/FUN_410e_0097.s — UNMATCHED until an oracle passes }
end;

