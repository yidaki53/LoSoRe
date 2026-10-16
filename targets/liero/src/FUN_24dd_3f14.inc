{ liero::FUN_24dd_3f14 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_3f14.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_3f14.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_24dd_3f14(byte *param_1,byte *param_2)
// 
// {
//   byte bVar1;
//   byte bVar2;
//   byte bVar3;
//   uint uVar4;
//   byte *pbVar5;
//   byte *pbVar6;
//   
//   pbVar5 = (byte *)param_1;
//   bVar2 = *param_2;
//   bVar3 = *param_1;
//   bVar1 = *param_2;
//   *param_2 = *param_2 + bVar3;
//   if (CARRY1(bVar1,bVar3)) {
//     *param_2 = 0xff;
//     bVar3 = ~bVar2;
//   }
//   pbVar6 = (byte *)param_2 + bVar2;
//   uVar4 = (uint)bVar3;
//   while( true ) {
//     pbVar6 = pbVar6 + 1;
//     pbVar5 = pbVar5 + 1;
//     if (uVar4 == 0) break;
//     uVar4 = uVar4 - 1;
//     *pbVar6 = *pbVar5;
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_3f14;
begin
  { TODO: translate from asm/FUN_24dd_3f14.s — UNMATCHED until an oracle passes }
end;

