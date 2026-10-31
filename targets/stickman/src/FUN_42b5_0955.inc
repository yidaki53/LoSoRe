{ stickman::FUN_42b5_0955 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_42b5_0955.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_42b5_0955.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined2 __cdecl16far FUN_42b5_0955(undefined4 param_1)
// 
// {
//   byte bVar1;
//   undefined2 uVar2;
//   int in_BX;
//   int iVar3;
//   undefined2 unaff_SS;
//   undefined2 unaff_DS;
//   undefined1 uVar4;
//   bool bVar5;
//   byte local_22 [32];
//   
//   uVar4 = &stack0xfffe < (undefined1 *)0x20;
//   bVar5 = &stack0x0000 == (undefined1 *)0x22;
//   FUN_42b5_0776();
//   iVar3 = 0;
//   if (bVar5) {
//     while( true ) {
//       bVar1 = FUN_42b5_079a();
//       uVar4 = bVar1 < 0x1a;
//       if (bVar1 == 0x1a) break;
//       if (0x20 < bVar1) goto LAB_42b5_0976;
//       in_BX = in_BX + 1;
//     }
//   }
// LAB_42b5_0989:
//   *(int *)((int)param_1 + 8) = in_BX;
//   if (iVar3 != 0) {
//     uVar2 = FUN_42b5_1387();
//     if ((!(bool)uVar4) && (iVar3 == 0)) {
//       return uVar2;
//     }
//     *(undefined2 *)0x39c = 0x6a;
//   }
//   return 0;
// LAB_42b5_0976:
//   while( true ) {
//     bVar1 = FUN_42b5_079a();
//     uVar4 = bVar1 < 0x20;
//     if (bVar1 < 0x21) break;
//     in_BX = in_BX + 1;
//     if (iVar3 != 0x20) {
//       local_22[iVar3] = bVar1;
//       iVar3 = iVar3 + 1;
//     }
//   }
//   goto LAB_42b5_0989;
// }
// 
// --- end reference ---
function FUN_42b5_0955(param_1: Longint): Word;
begin
  { TODO: translate from asm/FUN_42b5_0955.s — UNMATCHED until an oracle passes }
end;

