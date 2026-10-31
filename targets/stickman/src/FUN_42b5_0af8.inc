{ stickman::FUN_42b5_0af8 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_42b5_0af8.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_42b5_0af8.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_42b5_0af8(int param_1,undefined1 *param_2,undefined1 *param_3)
// 
// {
//   undefined1 *puVar1;
//   undefined1 *puVar2;
//   undefined1 *puVar3;
//   undefined1 *puVar4;
//   
//   puVar3 = (undefined1 *)param_3;
//   puVar4 = (undefined1 *)param_2;
//   for (; param_1 != 0; param_1 = param_1 + -1) {
//     puVar2 = puVar4;
//     puVar4 = puVar4 + 1;
//     puVar1 = puVar3;
//     puVar3 = puVar3 + 1;
//     *puVar2 = *puVar1;
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_42b5_0af8(param_1: Integer; param_2, param_3: Pointer);
begin
  { TODO: translate from asm/FUN_42b5_0af8.s — UNMATCHED until an oracle passes }
end;

