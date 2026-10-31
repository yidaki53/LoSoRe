{ stickman::FUN_42b5_00e2 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_42b5_00e2.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_42b5_00e2.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// /* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
// /* WARNING: Restarted to delay deadcode elimination for space: ram */
// 
// void __cdecl16far FUN_42b5_00e2(void)
// 
// {
//   code *pcVar1;
//   undefined2 in_AX;
//   int iVar2;
//   int iVar3;
//   char *pcVar4;
//   int in_stack_00000000;
//   int in_stack_00000002;
//   
//   DAT_4473_0392 = in_AX;
//   iVar2 = DAT_4473_0370;
//   if (in_stack_00000000 != 0 || in_stack_00000002 != 0) {
//     for (; (iVar3 = in_stack_00000002, iVar2 != 0 &&
//            (iVar3 = iVar2, in_stack_00000002 != *(int *)0x10)); iVar2 = *(int *)0x14) {
//     }
//     in_stack_00000002 = (iVar3 - DAT_4473_0398) + -0x10;
//   }
//   DAT_4473_0394 = in_stack_00000000;
//   DAT_4473_0396 = in_stack_00000002;
//   pcVar4 = (char *)_DAT_4473_038e;
//   if ((int)((ulong)_DAT_4473_038e >> 0x10) == 0 && pcVar4 == (char *)0x0) {
//     FUN_42b5_05bf();
//     FUN_42b5_05bf();
//     iVar2 = 0x13;
//     do {
//       pcVar1 = (code *)swi(0x21);
//       (*pcVar1)();
//       iVar2 = iVar2 + -1;
//     } while (iVar2 != 0);
//     if (DAT_4473_0394 != 0 || DAT_4473_0396 != 0) {
//       FUN_42b5_01a5();
//       FUN_42b5_01b3();
//       FUN_42b5_01a5();
//       FUN_42b5_01cd();
//       FUN_42b5_01e7();
//       FUN_42b5_01cd();
//       pcVar4 = (char *)0x215;
//       FUN_42b5_01a5();
//     }
//     pcVar1 = (code *)swi(0x21);
//     (*pcVar1)();
//     for (; *pcVar4 != '\0'; pcVar4 = pcVar4 + 1) {
//       FUN_42b5_01e7();
//     }
//     return;
//   }
//   _DAT_4473_038e = (char *)0x0;
//   DAT_4473_039c = 0;
//   return;
// }
// 
// --- end reference ---
procedure FUN_42b5_00e2;
begin
  { TODO: translate from asm/FUN_42b5_00e2.s — UNMATCHED until an oracle passes }
end;

