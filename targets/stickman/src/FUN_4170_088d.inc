{ stickman::FUN_4170_088d — game Pascal draft (oracle: none).
  Drafted from asm/FUN_4170_088d.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_4170_088d.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void FUN_4170_088d(undefined2 param_1,uint *param_2,undefined2 *param_3)
// 
// {
//   uint uVar1;
//   int in_DX;
//   undefined4 uVar2;
//   undefined2 uVar3;
//   undefined2 uVar4;
//   
//   uVar4 = 0x4170;
//   uVar3 = 0x1f98;
//   FUN_42b5_04df();
//   uVar1 = FUN_42b5_02b8(uVar3,uVar4);
//   if ((0 < in_DX) || ((-1 < in_DX && (0xfff0 < uVar1)))) {
//     uVar1 = 0xfff0;
//     in_DX = 0;
//   }
//   *param_2 = uVar1;
//   uVar3 = (undefined2)((ulong)param_3 >> 0x10);
//   if ((in_DX < 0) || ((in_DX < 1 && (uVar1 < 0x200)))) {
//     *param_3 = 0;
//     ((undefined2 *)param_3)[1] = 0;
//   }
//   else {
//     uVar2 = FUN_42b5_023f(*param_2);
//     *param_3 = (int)uVar2;
//     ((undefined2 *)param_3)[1] = (int)((ulong)uVar2 >> 0x10);
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_4170_088d(param_1: Word; param_2, param_3: Pointer);
begin
  { TODO: translate from asm/FUN_4170_088d.s — UNMATCHED until an oracle passes }
end;

