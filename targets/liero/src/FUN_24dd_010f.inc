{ liero::FUN_24dd_010f — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_010f.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_010f.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// /* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
// /* WARNING: Restarted to delay deadcode elimination for space: ram */
// 
// void __cdecl16far FUN_24dd_010f(void)
// 
// {
//   code *pcVar1;
//   undefined2 in_AX;
//   uint uVar2;
//   int iVar3;
//   uint uVar4;
//   char *pcVar5;
//   uint in_stack_00000000;
//   uint in_stack_00000002;
//   
//   DAT_2971_6406 = in_AX;
//   uVar2 = DAT_2971_63e4;
//   DAT_2971_6408 = in_stack_00000000;
//   if (in_stack_00000000 != 0 || in_stack_00000002 != 0) {
//     for (; (DAT_2971_6408 = in_stack_00000000, uVar4 = in_stack_00000002, uVar2 != 0 &&
//            ((((uVar4 = *(uint *)0x10, uVar4 == 0 ||
//               (iVar3 = uVar4 - in_stack_00000002, in_stack_00000002 <= uVar4 && iVar3 != 0)) ||
//              (0xfff < (uint)-iVar3)) ||
//             ((DAT_2971_6408 = iVar3 * -0x10 + in_stack_00000000,
//              CARRY2(iVar3 * -0x10,in_stack_00000000) ||
//              (uVar4 = uVar2, *(uint *)0x8 <= DAT_2971_6408)))))); uVar2 = *(uint *)0x14) {
//     }
//     in_stack_00000002 = (uVar4 - DAT_2971_640c) - 0x10;
//   }
//   DAT_2971_640a = in_stack_00000002;
//   pcVar5 = (char *)_DAT_2971_6402;
//   if ((int)((ulong)_DAT_2971_6402 >> 0x10) == 0 && pcVar5 == (char *)0x0) {
//     FUN_24dd_3711();
//     FUN_24dd_3711();
//     iVar3 = 0x13;
//     do {
//       pcVar1 = (code *)swi(0x21);
//       (*pcVar1)();
//       iVar3 = iVar3 + -1;
//     } while (iVar3 != 0);
//     if (DAT_2971_6408 != 0 || DAT_2971_640a != 0) {
//       FUN_24dd_01f0();
//       FUN_24dd_01fe();
//       FUN_24dd_01f0();
//       FUN_24dd_0218();
//       FUN_24dd_0232();
//       FUN_24dd_0218();
//       pcVar5 = (char *)0x260;
//       FUN_24dd_01f0();
//     }
//     pcVar1 = (code *)swi(0x21);
//     (*pcVar1)();
//     for (; *pcVar5 != '\0'; pcVar5 = pcVar5 + 1) {
//       FUN_24dd_0232();
//     }
//     return;
//   }
//   _DAT_2971_6402 = (char *)0x0;
//   DAT_2971_6410 = 0;
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_010f;
begin
  { TODO: translate from asm/FUN_24dd_010f.s — UNMATCHED until an oracle passes }
end;

