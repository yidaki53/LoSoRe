{ liero::FUN_24dd_3eaf — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_3eaf.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_3eaf.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_24dd_3eaf(byte param_1,byte *param_2,byte *param_3)
// 
// {
//   byte bVar1;
//   uint uVar2;
//   byte *pbVar3;
//   byte *pbVar4;
//   
//   pbVar3 = (byte *)param_3;
//   pbVar4 = (byte *)param_2;
//   bVar1 = *param_3;
//   if (param_1 < *param_3) {
//     bVar1 = param_1;
//   }
//   *param_2 = bVar1;
//   uVar2 = (uint)bVar1;
//   while( true ) {
//     pbVar4 = pbVar4 + 1;
//     pbVar3 = pbVar3 + 1;
//     if (uVar2 == 0) break;
//     uVar2 = uVar2 - 1;
//     *pbVar4 = *pbVar3;
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_3eaf;
begin
  { TODO: translate from asm/FUN_24dd_3eaf.s — UNMATCHED until an oracle passes }
end;

