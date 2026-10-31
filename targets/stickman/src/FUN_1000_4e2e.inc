{ stickman::FUN_1000_4e2e — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_4e2e.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_4e2e.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_1000_4e2e(void)
// 
// {
//   char cVar1;
//   undefined2 unaff_DS;
//   undefined2 uVar2;
//   int iVar3;
//   
//   uVar2 = 0x1000;
//   FUN_42b5_04df();
//   FUN_3de3_0c99(0x4e26,0x42b5);
//   *(undefined1 *)0x136 = 1;
//   FUN_1000_2d1f(uVar2);
//   iVar3 = 1;
//   *(undefined1 *)0x3a4 = 0;
//   while (*(char *)0x3a4 == '\0') {
//     FUN_1000_2d1f();
//     FUN_3de3_0b67(iVar3 + 9,0x18);
//     FUN_3de3_0d8a();
//     uVar2 = FUN_3de3_0339();
//     cVar1 = FUN_42b5_1bc4(uVar2);
//     if (cVar1 == '\0') {
//       FUN_3de3_0339();
//     }
//     else if (cVar1 == '2') {
//       if (iVar3 < 6) {
//         iVar3 = iVar3 + 1;
//       }
//     }
//     else if (cVar1 == '8') {
//       if (1 < iVar3) {
//         iVar3 = iVar3 + -1;
//       }
//     }
//     else if (cVar1 == '\r') {
//       if (iVar3 == 1) {
//         FUN_1000_328e(*(undefined2 *)0x4fd);
//       }
//       else if (iVar3 == 2) {
//         FUN_1000_35bb();
//       }
//       else if (iVar3 == 3) {
//         FUN_1000_4905();
//       }
//       else if (iVar3 == 4) {
//         FUN_1000_3a5e();
//       }
//       else if (iVar3 == 5) {
//         FUN_1000_4d03();
//       }
//       else if (iVar3 == 6) {
//         *(undefined1 *)0x3a4 = 1;
//       }
//     }
//     else if (cVar1 == 'P') {
//       FUN_1000_328e(*(undefined2 *)0x4fd);
//     }
//     else if (cVar1 == 'I') {
//       FUN_1000_35bb();
//     }
//     else if (cVar1 == 'C') {
//       FUN_1000_4905();
//     }
//     else if (cVar1 == 'H') {
//       FUN_1000_3a5e();
//     }
//     else if (cVar1 == 'O') {
//       FUN_1000_4d03();
//     }
//     else if (cVar1 == 'Q') {
//       *(undefined1 *)0x3a4 = 1;
//     }
//   }
//   FUN_1000_01cf();
//   *(undefined1 *)0x136 = 0;
//   return;
// }
// 
// --- end reference ---
procedure FUN_1000_4e2e;
begin
  { TODO: translate from asm/FUN_1000_4e2e.s — UNMATCHED until an oracle passes }
end;

