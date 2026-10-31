{ stickman::FUN_1000_1c3e — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_1c3e.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_1c3e.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_1000_1c3e(void)
// 
// {
//   undefined2 uVar1;
//   char cVar2;
//   undefined1 uVar3;
//   int iVar4;
//   int iVar5;
//   undefined2 unaff_DS;
//   bool bVar6;
//   
//   FUN_42b5_04df();
//   if (*(int *)0x3b0 < 2) {
//     return;
//   }
//   cVar2 = FUN_1000_1b9e(*(undefined2 *)0x3b0,*(int *)0x3ae + -1);
//   if (cVar2 != '\0') {
//     return;
//   }
//   cVar2 = FUN_1000_1b9e(*(int *)0x3b0 + -1,*(undefined2 *)0x3ae);
//   if (cVar2 != '\0') {
//     return;
//   }
//   cVar2 = FUN_1000_1b9e(*(int *)0x3b0 + -1,*(int *)0x3ae + 1);
//   if (cVar2 != '\0') {
//     return;
//   }
//   uVar1 = *(undefined2 *)0x3ae;
//   if (*(char *)0x3a6 == '\0') {
//     cVar2 = *(char *)((*(int *)0x3b0 + -1) * 0x50 + *(int *)0x3ae + 0x1f6f);
//     if (cVar2 == '\a') {
//       *(int *)0x3ae = *(int *)0x3ae + 1;
//     }
//     else if (cVar2 != '\b') {
//       if (cVar2 != '\t') {
//         return;
//       }
//       *(int *)0x3ae = *(int *)0x3ae + -1;
//     }
//   }
//   FUN_3de3_0b67(*(int *)0x3b0 + 1,uVar1);
//   FUN_3de3_002d(0x1be5,0x3de3);
//   if (*(char *)0x3a6 != '\0') {
//     FUN_1000_0614();
//   }
//   *(int *)0x3b0 = *(int *)0x3b0 + -1;
//   iVar5 = (*(int *)0x3b0 + 2) * 0x50;
//   iVar4 = iVar5 + *(int *)0x3ae;
//   bVar6 = iVar4 == 0;
//   FUN_42b5_0e79(0x1bf4,0x3de3,CONCAT11((char)((uint)iVar5 >> 8),*(undefined1 *)(iVar4 + 0x1f6f)));
//   if (bVar6) {
//     iVar5 = (*(int *)0x3b0 + 1) * 0x50;
//     iVar4 = iVar5 + *(int *)0x3ae;
//     bVar6 = iVar4 == 0;
//     FUN_42b5_0e79(0x1bf4,0x42b5,CONCAT11((char)((uint)iVar5 >> 8),*(undefined1 *)(iVar4 + 0x1f6f)));
//     if (bVar6) {
//       iVar5 = *(int *)0x3b0 * 0x50 + *(int *)0x3ae;
//       bVar6 = iVar5 == 0;
//       FUN_42b5_0e79(0x1bf4,0x42b5,
//                     CONCAT11((char)((uint)(*(int *)0x3b0 * 0x50) >> 8),
//                              *(undefined1 *)(iVar5 + 0x1f6f)));
//       if (bVar6) {
//         uVar3 = 0;
//         goto LAB_1000_1d5c;
//       }
//     }
//   }
//   uVar3 = 1;
// LAB_1000_1d5c:
//   *(undefined1 *)0x3a6 = uVar3;
//   if (*(char *)0x3a6 == '\0') {
//     FUN_3de3_0bea(0x1c2f,0x42b5,*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
//   }
//   else {
//     if (*(char *)0x2 == '\0') {
//       FUN_3de3_0bea(0x1c21,0x42b5,*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
//     }
//     else {
//       FUN_3de3_0bea(0x1c14,0x42b5,*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
//     }
//     *(bool *)2 = *(char *)0x2 == '\0';
//   }
//   FUN_1000_1619(10);
//   return;
// }
// 
// --- end reference ---
procedure FUN_1000_1c3e;
begin
  { TODO: translate from asm/FUN_1000_1c3e.s — UNMATCHED until an oracle passes }
end;

