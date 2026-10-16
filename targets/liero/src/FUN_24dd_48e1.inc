{ liero::FUN_24dd_48e1 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_48e1.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_48e1.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_24dd_48e1(int param_1,undefined1 *param_2,undefined1 *param_3)
// 
// {
//   undefined1 *puVar1;
//   undefined1 *puVar2;
//   undefined1 *puVar3;
//   undefined1 *puVar4;
//   byte bVar5;
//   
//   puVar3 = (undefined1 *)param_3;
//   puVar4 = (undefined1 *)param_2;
//   bVar5 = 0;
//   if (puVar3 < puVar4) {
//     puVar3 = puVar3 + param_1 + -1;
//     puVar4 = puVar4 + param_1 + -1;
//     bVar5 = 1;
//   }
//   for (; param_1 != 0; param_1 = param_1 + -1) {
//     puVar2 = puVar4;
//     puVar4 = puVar4 + (uint)bVar5 * -2 + 1;
//     puVar1 = puVar3;
//     puVar3 = puVar3 + (uint)bVar5 * -2 + 1;
//     *puVar2 = *puVar1;
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_48e1;
begin
  { TODO: translate from asm/FUN_24dd_48e1.s — UNMATCHED until an oracle passes }
end;

