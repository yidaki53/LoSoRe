{ liero::FUN_1ec2_00a5 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1ec2_00a5.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1ec2_00a5.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_1ec2_00a5(int param_1,int param_2,undefined1 *param_3,undefined1 *param_4)
// 
// {
//   undefined1 *puVar1;
//   undefined1 *puVar2;
//   int iVar3;
//   undefined1 *puVar4;
//   undefined1 *puVar5;
//   
//   puVar5 = (undefined1 *)param_3;
//   puVar4 = (undefined1 *)param_4;
//   iVar3 = param_2;
//   do {
//     for (; iVar3 != 0; iVar3 = iVar3 + -1) {
//       puVar2 = puVar5;
//       puVar5 = puVar5 + 1;
//       puVar1 = puVar4;
//       puVar4 = puVar4 + 1;
//       *puVar2 = *puVar1;
//     }
//     puVar5 = puVar5 + (0x140 - param_2);
//     puVar4 = puVar4 + (0x140 - param_2);
//     param_1 = param_1 + -1;
//     iVar3 = param_2;
//   } while (param_1 != 0);
//   return;
// }
// 
// --- end reference ---
procedure FUN_1ec2_00a5;
begin
  { TODO: translate from asm/FUN_1ec2_00a5.s — UNMATCHED until an oracle passes }
end;

