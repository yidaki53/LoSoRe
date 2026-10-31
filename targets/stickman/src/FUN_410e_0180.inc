{ stickman::FUN_410e_0180 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_410e_0180.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_410e_0180.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_410e_0180(byte param_1,byte param_2,byte param_3,byte param_4)
// 
// {
//   undefined2 unaff_DS;
//   
//   if ((((param_4 <= param_2) && (param_3 <= param_1)) && (-1 < (char)(param_4 - 1))) &&
//      (((-1 < (char)(param_3 - 1) && ((byte)(param_2 - 1) <= *(byte *)0xeb10)) &&
//       ((byte)(param_1 - 1) <= *(byte *)0xeb11)))) {
//     *(undefined2 *)0xeb0a = CONCAT11(param_3 - 1,param_4 - 1);
//     *(undefined2 *)0xeb0c = CONCAT11(param_1 - 1,param_2 - 1);
//     thunk_FUN_410e_0609();
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_410e_0180(param_1, param_2, param_3, param_4: Byte);
begin
  { TODO: translate from asm/FUN_410e_0180.s — UNMATCHED until an oracle passes }
end;

