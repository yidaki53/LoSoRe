{ stickman::FUN_1000_0850 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_0850.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_0850.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_1000_0850(void)
// 
// {
//   int iVar1;
//   undefined2 uVar2;
//   undefined2 unaff_DS;
//   undefined2 local_8;
//   undefined2 local_4;
//   
//   uVar2 = 0x42b5;
//   FUN_42b5_04df();
//   local_4 = 1;
//   while( true ) {
//     if (*(int *)(local_4 * 0x275 + 0x459) != 0) {
//       iVar1 = local_4 * 0x275;
//       _local_8 = (undefined2 *)CONCAT22(unaff_DS,(undefined2 *)(iVar1 + 0x459));
//       FUN_3de3_0b67(*(int *)(iVar1 + 0x45b) + 1,*_local_8);
//       uVar2 = 0x3de3;
//       FUN_3de3_002d(iVar1 + 0x48e,unaff_DS);
//     }
//     if (local_4 == 10) break;
//     local_4 = local_4 + 1;
//   }
//   FUN_3de3_002d(0x84b,uVar2);
//   return;
// }
// 
// --- end reference ---
procedure FUN_1000_0850;
begin
  { TODO: translate from asm/FUN_1000_0850.s — UNMATCHED until an oracle passes }
end;

