{ stickman::FUN_42b5_0a50 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_42b5_0a50.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_42b5_0a50.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far
// FUN_42b5_0a50(int param_1,int param_2,undefined2 param_3,undefined2 param_4,undefined2 param_5,
//              undefined4 param_6)
// 
// {
//   int iVar1;
//   undefined1 uVar2;
//   
//   uVar2 = param_1 == 0;
//   if (param_1 < 0) {
//     param_1 = 6 - param_2;
//     uVar2 = param_1 == -2;
//     if (-2 < param_1) {
//       param_1 = -2;
//     }
//   }
//   FUN_42b5_141f();
//   FUN_42b5_07b6();
//   if ((bool)uVar2) {
//     iVar1 = param_2 - param_1;
//     if (iVar1 != 0 && param_1 <= param_2) {
//       do {
//         FUN_42b5_07da();
//         iVar1 = iVar1 + -1;
//       } while (iVar1 != 0);
//     }
//     do {
//       FUN_42b5_07da();
//       param_1 = param_1 + -1;
//     } while (param_1 != 0);
//   }
//   *(undefined2 *)((int)param_6 + 8) = param_4;
//   return;
// }
// 
// --- end reference ---
procedure FUN_42b5_0a50(param_1, param_2: Integer; param_3, param_4, param_5: Word; param_6: Longint);
begin
  { TODO: translate from asm/FUN_42b5_0a50.s — UNMATCHED until an oracle passes }
end;

