{ stickman::FUN_405f_00ad — game Pascal draft (oracle: none).
  Drafted from asm/FUN_405f_00ad.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_405f_00ad.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void FUN_405f_00ad(int param_1)
// 
// {
//   undefined2 unaff_SS;
//   undefined2 unaff_DS;
//   undefined2 local_4;
//   
//   FUN_42b5_04df();
//   local_4 = *(int *)0x156 + 1;
//   if (0x3fff < local_4) {
//     local_4 = *(int *)0x156 + -0x3fff;
//   }
//   if (local_4 == *(int *)0x158) {
//     FUN_410e_02c7(5000);
//     FUN_410e_029c(1000);
//     FUN_410e_02c7(500);
//     FUN_410e_029c(100);
//     FUN_410e_02f4();
//   }
//   else {
//     *(undefined1 *)(*(int *)0x156 + -0x54fe) = *(undefined1 *)(param_1 + 6);
//     *(int *)0x156 = local_4;
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_405f_00ad(param_1: Integer);
begin
  { TODO: translate from asm/FUN_405f_00ad.s — UNMATCHED until an oracle passes }
end;

