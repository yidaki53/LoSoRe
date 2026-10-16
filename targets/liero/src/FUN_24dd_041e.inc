{ liero::FUN_24dd_041e — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_041e.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_041e.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_24dd_041e(void)
// 
// {
//   undefined4 *puVar1;
//   int in_AX;
//   undefined4 *in_CX;
//   uint in_BX;
//   undefined4 *puVar2;
//   undefined4 *puVar3;
//   uint uVar4;
//   uint unaff_DS;
//   undefined4 uVar5;
//   
//   if ((((in_AX != 0) && (((uint)in_CX & 0xfff7) == 0)) &&
//       ((*(uint *)0x63ec < in_BX ||
//        ((*(uint *)0x63ec <= in_BX && ((undefined4 *)*(uint *)0x63ea <= in_CX)))))) &&
//      ((in_BX < *(uint *)0x63f0 ||
//       ((in_BX <= *(uint *)0x63f0 && (in_CX < (undefined4 *)*(uint *)0x63ee)))))) {
//     uVar5 = FUN_24dd_04dc();
//     *(int *)(in_CX + 1) = (int)uVar5;
//     *(undefined2 *)((int)in_CX + 6) = (int)((ulong)uVar5 >> 0x10);
//     puVar3 = (undefined4 *)0x63f6;
//     do {
//       do {
//         uVar4 = unaff_DS;
//         puVar2 = puVar3;
//         puVar1 = (undefined4 *)*puVar2;
//         unaff_DS = (uint)((ulong)puVar1 >> 0x10);
//         puVar3 = (undefined4 *)puVar1;
//       } while (unaff_DS < in_BX);
//       if (in_BX < unaff_DS) goto LAB_24dd_046f;
//     } while (puVar3 < in_CX);
//     if (in_CX != puVar3) {
// LAB_24dd_046f:
//       FUN_24dd_047d(puVar2,uVar4);
//       FUN_24dd_047d();
//       return;
//     }
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_041e;
begin
  { TODO: translate from asm/FUN_24dd_041e.s — UNMATCHED until an oracle passes }
end;

