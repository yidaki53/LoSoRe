{ liero::FUN_1ec2_0d88 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1ec2_0d88.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1ec2_0d88.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_1ec2_0d88(undefined1 param_1,int param_2,int param_3,undefined1 *param_4)
// 
// {
//   undefined1 *puVar1;
//   int iVar2;
//   undefined1 *puVar3;
//   undefined2 uVar4;
//   
//   uVar4 = (undefined2)((ulong)param_4 >> 0x10);
//   param_2 = param_2 + -2;
//   puVar3 = (undefined1 *)param_4;
//   for (iVar2 = param_3 + -2; iVar2 != 0; iVar2 = iVar2 + -1) {
//     puVar3[1] = param_1;
//     puVar3 = puVar3 + 1;
//   }
//   puVar3 = puVar3 + -param_3 + 0x142;
//   iVar2 = param_3;
//   do {
//     for (; iVar2 != 0; iVar2 = iVar2 + -1) {
//       puVar1 = puVar3;
//       puVar3 = puVar3 + 1;
//       *puVar1 = param_1;
//     }
//     puVar3 = puVar3 + -param_3 + 0x140;
//     param_2 = param_2 + -1;
//     iVar2 = param_3;
//   } while (param_2 != 0);
//   for (param_3 = param_3 + -2; puVar3 = puVar3 + 1, param_3 != 0; param_3 = param_3 + -1) {
//     *puVar3 = param_1;
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_1ec2_0d88;
begin
  { TODO: translate from asm/FUN_1ec2_0d88.s — UNMATCHED until an oracle passes }
end;

