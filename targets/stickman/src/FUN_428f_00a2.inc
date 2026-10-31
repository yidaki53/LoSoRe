{ stickman::FUN_428f_00a2 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_428f_00a2.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_428f_00a2.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_428f_00a2(uint *param_1,uint *param_2,uint *param_3,uint *param_4)
// 
// {
//   code *pcVar1;
//   byte in_CL;
//   byte in_CH;
//   byte extraout_DL;
//   byte extraout_DH;
//   
//   pcVar1 = (code *)swi(0x21);
//   (*pcVar1)();
//   *param_1 = (uint)extraout_DL;
//   *param_2 = (uint)extraout_DH;
//   *param_3 = (uint)in_CL;
//   *param_4 = (uint)in_CH;
//   return;
// }
// 
// --- end reference ---
procedure FUN_428f_00a2(param_1, param_2, param_3, param_4: Pointer);
begin
  { TODO: translate from asm/FUN_428f_00a2.s — UNMATCHED until an oracle passes }
end;

