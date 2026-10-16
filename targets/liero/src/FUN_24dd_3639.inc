{ liero::FUN_24dd_3639 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_3639.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_3639.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_24dd_3639(byte *param_1,undefined2 *param_2)
// 
// {
//   byte *pbVar1;
//   byte *pbVar2;
//   int iVar3;
//   uint uVar4;
//   byte *pbVar5;
//   undefined2 *puVar6;
//   byte *pbVar7;
//   undefined2 uVar8;
//   
//   uVar8 = (undefined2)((ulong)param_2 >> 0x10);
//   puVar6 = (undefined2 *)param_2;
//   *param_2 = 0;
//   puVar6[1] = 0xd7b0;
//   puVar6[2] = 0x80;
//   puVar6[3] = 0;
//   puVar6[4] = 0;
//   puVar6[5] = 0;
//   puVar6[6] = puVar6 + 0x40;
//   puVar6[7] = uVar8;
//   pbVar7 = (byte *)(puVar6 + 9);
//   puVar6[8] = 0x420c;
//   pbVar7[0] = 0xdd;
//   pbVar7[1] = 0x24;
//   for (iVar3 = 0xe; pbVar7 = pbVar7 + 2, iVar3 != 0; iVar3 = iVar3 + -1) {
//     pbVar7[0] = 0;
//     pbVar7[1] = 0;
//   }
//   uVar4 = 0x4f;
//   pbVar5 = (byte *)param_1 + 1;
//   if (0x4e < *param_1) goto LAB_24dd_367d;
//   for (uVar4 = (uint)*param_1; uVar4 != 0; uVar4 = uVar4 - 1) {
// LAB_24dd_367d:
//     pbVar1 = pbVar5;
//     pbVar5 = pbVar5 + 1;
//     if (*pbVar1 == 0) break;
//     pbVar2 = pbVar7;
//     pbVar7 = pbVar7 + 1;
//     *pbVar2 = *pbVar1;
//   }
//   *pbVar7 = 0;
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_3639;
begin
  { TODO: translate from asm/FUN_24dd_3639.s — UNMATCHED until an oracle passes }
end;

