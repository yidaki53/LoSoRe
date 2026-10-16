{ liero::FUN_24dd_35d4 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_35d4.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_35d4.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_24dd_35d4(void)
// 
// {
//   code *pcVar1;
//   uint uVar2;
//   int in_AX;
//   int iVar3;
//   uint uVar4;
//   undefined2 uVar5;
//   
//   if (0x1000 < in_AX) {
//     pcVar1 = (code *)swi(0x3c);
//     iVar3 = (*pcVar1)();
//     in_AX = iVar3 + -0xfff;
//   }
//   if (in_AX < -0x1000) {
//     pcVar1 = (code *)swi(0x3c);
//     iVar3 = (*pcVar1)();
//     in_AX = iVar3 + 0x1001;
//   }
//   if (in_AX != 0) {
//     pcVar1 = (code *)swi(0x3c);
//     (*pcVar1)();
//     uVar4 = FUN_24dd_1ee4();
//     uVar4 = uVar4 >> 1;
//     while (uVar4 != 0) {
//       uVar2 = uVar4 & 1;
//       uVar4 = uVar4 >> 1;
//       if (uVar2 != 0) {
//         pcVar1 = (code *)swi(0x3c);
//         uVar5 = (*pcVar1)();
//         uVar4 = CONCAT11((char)((uint)uVar5 >> 8),(char)uVar5 + '3');
//       }
//     }
//     if (-1 < in_AX) {
//       pcVar1 = (code *)swi(0x3a);
//       (*pcVar1)();
//       return;
//     }
//     pcVar1 = (code *)swi(0x3a);
//     (*pcVar1)();
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_35d4;
begin
  { TODO: translate from asm/FUN_24dd_35d4.s — UNMATCHED until an oracle passes }
end;

