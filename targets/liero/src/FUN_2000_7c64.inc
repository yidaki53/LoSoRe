{ liero::FUN_2000_7c64 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_2000_7c64.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_2000_7c64.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined2 FUN_2000_7c64(void)
// 
// {
//   byte bVar1;
//   undefined2 in_AX;
//   undefined1 uVar3;
//   uint uVar2;
//   int iVar4;
//   undefined2 uVar5;
//   undefined4 in_stack_00000000;
//   
//   uVar5 = (undefined2)((ulong)in_stack_00000000 >> 0x10);
//   iVar4 = (int)in_stack_00000000;
//   uVar2 = *(uint *)(iVar4 + -1);
//   uVar3 = (undefined1)(uVar2 >> 8);
//   bVar1 = (char)uVar2 - 0x34;
//   if (bVar1 < 8) {
//     *(int *)(iVar4 + -2) = *(int *)(iVar4 + -2) + -0x5c32;
//   }
//   else if (bVar1 < 9) {
//     if ((uVar2 & 0x2000) == 0) {
//       *(undefined1 *)(iVar4 + -2) = 0x9b;
//       uVar2 = CONCAT11(uVar3,uVar3) & 0x7c0;
//       *(int *)(iVar4 + -1) = (CONCAT11((char)(uVar2 >> 8),(byte)uVar2 >> 3) ^ 0x18) + 0xd826;
//     }
//   }
//   else if (bVar1 < 10) {
//     *(undefined2 *)(iVar4 + -2) = 0x9b90;
//   }
//   return in_AX;
// }
// 
// --- end reference ---
procedure FUN_2000_7c64;
begin
  { TODO: translate from asm/FUN_2000_7c64.s — UNMATCHED until an oracle passes }
end;

