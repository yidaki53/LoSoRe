{ stickman::FUN_42b5_03d3 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_42b5_03d3.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_42b5_03d3.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_42b5_03d3(void)
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
//       ((*(uint *)0x378 < in_BX ||
//        ((*(uint *)0x378 <= in_BX && ((undefined4 *)*(uint *)0x376 <= in_CX)))))) &&
//      ((in_BX < *(uint *)0x37c ||
//       ((in_BX <= *(uint *)0x37c && (in_CX < (undefined4 *)*(uint *)0x37a)))))) {
//     uVar5 = FUN_42b5_0491();
//     *(int *)(in_CX + 1) = (int)uVar5;
//     *(undefined2 *)((int)in_CX + 6) = (int)((ulong)uVar5 >> 0x10);
//     puVar3 = (undefined4 *)0x382;
//     do {
//       do {
//         uVar4 = unaff_DS;
//         puVar2 = puVar3;
//         puVar1 = (undefined4 *)*puVar2;
//         unaff_DS = (uint)((ulong)puVar1 >> 0x10);
//         puVar3 = (undefined4 *)puVar1;
//       } while (unaff_DS < in_BX);
//       if (in_BX < unaff_DS) goto LAB_42b5_0424;
//     } while (puVar3 < in_CX);
//     if (in_CX != puVar3) {
// LAB_42b5_0424:
//       FUN_42b5_0432(puVar2,uVar4);
//       FUN_42b5_0432();
//       return;
//     }
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_42b5_03d3;
begin
  { TODO: translate from asm/FUN_42b5_03d3.s — UNMATCHED until an oracle passes }
end;

