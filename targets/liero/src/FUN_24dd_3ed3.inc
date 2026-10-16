{ liero::FUN_24dd_3ed3 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_3ed3.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_3ed3.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_24dd_3ed3(uint param_1,uint param_2,byte *param_3,byte *param_4)
// 
// {
//   byte *pbVar1;
//   uint uVar2;
//   byte *pbVar3;
//   byte *pbVar4;
//   
//   pbVar4 = (byte *)param_4;
//   if ((int)param_2 < 1) {
//     param_2 = 1;
//   }
//   pbVar3 = (byte *)param_3 + param_2;
//   if (*param_3 < param_2) {
//     uVar2 = 0;
//   }
//   else {
//     uVar2 = (*param_3 - param_2) + 1;
//     if ((int)param_1 < 0) {
//       param_1 = 0;
//     }
//     if (param_1 < uVar2) {
//       uVar2 = param_1;
//     }
//   }
//   *param_4 = (byte)uVar2;
//   for (; pbVar4 = pbVar4 + 1, uVar2 != 0; uVar2 = uVar2 - 1) {
//     pbVar1 = pbVar3;
//     pbVar3 = pbVar3 + 1;
//     *pbVar4 = *pbVar1;
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_3ed3;
begin
  { TODO: translate from asm/FUN_24dd_3ed3.s — UNMATCHED until an oracle passes }
end;

