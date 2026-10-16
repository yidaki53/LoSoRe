{ liero::FUN_1ec2_0d5d — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1ec2_0d5d.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1ec2_0d5d.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_1ec2_0d5d(undefined1 param_1,int param_2,uint param_3,undefined1 *param_4)
// 
// {
//   undefined1 *puVar1;
//   uint uVar2;
//   undefined1 *puVar3;
//   
//   puVar3 = (undefined1 *)param_4;
//   uVar2 = param_3;
//   do {
//     for (uVar2 = uVar2 | param_3; uVar2 != 0; uVar2 = uVar2 - 1) {
//       puVar1 = puVar3;
//       puVar3 = puVar3 + 1;
//       *puVar1 = param_1;
//     }
//     puVar3 = puVar3 + (0x140 - param_3);
//     param_2 = param_2 + -1;
//     uVar2 = 0;
//   } while (param_2 != 0);
//   return;
// }
// 
// --- end reference ---
procedure FUN_1ec2_0d5d;
begin
  { TODO: translate from asm/FUN_1ec2_0d5d.s — UNMATCHED until an oracle passes }
end;

