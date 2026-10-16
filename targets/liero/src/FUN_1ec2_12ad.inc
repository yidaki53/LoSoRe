{ liero::FUN_1ec2_12ad — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1ec2_12ad.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1ec2_12ad.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far
// FUN_1ec2_12ad(undefined4 param_1,undefined1 param_2,int param_3,uint param_4,int param_5)
// 
// {
//   undefined2 *puVar1;
//   uint uVar2;
//   undefined2 *puVar3;
//   undefined2 uVar4;
//   
//   uVar4 = (undefined2)((ulong)param_1 >> 0x10);
//   puVar3 = (undefined2 *)((int)param_1 + param_3 * 0x140 + param_5);
//   uVar2 = param_4 >> 1;
//   if ((param_4 & 1) != 0) {
//     puVar1 = puVar3;
//     puVar3 = (undefined2 *)((int)puVar3 + 1);
//     *(undefined1 *)puVar1 = param_2;
//   }
//   for (; uVar2 != 0; uVar2 = uVar2 - 1) {
//     puVar1 = puVar3;
//     puVar3 = puVar3 + 1;
//     *puVar1 = CONCAT11(param_2,param_2);
//   }
//   puVar3 = (undefined2 *)((int)puVar3 + (0x140 - param_4));
//   uVar2 = param_4 >> 1;
//   if ((param_4 & 1) != 0) {
//     puVar1 = puVar3;
//     puVar3 = (undefined2 *)((int)puVar3 + 1);
//     *(undefined1 *)puVar1 = param_2;
//   }
//   for (; uVar2 != 0; uVar2 = uVar2 - 1) {
//     puVar1 = puVar3;
//     puVar3 = puVar3 + 1;
//     *puVar1 = CONCAT11(param_2,param_2);
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_1ec2_12ad;
begin
  { TODO: translate from asm/FUN_1ec2_12ad.s — UNMATCHED until an oracle passes }
end;

