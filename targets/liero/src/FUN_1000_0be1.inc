{ liero::FUN_1000_0be1 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_0be1.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_0be1.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void FUN_1000_0be1(undefined2 param_1,undefined2 param_2,undefined2 param_3,undefined2 param_4,
//                   undefined2 param_5,undefined2 param_6)
// 
// {
//   char cVar1;
//   int iVar2;
//   undefined2 uVar3;
//   undefined2 unaff_DS;
//   undefined2 local_4;
//   
//   FUN_24dd_0530();
//   for (local_4 = 0;
//       (*(char *)((int)*(undefined4 *)0x6690 + local_4 * 0x11) != '\0' && (local_4 < 700));
//       local_4 = local_4 + 1) {
//   }
//   cVar1 = FUN_24dd_4654(2);
//   *(char *)((int)*(undefined4 *)0x6690 + local_4 * 0x11) = cVar1 + 'P';
//   *(undefined2 *)((int)*(undefined4 *)0x6690 + local_4 * 0x11 + 3) = param_6;
//   *(undefined2 *)((int)*(undefined4 *)0x6690 + local_4 * 0x11 + 7) = param_5;
//   uVar3 = (undefined2)((ulong)*(undefined4 *)0x6690 >> 0x10);
//   iVar2 = (int)*(undefined4 *)0x6690 + local_4 * 0x11;
//   *(undefined2 *)(iVar2 + 9) = param_3;
//   *(undefined2 *)(iVar2 + 0xb) = param_4;
//   uVar3 = (undefined2)((ulong)*(undefined4 *)0x6690 >> 0x10);
//   iVar2 = (int)*(undefined4 *)0x6690 + local_4 * 0x11;
//   *(undefined2 *)(iVar2 + 0xd) = param_1;
//   *(undefined2 *)(iVar2 + 0xf) = param_2;
//   return;
// }
// 
// --- end reference ---
procedure FUN_1000_0be1;
begin
  { TODO: translate from asm/FUN_1000_0be1.s — UNMATCHED until an oracle passes }
end;

