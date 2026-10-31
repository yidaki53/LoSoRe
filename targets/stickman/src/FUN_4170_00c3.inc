{ stickman::FUN_4170_00c3 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_4170_00c3.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_4170_00c3.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_4170_00c3(byte *param_1)
// 
// {
//   byte bVar1;
//   byte bVar2;
//   undefined2 uVar3;
//   uint local_4;
//   
//   FUN_42b5_04df();
//   if ((*param_1 != 0) && (bVar1 = *param_1, bVar1 != 0)) {
//     local_4 = 1;
//     while( true ) {
//       uVar3 = (undefined2)((ulong)param_1 >> 0x10);
//       bVar2 = FUN_42b5_1bc4(CONCAT11((char)(local_4 >> 8),((byte *)param_1)[local_4]));
//       ((byte *)param_1)[local_4] = bVar2;
//       if (local_4 == bVar1) break;
//       local_4 = local_4 + 1;
//     }
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_4170_00c3(param_1: Pointer);
begin
  { TODO: translate from asm/FUN_4170_00c3.s — UNMATCHED until an oracle passes }
end;

