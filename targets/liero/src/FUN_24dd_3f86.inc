{ liero::FUN_24dd_3f86 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_3f86.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_3f86.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_24dd_3f86(byte *param_1,byte *param_2)
// 
// {
//   byte bVar1;
//   uint uVar2;
//   byte *pbVar3;
//   byte *pbVar4;
//   
//   pbVar3 = (byte *)param_2;
//   pbVar4 = (byte *)param_1;
//   bVar1 = *param_2;
//   if (*param_1 < *param_2) {
//     bVar1 = *param_1;
//   }
//   if (bVar1 != 0) {
//     uVar2 = (uint)bVar1;
//     do {
//       pbVar4 = pbVar4 + 1;
//       pbVar3 = pbVar3 + 1;
//       if (uVar2 == 0) {
//         return;
//       }
//       uVar2 = uVar2 - 1;
//     } while (*pbVar3 == *pbVar4);
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_3f86;
begin
  { TODO: translate from asm/FUN_24dd_3f86.s — UNMATCHED until an oracle passes }
end;

