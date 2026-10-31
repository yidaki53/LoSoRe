{ stickman::FUN_42b5_07da — game Pascal draft (oracle: none).
  Drafted from asm/FUN_42b5_07da.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_42b5_07da.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined4 __cdecl16near FUN_42b5_07da(undefined4 param_1)
// 
// {
//   undefined2 in_AX;
//   int iVar1;
//   int in_DX;
//   int in_BX;
//   int unaff_DI;
//   int iVar2;
//   undefined2 unaff_ES;
//   undefined2 uVar3;
//   
//   *(undefined1 *)(in_BX + unaff_DI) = (char)in_AX;
//   if (in_BX + 1 != in_DX) {
//     return CONCAT22(in_DX,in_AX);
//   }
//   uVar3 = (undefined2)((ulong)param_1 >> 0x10);
//   iVar2 = (int)param_1;
//   *(int *)(iVar2 + 8) = in_BX + 1;
//   iVar1 = (*(code *)*(undefined2 *)(iVar2 + 0x14))(0x42b5,iVar2,uVar3,iVar2,uVar3);
//   if (iVar1 != 0) {
//     DAT_4473_039c = iVar1;
//   }
//   return CONCAT22(*(undefined2 *)(iVar2 + 4),*(undefined2 *)(iVar2 + 10));
// }
// 
// --- end reference ---
function FUN_42b5_07da(param_1: Longint): Longint;
begin
  { TODO: translate from asm/FUN_42b5_07da.s — UNMATCHED until an oracle passes }
end;

