{ stickman::FUN_428f_0156 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_428f_0156.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_428f_0156.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_428f_0156(int *param_1,int *param_2)
// 
// {
//   int iVar1;
//   int iVar2;
//   int iVar3;
//   int *piVar4;
//   undefined2 uVar5;
//   
//   uVar5 = (undefined2)((ulong)param_2 >> 0x10);
//   piVar4 = (int *)param_2;
//   iVar1 = *param_2;
//   iVar2 = piVar4[1];
//   iVar3 = piVar4[2];
//   *param_1 = ((uint)piVar4[5] >> 1) + piVar4[3] * 0x800 + piVar4[4] * 0x20;
//   ((int *)param_1)[1] = (iVar1 + -0x7bc) * 0x200 + iVar2 * 0x20 + iVar3;
//   return;
// }
// 
// --- end reference ---
procedure FUN_428f_0156(param_1, param_2: Pointer);
begin
  { TODO: translate from asm/FUN_428f_0156.s — UNMATCHED until an oracle passes }
end;

