{ liero::FUN_24dd_4141 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_4141.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_4141.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_24dd_4141(uint param_1,undefined1 *param_2,undefined4 param_3)
// 
// {
//   undefined1 *puVar1;
//   undefined1 *puVar2;
//   undefined1 *puVar3;
//   undefined1 *puVar4;
//   
//   puVar4 = (undefined1 *)param_2;
//   puVar3 = (undefined1 *)((int)param_3 + (param_1 >> 8));
//   for (param_1 = param_1 & 0xff; param_1 != 0; param_1 = param_1 - 1) {
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
procedure FUN_24dd_4141;
begin
  { TODO: translate from asm/FUN_24dd_4141.s — UNMATCHED until an oracle passes }
end;

