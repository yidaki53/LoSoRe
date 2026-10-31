{ stickman::FUN_1000_0614 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_0614.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_0614.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_1000_0614(void)
// 
// {
//   int iVar1;
//   undefined2 unaff_DS;
//   undefined2 local_4;
//   
//   FUN_42b5_04df();
//   iVar1 = *(int *)0x3b0;
//   local_4 = *(int *)0x3b0;
//   if (local_4 <= iVar1 + 2) {
//     while( true ) {
//       FUN_1000_04bc(local_4,*(int *)0x3ae + -1);
//       FUN_1000_04bc(local_4,*(undefined2 *)0x3ae);
//       FUN_1000_04bc(local_4,*(int *)0x3ae + 1);
//       if (local_4 == iVar1 + 2) break;
//       local_4 = local_4 + 1;
//     }
//   }
//   FUN_3de3_002d(0x60f,0x42b5);
//   return;
// }
// 
// --- end reference ---
procedure FUN_1000_0614;
begin
  { TODO: translate from asm/FUN_1000_0614.s — UNMATCHED until an oracle passes }
end;

