{ stickman::FUN_428f_006c — game Pascal draft (oracle: none).
  Drafted from asm/FUN_428f_006c.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_428f_006c.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_428f_006c(uint *param_1,uint *param_2,uint *param_3,undefined2 *param_4)
// 
// {
//   code *pcVar1;
//   uint uVar2;
//   undefined2 in_CX;
//   byte extraout_DL;
//   byte extraout_DH;
//   
//   pcVar1 = (code *)swi(0x21);
//   uVar2 = (*pcVar1)();
//   *param_1 = uVar2 & 0xff;
//   *param_2 = (uint)extraout_DL;
//   *param_3 = (uint)extraout_DH;
//   *param_4 = in_CX;
//   return;
// }
// 
// --- end reference ---
procedure FUN_428f_006c(param_1, param_2, param_3, param_4: Pointer);
begin
  { TODO: translate from asm/FUN_428f_006c.s — UNMATCHED until an oracle passes }
end;

