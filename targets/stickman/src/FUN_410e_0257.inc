{ stickman::FUN_410e_0257 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_410e_0257.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_410e_0257.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_410e_0257(byte param_1)
// 
// {
//   undefined2 unaff_DS;
//   
//   if ((param_1 & 0xf0) != 0) {
//     param_1 = param_1 & 0xf | 0x80;
//   }
//   *(byte *)0xeb08 = *(byte *)0xeb08 & 0x70;
//   *(byte *)0xeb08 = *(byte *)0xeb08 | param_1;
//   return;
// }
// 
// --- end reference ---
procedure FUN_410e_0257(param_1: Byte);
begin
  { TODO: translate from asm/FUN_410e_0257.s — UNMATCHED until an oracle passes }
end;

