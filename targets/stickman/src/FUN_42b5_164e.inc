{ stickman::FUN_42b5_164e — game Pascal draft (oracle: none).
  Drafted from asm/FUN_42b5_164e.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_42b5_164e.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_42b5_164e(void)
// 
// {
//   int in_CX;
//   int iVar1;
//   undefined2 uVar2;
//   int unaff_BP;
//   char *unaff_DI;
//   undefined2 unaff_ES;
//   undefined2 unaff_SS;
//   undefined1 uVar3;
//   undefined4 uVar4;
//   
//   iVar1 = 0;
//   while( true ) {
//     if (in_CX == 0) {
//       return;
//     }
//     uVar3 = 0xf5 < (byte)(*unaff_DI - 0x3aU);
//     if (!(bool)uVar3) break;
//     iVar1 = iVar1 + 1;
//     unaff_DI = unaff_DI + 1;
//     in_CX = in_CX + -1;
//     FUN_42b5_1192(unaff_DI,in_CX,iVar1);
//     uVar2 = *(undefined2 *)(unaff_BP + -6);
//     FUN_42b5_1718();
//     if (!(bool)uVar3) {
//       uVar4 = FUN_42b5_0f29();
//       *(undefined2 *)(unaff_BP + -8) = (int)uVar4;
//       *(undefined2 *)(unaff_BP + -6) = uVar2;
//       *(undefined2 *)(unaff_BP + -4) = (int)((ulong)uVar4 >> 0x10);
//     }
//     if ((bool)uVar3) {
//       return;
//     }
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_42b5_164e;
begin
  { TODO: translate from asm/FUN_42b5_164e.s — UNMATCHED until an oracle passes }
end;

