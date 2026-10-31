{ stickman::FUN_42b5_05bf — game Pascal draft (oracle: none).
  Drafted from asm/FUN_42b5_05bf.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_42b5_05bf.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_42b5_05bf(undefined4 param_1)
// 
// {
//   int iVar1;
//   undefined2 uVar2;
//   undefined2 unaff_DS;
//   
//   uVar2 = (undefined2)((ulong)param_1 >> 0x10);
//   iVar1 = (int)param_1;
//   if (*(int *)(iVar1 + 2) != -0x284f) {
//     if (*(int *)(iVar1 + 2) != -0x284e) {
//       *(undefined2 *)0x39c = 0x67;
//       return;
//     }
//     FUN_42b5_05fb();
//   }
//   FUN_42b5_05fb();
//   *(undefined2 *)(iVar1 + 2) = 0xd7b0;
//   return;
// }
// 
// --- end reference ---
procedure FUN_42b5_05bf(param_1: Longint);
begin
  { TODO: translate from asm/FUN_42b5_05bf.s — UNMATCHED until an oracle passes }
end;

