{ liero::FUN_24dd_3b22 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_3b22.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_3b22.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_24dd_3b22(byte *param_1,undefined2 *param_2)
// 
// {
//   byte *pbVar1;
//   byte *pbVar2;
//   int iVar3;
//   uint uVar4;
//   byte *pbVar5;
//   byte *pbVar6;
//   undefined2 uVar7;
//   
//   uVar7 = (undefined2)((ulong)param_2 >> 0x10);
//   pbVar6 = (byte *)((undefined2 *)param_2 + 1);
//   *param_2 = 0;
//   pbVar6[0] = 0xb0;
//   pbVar6[1] = 0xd7;
//   for (iVar3 = 0x16; pbVar6 = pbVar6 + 2, iVar3 != 0; iVar3 = iVar3 + -1) {
//     pbVar6[0] = 0;
//     pbVar6[1] = 0;
//   }
//   uVar4 = 0x4f;
//   pbVar5 = (byte *)param_1 + 1;
//   if (0x4e < *param_1) goto LAB_24dd_3b4e;
//   for (uVar4 = (uint)*param_1; uVar4 != 0; uVar4 = uVar4 - 1) {
// LAB_24dd_3b4e:
//     pbVar1 = pbVar5;
//     pbVar5 = pbVar5 + 1;
//     if (*pbVar1 == 0) break;
//     pbVar2 = pbVar6;
//     pbVar6 = pbVar6 + 1;
//     *pbVar2 = *pbVar1;
//   }
//   *pbVar6 = 0;
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_3b22;
begin
  { TODO: translate from asm/FUN_24dd_3b22.s — UNMATCHED until an oracle passes }
end;

