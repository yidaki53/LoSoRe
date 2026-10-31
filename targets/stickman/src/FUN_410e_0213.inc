{ stickman::FUN_410e_0213 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_410e_0213.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_410e_0213.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_410e_0213(char param_1,char param_2)
// 
// {
//   undefined2 unaff_DS;
//   
//   if ((((!CARRY1(param_2 - 1U,*(byte *)0xeb0a)) &&
//        ((byte)((param_2 - 1U) + *(byte *)0xeb0a) <= *(byte *)0xeb0c)) &&
//       (!CARRY1(param_1 - 1U,*(byte *)0xeb0b))) &&
//      ((byte)((param_1 - 1U) + *(byte *)0xeb0b) <= *(byte *)0xeb0d)) {
//     thunk_FUN_410e_0609();
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_410e_0213(param_1, param_2: Char);
begin
  { TODO: translate from asm/FUN_410e_0213.s — UNMATCHED until an oracle passes }
end;

