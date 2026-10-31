{ stickman::FUN_42b5_1aac — game Pascal draft (oracle: none).
  Drafted from asm/FUN_42b5_1aac.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_42b5_1aac.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_42b5_1aac(void)
// 
// {
//   undefined2 uVar1;
//   byte *pbVar2;
//   byte *pbVar3;
//   uint uVar4;
//   int in_DX;
//   undefined2 unaff_DS;
//   
//   uVar1 = *(undefined2 *)0x398;
//   uVar4 = (uint)*(byte *)0x80;
//   pbVar2 = (byte *)0x81;
//   do {
//     for (; (pbVar3 = pbVar2, uVar4 != 0 && (*pbVar2 < 0x21)); pbVar2 = pbVar2 + 1) {
//       uVar4 = uVar4 - 1;
//     }
//     for (; (uVar4 != 0 && (0x20 < *pbVar3)); pbVar3 = pbVar3 + 1) {
//       uVar4 = uVar4 - 1;
//     }
//   } while ((pbVar3 != pbVar2) && (in_DX = in_DX + -1, pbVar2 = pbVar3, in_DX != 0));
//   return;
// }
// 
// --- end reference ---
procedure FUN_42b5_1aac;
begin
  { TODO: translate from asm/FUN_42b5_1aac.s — UNMATCHED until an oracle passes }
end;

