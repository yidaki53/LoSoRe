{ stickman::FUN_42b5_130d — game Pascal draft (oracle: none).
  Drafted from asm/FUN_42b5_130d.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_42b5_130d.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_42b5_130d(void)
// 
// {
//   char *pcVar1;
//   uint uVar2;
//   char cVar3;
//   uint in_AX;
//   char cVar4;
//   uint in_DX;
//   uint uVar5;
//   uint *puVar6;
//   char *unaff_DI;
//   undefined2 unaff_ES;
//   bool bVar7;
//   
//   if ((int)in_DX < 0) {
//     uVar5 = ~in_AX;
//     in_AX = uVar5 + 1;
//     in_DX = ~in_DX + (uint)(0xfffe < uVar5);
//     pcVar1 = unaff_DI;
//     unaff_DI = unaff_DI + 1;
//     *pcVar1 = '-';
//   }
//   puVar6 = (uint *)0x135f;
//   cVar4 = '\t';
//   do {
//     if ((puVar6[1] <= in_DX) && ((puVar6[1] < in_DX || (*puVar6 <= in_AX)))) break;
//     puVar6 = puVar6 + 2;
//     cVar4 = cVar4 + -1;
//   } while (cVar4 != '\0');
//   cVar4 = cVar4 + '\x01';
//   do {
//     cVar3 = '/';
//     do {
//       cVar3 = cVar3 + '\x01';
//       bVar7 = in_AX < *puVar6;
//       in_AX = in_AX - *puVar6;
//       uVar5 = (uint)bVar7;
//       bVar7 = puVar6[1] <= in_DX;
//       uVar2 = in_DX - puVar6[1];
//       in_DX = uVar2 - uVar5;
//     } while (bVar7 && uVar5 <= uVar2);
//     bVar7 = CARRY2(in_AX,*puVar6);
//     in_AX = in_AX + *puVar6;
//     in_DX = in_DX + puVar6[1] + (uint)bVar7;
//     puVar6 = puVar6 + 2;
//     pcVar1 = unaff_DI;
//     unaff_DI = unaff_DI + 1;
//     *pcVar1 = cVar3;
//     cVar4 = cVar4 + -1;
//   } while (cVar4 != '\0');
//   return;
// }
// 
// --- end reference ---
procedure FUN_42b5_130d;
begin
  { TODO: translate from asm/FUN_42b5_130d.s — UNMATCHED until an oracle passes }
end;

