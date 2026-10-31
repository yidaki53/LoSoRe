{ stickman::FUN_42b5_1a42 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_42b5_1a42.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_42b5_1a42.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_42b5_1a42(undefined1 param_1,int param_2,undefined1 *param_3)
// 
// {
//   undefined1 *puVar1;
//   undefined1 *puVar2;
//   
//   puVar2 = (undefined1 *)param_3;
//   for (; param_2 != 0; param_2 = param_2 + -1) {
//     puVar1 = puVar2;
//     puVar2 = puVar2 + 1;
//     *puVar1 = param_1;
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_42b5_1a42(param_1: Byte; param_2: Integer; param_3: Pointer);
begin
  { TODO: translate from asm/FUN_42b5_1a42.s — UNMATCHED until an oracle passes }
end;

