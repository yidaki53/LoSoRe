{ liero::FUN_1ec2_0000 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1ec2_0000.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1ec2_0000.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_1ec2_0000(uint param_1,undefined4 *param_2,undefined4 *param_3)
// 
// {
//   undefined4 *puVar1;
//   undefined4 *puVar2;
//   undefined4 *puVar3;
//   undefined4 *puVar4;
//   
//   puVar3 = (undefined4 *)param_3;
//   puVar4 = (undefined4 *)param_2;
//   for (param_1 = param_1 >> 2; param_1 != 0; param_1 = param_1 - 1) {
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
procedure FUN_1ec2_0000;
begin
  { TODO: translate from asm/FUN_1ec2_0000.s — UNMATCHED until an oracle passes }
end;

