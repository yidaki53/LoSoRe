{ stickman::FUN_40a5_0000 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_40a5_0000.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_40a5_0000.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void FUN_40a5_0000(byte param_1)
// 
// {
//   undefined1 extraout_AH;
//   int iVar1;
//   undefined2 unaff_DS;
//   
//   FUN_42b5_04df();
//   iVar1 = CONCAT11(extraout_AH,param_1);
//   *(byte *)0x15c = param_1;
//   if (*(char *)0x15a != '\0') {
//     iVar1 = param_1 + 0x80;
//     param_1 = (byte)iVar1;
//   }
//   FUN_410e_0257(CONCAT11((char)((uint)iVar1 >> 8),param_1));
//   if (*(char *)0x15b != '\0') {
//     FUN_410e_028f();
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_40a5_0000(param_1: Byte);
begin
  { TODO: translate from asm/FUN_40a5_0000.s — UNMATCHED until an oracle passes }
end;

