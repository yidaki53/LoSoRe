{ liero::FUN_1ec2_09e7 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1ec2_09e7.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1ec2_09e7.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far
// FUN_1ec2_09e7(undefined4 param_1,int param_2,int param_3,int param_4,int param_5)
// 
// {
//   uint uVar1;
//   uint uVar2;
//   int iVar3;
//   int iVar4;
//   int iVar5;
//   int iVar6;
//   undefined2 uVar7;
//   int local_8;
//   int local_6;
//   int local_4;
//   
//   local_4 = param_5;
//   local_6 = param_4;
//   uVar1 = param_3 - param_5;
//   uVar2 = param_2 - param_4;
//   iVar3 = FUN_1ec2_09bd(&stack0xfffe,uVar1);
//   iVar4 = FUN_1ec2_09bd(&stack0xfffe,uVar2);
//   iVar5 = (uVar1 ^ (int)uVar1 >> 0xf) - ((int)uVar1 >> 0xf);
//   iVar6 = (uVar2 ^ (int)uVar2 >> 0xf) - ((int)uVar2 >> 0xf);
//   uVar7 = (undefined2)((ulong)param_1 >> 0x10);
//   if (iVar6 < iVar5) {
//     local_8 = -(iVar5 / 2);
//     while (local_4 != param_3) {
//       local_8 = local_8 + iVar6;
//       local_4 = local_4 + iVar3;
//       if (0 < local_8) {
//         local_6 = local_6 + iVar4;
//         local_8 = local_8 - iVar5;
//       }
//       FUN_1ec2_0e4a((int)param_1,uVar7,local_6,local_4);
//     }
//   }
//   else {
//     local_8 = -(iVar6 / 2);
//     while (local_6 != param_2) {
//       local_8 = local_8 + iVar5;
//       local_6 = local_6 + iVar4;
//       if (0 < local_8) {
//         local_4 = local_4 + iVar3;
//         local_8 = local_8 - iVar6;
//       }
//       FUN_1ec2_0e4a((int)param_1,uVar7,local_6,local_4);
//     }
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_1ec2_09e7;
begin
  { TODO: translate from asm/FUN_1ec2_09e7.s — UNMATCHED until an oracle passes }
end;

