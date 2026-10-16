{ liero::FUN_24dd_0e57 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_0e57.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_0e57.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_24dd_0e57(void)
// 
// {
//   uint *puVar1;
//   uint *puVar2;
//   int iVar3;
//   uint *in_BX;
//   uint *unaff_SI;
//   uint *unaff_DI;
//   undefined2 unaff_ES;
//   undefined2 unaff_DS;
//   
//   if ((((unaff_SI[3] & 0x7fff) == 0 && *unaff_SI == 0) && unaff_SI[1] == 0) && unaff_SI[2] == 0) {
//     if (in_BX == (uint *)0xffff) {
//       return;
//     }
//     if ((int)in_BX[4] < 0x4001) {
//       return;
//     }
//     if ((((in_BX[3] & 0x7fff) == 0 && *in_BX == 0) && in_BX[1] == 0) && in_BX[2] == 0) {
//       return;
//     }
//   }
//   else if (((((in_BX == (uint *)0xffff) || ((int)in_BX[4] < 0x4001)) ||
//             ((((in_BX[3] & 0x7fff) == 0 && *in_BX == 0) && in_BX[1] == 0) && in_BX[2] == 0)) ||
//            (in_BX[3] < unaff_SI[3])) ||
//           ((in_BX[3] <= unaff_SI[3] &&
//            ((in_BX[2] < unaff_SI[2] ||
//             ((in_BX[2] <= unaff_SI[2] &&
//              ((in_BX[1] < unaff_SI[1] || ((in_BX[1] <= unaff_SI[1] && (*in_BX < *unaff_SI)))))))))))
//           ) goto LAB_24dd_0ece;
//   unaff_SI = in_BX;
// LAB_24dd_0ece:
//   FUN_24dd_2361();
//   for (iVar3 = 6; iVar3 != 0; iVar3 = iVar3 + -1) {
//     puVar2 = unaff_DI;
//     unaff_DI = unaff_DI + 1;
//     puVar1 = unaff_SI;
//     unaff_SI = unaff_SI + 1;
//     *puVar2 = *puVar1;
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_0e57;
begin
  { TODO: translate from asm/FUN_24dd_0e57.s — UNMATCHED until an oracle passes }
end;

