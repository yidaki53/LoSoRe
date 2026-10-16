{ liero::FUN_24dd_3ce0 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_3ce0.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_3ce0.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined2 __stdcall16far FUN_24dd_3ce0(int param_1,char *param_2)
// 
// {
//   char *pcVar1;
//   code *pcVar2;
//   byte bVar3;
//   int iVar4;
//   undefined2 in_CX;
//   char *unaff_SI;
//   char *pcVar5;
//   undefined2 unaff_ES;
//   undefined2 unaff_DS;
//   
//   if (param_1 == 0) {
//     pcVar2 = (code *)swi(0x21);
//     bVar3 = (*pcVar2)();
//     iVar4 = 0;
//     if (2 < bVar3) {
//       unaff_ES = *(undefined2 *)0x2c;
//       pcVar5 = (char *)0x0;
// LAB_24dd_3d06:
//       if (*pcVar5 != '\0') {
//         iVar4 = -1;
//         do {
//           if (iVar4 == 0) break;
//           iVar4 = iVar4 + -1;
//           pcVar1 = pcVar5;
//           pcVar5 = pcVar5 + 1;
//         } while (*pcVar1 != '\0');
//         goto LAB_24dd_3d06;
//       }
//       unaff_SI = pcVar5 + 3;
//       iVar4 = 0x100;
//       pcVar5 = unaff_SI;
//       do {
//         if (iVar4 == 0) break;
//         iVar4 = iVar4 + -1;
//         pcVar1 = pcVar5;
//         pcVar5 = pcVar5 + 1;
//       } while (*pcVar1 != '\0');
//       in_CX = 0;
//       iVar4 = CONCAT11((char)((uint)iVar4 >> 8),~(byte)iVar4);
//     }
//   }
//   else {
//     iVar4 = FUN_24dd_3d36();
//   }
//   pcVar5 = (char *)param_2;
//   *param_2 = (char)iVar4;
//   for (; pcVar5 = pcVar5 + 1, iVar4 != 0; iVar4 = iVar4 + -1) {
//     pcVar1 = unaff_SI;
//     unaff_SI = unaff_SI + 1;
//     *pcVar5 = *pcVar1;
//   }
//   return in_CX;
// }
// 
// --- end reference ---
procedure FUN_24dd_3ce0;
begin
  { TODO: translate from asm/FUN_24dd_3ce0.s — UNMATCHED until an oracle passes }
end;

