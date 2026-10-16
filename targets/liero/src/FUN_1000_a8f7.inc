{ liero::FUN_1000_a8f7 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_a8f7.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_a8f7.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void FUN_1000_a8f7(undefined2 param_1,int *param_2,byte *param_3)
// 
// {
//   byte *pbVar1;
//   uint uVar2;
//   uint uVar3;
//   uint uVar4;
//   int iVar5;
//   byte *pbVar6;
//   int *piVar7;
//   undefined2 uVar8;
//   undefined2 unaff_SS;
//   bool bVar9;
//   uint local_10a;
//   int local_108;
//   byte local_102 [252];
//   undefined2 uStack_6;
//   undefined2 uStack_4;
//   
//   uStack_4 = 0x1000;
//   uStack_6 = 0xa902;
//   FUN_24dd_0530();
//   pbVar6 = (byte *)param_3;
//   local_102[0] = *param_3;
//   pbVar1 = local_102;
//   for (uVar4 = (uint)local_102[0]; pbVar1 = pbVar1 + 1, pbVar6 = pbVar6 + 1, uVar4 != 0;
//       uVar4 = uVar4 - 1) {
//     *pbVar1 = *pbVar6;
//   }
//   uVar8 = (undefined2)((ulong)param_2 >> 0x10);
//   piVar7 = (int *)param_2;
//   *param_2 = 0;
//   piVar7[1] = 0;
//   uVar4 = (uint)local_102[0];
//   if (uVar4 != 0) {
//     local_10a = 1;
//     local_108 = 0;
//     while( true ) {
//       iVar5 = piVar7[1];
//       uVar2 = FUN_24dd_3d80();
//       uVar3 = local_102[local_10a] - 0x30;
//       *param_2 = uVar3 + uVar2;
//       piVar7[1] = ((int)uVar3 >> 0xf) + iVar5 + (uint)CARRY2(uVar3,uVar2);
//       if ((local_108 == 0) && (local_10a == uVar4)) break;
//       bVar9 = 0xfffe < local_10a;
//       local_10a = local_10a + 1;
//       local_108 = local_108 + (uint)bVar9;
//     }
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_1000_a8f7;
begin
  { TODO: translate from asm/FUN_1000_a8f7.s — UNMATCHED until an oracle passes }
end;

