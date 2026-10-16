{ liero::FUN_24dd_3054 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_3054.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_3054.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// /* WARNING: Control flow encountered bad instruction data */
// /* WARNING: Instruction at (ram,0x00027e7f) overlaps instruction at (ram,0x00027e7e)
//     */
// /* WARNING: Heritage AFTER dead removal. Example location: r0x0002fb18 : 0x00024f87 */
// /* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
// /* WARNING: Restarted to delay deadcode elimination for space: ram */
// 
// uint __cdecl16far FUN_24dd_3054(void)
// 
// {
//   char *pcVar1;
//   uint *puVar2;
//   code *pcVar3;
//   undefined2 uVar4;
//   uint uVar5;
//   uint uVar6;
//   int iVar7;
//   int iVar8;
//   uint uVar9;
//   char *pcVar10;
//   int in_BX;
//   int unaff_BP;
//   int unaff_SI;
//   int unaff_DI;
//   undefined2 unaff_SS;
//   bool bVar11;
//   undefined2 in_FPUControlWord;
//   uint in_FPUStatusWord;
//   byte bVar12;
//   uint in_FPUTagWord;
//   undefined2 in_FPULastInstructionOpcode;
//   undefined4 in_FPUDataPointer;
//   undefined4 in_FPUInstructionPointer;
//   undefined4 uVar13;
//   undefined2 in_stack_0000000a;
//   uint uStack_4;
//   
//   uStack_4 = 0x24dd;
//   do {
//     iVar7 = 10;
//     do {
//       pcVar3 = (code *)swi(0x21);
//       (*pcVar3)();
//       iVar7 = iVar7 + -1;
//       iVar8 = 0;
//     } while (iVar7 != 0);
//     while( true ) {
//       pcVar3 = (code *)swi(0x21);
//       (*pcVar3)();
//       pcVar3 = (code *)swi(0x21);
//       (*pcVar3)();
//       pcVar3 = (code *)swi(0x21);
//       (*pcVar3)();
//       uRam000230c2 = *(undefined2 *)0x7af4;
//       uRam000230c4 = *(undefined2 *)0x7af6;
//       pcVar3 = (code *)swi(0x37);
//       uVar5 = (*pcVar3)();
//       if (iVar8 == 0) break;
//       uVar5 = uVar5 ^ 0x3e2e;
//       if ((POPCOUNT(uVar5 & 0xff) & 1U) == 0) {
//         out(0xf0,0);
//         out(0xa0,0x20);
//         out(0x20,0x20);
//         goto LAB_24dd_309c;
//       }
//       pcVar1 = (char *)(unaff_BP + unaff_DI + -0x322a);
//       *pcVar1 = *pcVar1 + (char)iVar8;
//       puVar2 = (uint *)(in_BX + unaff_SI + -0x1e);
//       *puVar2 = *puVar2 & uVar5 & 0xab9;
//     }
//   } while( true );
//   while( true ) {
//     pcVar3 = (code *)swi(0x37);
//     uVar6 = (*pcVar3)();
//     bVar11 = iVar8 != 0;
//     iVar8 = 0;
//     if (bVar11) break;
// LAB_24dd_309c:
//     if (DAT_2971_6421 == '\0') {
//       pcVar3 = (code *)swi(0x35);
//       uVar13 = (*pcVar3)();
//       uRam0003124e = (int)((ulong)uVar13 >> 0x10);
//       return (int)uVar13 + 0x36d9;
//     }
//     DAT_2971_7b58 = in_FPUDataPointer;
//     DAT_2971_7b56 = in_FPULastInstructionOpcode;
//     DAT_2971_7b50 = in_FPUInstructionPointer;
//     DAT_2971_7b4c = in_FPUTagWord;
//     DAT_2971_7b48 = in_FPUStatusWord;
//     DAT_2971_7b44 = in_FPUControlWord;
//     uVar4 = DAT_2971_7b44;
//     DAT_2971_7b44._0_1_ = (byte)in_FPUControlWord;
//     if (-1 < (char)(~(byte)DAT_2971_7b44 & DAT_2971_7b46)) {
//       DAT_2971_7b44 = uVar4;
//                     /* WARNING: Bad instruction - Truncating control flow here */
//       halt_baddata();
//     }
//     if ((~(byte)DAT_2971_7b44 & DAT_2971_7b46 & 0x3d) == 0) {
//       bVar11 = ((byte)in_FPUTagWord & 0xc0) == 0xc0;
//       goto LAB_24dd_312d;
//     }
//   }
//   in_FPUTagWord = uVar6 ^ 0x3e2e;
//   bVar11 = in_FPUTagWord == 0;
//   if ((POPCOUNT(in_FPUTagWord & 0xff) & 1U) == 0) {
//     if (DAT_2971_6421 != '\0') {
//       uStack_4 = (DAT_2971_7b4c & 0xf000) + (DAT_2971_7b4a >> 4);
//       uVar5 = DAT_2971_7b4a & 0xf;
//     }
//     if (((in_FPUTagWord & 1) != 0) ||
//        (((DAT_2971_6406 = 200, (in_FPUTagWord & 4) == 0 &&
//          (DAT_2971_6406 = 0xcd, (in_FPUTagWord & 8) == 0)) &&
//         (DAT_2971_6406 = 0xce, (in_FPUTagWord & 0x10) == 0)))) {
//       DAT_2971_6406 = 0xcf;
//     }
//     uVar6 = DAT_2971_63e4;
//     DAT_2971_6408 = uVar5;
//     if (uVar5 != 0 || uStack_4 != 0) {
//       for (; (DAT_2971_6408 = uVar5, uVar9 = uStack_4, uVar6 != 0 &&
//              (((uVar9 = *(uint *)0x10, uVar9 == 0 ||
//                (iVar7 = uVar9 - uStack_4, uStack_4 <= uVar9 && iVar7 != 0)) ||
//               ((0xfff < (uint)-iVar7 ||
//                ((DAT_2971_6408 = iVar7 * -0x10 + uVar5, CARRY2(iVar7 * -0x10,uVar5) ||
//                 (uVar9 = uVar6, *(uint *)0x8 <= DAT_2971_6408)))))))); uVar6 = *(uint *)0x14) {
//       }
//       uStack_4 = (uVar9 - DAT_2971_640c) - 0x10;
//     }
//     DAT_2971_640a = uStack_4;
//     pcVar10 = (char *)_DAT_2971_6402;
//     if ((int)((ulong)_DAT_2971_6402 >> 0x10) == 0 && pcVar10 == (char *)0x0) {
//       FUN_24dd_3711();
//       FUN_24dd_3711();
//       iVar7 = 0x13;
//       do {
//         pcVar3 = (code *)swi(0x21);
//         (*pcVar3)();
//         iVar7 = iVar7 + -1;
//       } while (iVar7 != 0);
//       if (DAT_2971_6408 != 0 || DAT_2971_640a != 0) {
//         FUN_24dd_01f0();
//         FUN_24dd_01fe();
//         FUN_24dd_01f0();
//         FUN_24dd_0218();
//         FUN_24dd_0232();
//         FUN_24dd_0218();
//         pcVar10 = (char *)0x260;
//         FUN_24dd_01f0();
//       }
//       pcVar3 = (code *)swi(0x21);
//       (*pcVar3)();
//       for (; *pcVar10 != '\0'; pcVar10 = pcVar10 + 1) {
//         FUN_24dd_0232();
//       }
//       return 0;
//     }
//     _DAT_2971_6402 = (char *)0x0;
//     DAT_2971_6410 = 0;
//     return 0x16e;
//   }
// LAB_24dd_312d:
//   bVar12 = (byte)(in_FPUStatusWord >> 8);
//   if (!bVar11) {
//     in_FPUTagWord = in_FPUTagWord & 0xff38 | 7;
//   }
//   uRam0002311d = CONCAT11((char)in_FPUTagWord,(char)(in_FPUTagWord >> 8)) & 0xff07 | 0xd8;
//   if (((uRam0002311d != 0x7d9) && (uRam0002311d != 0x7dd)) && (uRam0002311d != 0x2fdb)) {
//     if (((uRam0002311d == 0x17d8) || (uRam0002311d == 0x17dc)) ||
//        ((uRam0002311d == 0x1fd8 || (uRam0002311d == 0x1fdc)))) goto LAB_24dd_3195;
//     if ((uRam0002311d == 0x37d8) || (uRam0002311d == 0x37dc)) {
//       uRam0002311d = uRam0002311d + 0xd001;
//       FUN_24dd_3117();
//       FUN_24dd_31a6();
//       iVar7 = (bVar12 & 0x7f) << 8;
//     }
//     else {
//       iVar7 = (in_FPUStatusWord >> 8 & 0x7f) << 8;
//       FUN_24dd_3117();
//     }
//     DAT_2971_7b40 = (byte)iVar7;
//     DAT_2971_7b46 = DAT_2971_7b46 | DAT_2971_7b40;
//     _DAT_2971_7b40 = iVar7;
//   }
//   FUN_24dd_31a6();
// LAB_24dd_3195:
//   DAT_2971_7b46 = DAT_2971_7b46 & 0xfd;
//   return uVar5;
// }
// 
// --- end reference ---
procedure FUN_24dd_3054;
begin
  { TODO: translate from asm/FUN_24dd_3054.s — UNMATCHED until an oracle passes }
end;

