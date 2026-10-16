{ liero::FUN_24dd_36c4 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_36c4.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_36c4.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_24dd_36c4(undefined4 param_1)
// 
// {
//   int iVar1;
//   undefined2 in_DX;
//   int iVar2;
//   undefined2 uVar3;
//   undefined2 unaff_DS;
//   bool bVar4;
//   
//   uVar3 = (undefined2)((ulong)param_1 >> 0x10);
//   iVar2 = (int)param_1;
//   iVar1 = *(int *)(iVar2 + 2);
//   if ((iVar1 == -0x284f) || (iVar1 == -0x284e)) {
//     FUN_24dd_3711(iVar2,uVar3);
//   }
//   else if (iVar1 != -0x2850) {
//     *(undefined2 *)0x6410 = 0x66;
//     return;
//   }
//   bVar4 = true;
//   *(undefined2 *)(iVar2 + 2) = in_DX;
//   *(undefined2 *)(iVar2 + 8) = 0;
//   *(undefined2 *)(iVar2 + 10) = 0;
//   FUN_24dd_374d();
//   if (!bVar4) {
//     *(undefined2 *)(iVar2 + 2) = 0xd7b0;
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_36c4;
begin
  { TODO: translate from asm/FUN_24dd_36c4.s — UNMATCHED until an oracle passes }
end;

