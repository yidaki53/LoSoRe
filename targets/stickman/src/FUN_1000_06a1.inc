{ stickman::FUN_1000_06a1 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_06a1.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_06a1.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_1000_06a1(void)
// 
// {
//   int iVar1;
//   undefined1 uVar2;
//   undefined2 unaff_DS;
//   undefined2 local_4;
//   
//   FUN_42b5_04df();
//   FUN_3de3_0b67(0x16,10);
//   iVar1 = *(int *)0x3b4;
//   if (iVar1 == 0) {
//     FUN_3de3_002d(0x670,0x3de3);
//   }
//   else if ((iVar1 < 1) || (3 < iVar1)) {
//     if ((iVar1 < 4) || (6 < iVar1)) {
//       FUN_3de3_002d(0x691,0x3de3);
//     }
//     else {
//       FUN_3de3_002d(0x686,0x3de3);
//     }
//   }
//   else {
//     FUN_3de3_002d(0x67b,0x3de3);
//   }
//   local_4 = 1;
//   while( true ) {
//     uVar2 = (undefined1)((uint)local_4 >> 8);
//     if (*(int *)0x3b4 < local_4) {
//       FUN_3de3_0000(CONCAT11(uVar2,0xfa));
//     }
//     else {
//       FUN_3de3_0000(CONCAT11(uVar2,0xfe));
//     }
//     if (local_4 == 10) break;
//     local_4 = local_4 + 1;
//   }
//   FUN_3de3_002d(0x69c,0x3de3);
//   return;
// }
// 
// --- end reference ---
procedure FUN_1000_06a1;
begin
  { TODO: translate from asm/FUN_1000_06a1.s — UNMATCHED until an oracle passes }
end;

