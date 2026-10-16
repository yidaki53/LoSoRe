{ liero::FUN_24dd_351a — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_351a.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_351a.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// /* WARNING: Instruction at (ram,0x00028368) overlaps instruction at (ram,0x00028367)
//     */
// /* WARNING: Removing unreachable block (ram,0x00028303) */
// /* WARNING: Removing unreachable block (ram,0x0002830c) */
// /* WARNING: Removing unreachable block (ram,0x00028310) */
// /* WARNING: Removing unreachable block (ram,0x00028314) */
// /* WARNING: Removing unreachable block (ram,0x00028316) */
// /* WARNING: Removing unreachable block (ram,0x0002831e) */
// /* WARNING: Removing unreachable block (ram,0x00028325) */
// /* WARNING: Removing unreachable block (ram,0x0002832c) */
// /* WARNING: Removing unreachable block (ram,0x00028331) */
// 
// void __cdecl16near FUN_24dd_351a(void)
// 
// {
//   code *pcVar1;
//   undefined1 uVar2;
//   byte bVar3;
//   int iVar4;
//   byte *pbVar5;
//   int in_CX;
//   undefined1 *puVar6;
//   uint uVar7;
//   undefined2 in_BX;
//   byte *unaff_DI;
//   undefined2 unaff_ES;
//   undefined2 unaff_DS;
//   bool bVar8;
//   char cVar9;
//   char cVar10;
//   char cVar11;
//   longdouble in_ST0;
//   undefined4 uVar12;
//   undefined1 *in_stack_00000000;
//   uint uStack_a;
//   undefined1 uStack_8;
//   char local_7;
//   
//   puVar6 = &stack0xfffe;
//   cVar10 = SBORROW2((int)&stack0xfffe,6);
//   cVar9 = (int)&uStack_8 < 0;
//   bVar8 = &stack0x0000 == (undefined1 *)0x8;
//   pcVar1 = (code *)swi(0x35);
//   (*pcVar1)();
//   do {
//   } while (bVar8 || cVar10 != cVar9);
//   pcVar1 = (code *)swi(0x37);
//   uVar12 = (*pcVar1)();
//   if (in_CX != 1) {
//     while( true ) {
//       uVar7 = (uint)((ulong)uVar12 >> 0x10) & 0xff;
//       *(int *)unaff_DI =
//            CONCAT11((char)((uint)(int)(char)uVar12 % uVar7),(char)((uint)(int)(char)uVar12 / uVar7))
//            + 0x3030;
//       pbVar5 = unaff_DI + (2 - (int)in_stack_00000000);
//       pcVar1 = (code *)swi(0x37);
//       (*pcVar1)();
//       if (pbVar5 == (byte *)0x1) break;
//       *in_stack_00000000 = 0x45;
//       uVar2 = 0x2b;
//       uVar7 = uStack_a;
//       if ((int)uStack_a < 0) {
//         uVar2 = 0x2d;
//         uVar7 = -uStack_a;
//       }
//       in_stack_00000000[1] = uVar2;
//       uVar12 = CONCAT22(10,uVar7 % 100);
//       uVar7 = (uint)(char)(uVar7 / 100);
//       unaff_DI = in_stack_00000000 + 4;
//       *(int *)(in_stack_00000000 + 2) = CONCAT11((char)(uVar7 % 10),(char)(uVar7 / 10)) + 0x3030;
//     }
//     pcVar1 = (code *)swi(0x3d);
//     (*pcVar1)();
//     return;
//   }
//   *(long *)(in_stack_00000000 +
//            CONCAT11((char)((uint)in_BX >> 8) + (char)((ulong)uVar12 >> 0x18),(char)in_BX) + 0x3b) =
//        (long)ROUND(in_ST0);
//   *(int *)(in_stack_00000000 + 0x44) = *(int *)(in_stack_00000000 + 0x44) << 3;
//   bVar3 = *unaff_DI;
// code_r0x00028336:
//   bVar8 = bVar3 < 0x45;
//   if ((bVar3 != 0x45) && (bVar8 = bVar3 < 0x65, bVar3 != 0x65)) goto LAB_24dd_358a;
//   puVar6 = puVar6 + -1;
//   uVar12 = FUN_24dd_4732();
//   if (bVar8) goto LAB_24dd_35a6;
//   do {
//     iVar4 = (int)uVar12;
//     if ((((int)((ulong)uVar12 >> 0x10) == iVar4 >> 0xf) && (iVar4 < 4999)) && (-4999 < iVar4)) {
// LAB_24dd_358a:
//       FUN_24dd_35d4();
//       cVar11 = SBORROW1(local_7,'-');
//       cVar10 = (char)(local_7 + -0x2d) < '\0';
//       cVar9 = local_7 == '-';
//       if ((bool)cVar9) {
//         pcVar1 = (code *)swi(0x35);
//         bVar3 = (*pcVar1)();
//         puVar6 = puVar6 + -1;
//         if (puVar6 != (undefined1 *)0x0 && cVar9 == '\0') goto code_r0x00028336;
//       }
//       else {
//         do {
//           pcVar1 = (code *)swi(0x39);
//           (*pcVar1)();
//         } while ((bool)cVar9 || cVar11 != cVar10);
//       }
//       pcVar1 = (code *)swi(0x3d);
//       (*pcVar1)();
//     }
// LAB_24dd_35a6:
//     pcVar1 = (code *)swi(0x37);
//     uVar12 = (*pcVar1)();
//     puVar6 = puVar6 + -1;
//     if (puVar6 == (undefined1 *)0x0) {
//       pcVar1 = (code *)swi(0x3d);
//       (*pcVar1)();
//       return;
//     }
//   } while( true );
// }
// 
// --- end reference ---
procedure FUN_24dd_351a;
begin
  { TODO: translate from asm/FUN_24dd_351a.s — UNMATCHED until an oracle passes }
end;

