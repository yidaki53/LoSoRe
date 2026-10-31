{ stickman::FUN_42b5_0bde — game Pascal draft (oracle: none).
  Drafted from asm/FUN_42b5_0bde.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_42b5_0bde.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_42b5_0bde(byte param_1,byte *param_2,byte *param_3)
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
procedure FUN_42b5_0bde(param_1: Byte; param_2, param_3: Pointer);
begin
  { TODO: translate from asm/FUN_42b5_0bde.s — UNMATCHED until an oracle passes }
end;

