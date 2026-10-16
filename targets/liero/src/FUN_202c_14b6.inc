{ liero::FUN_202c_14b6 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_202c_14b6.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_202c_14b6.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far
// FUN_202c_14b6(uint param_1,int param_2,uint param_3,int param_4,undefined2 param_5,
//              undefined2 param_6,int param_7,byte param_8)
// 
// {
//   uint uVar1;
//   byte bVar2;
//   undefined1 uVar3;
//   uint uVar4;
//   int iVar5;
//   undefined2 uVar6;
//   undefined2 unaff_DS;
//   undefined2 local_4;
//   
//   for (local_4 = 0;
//       (*(char *)((int)*(undefined4 *)0x6694 + local_4 * 0x14 + 0x12) != '\0' && (local_4 < 600));
//       local_4 = local_4 + 1) {
//   }
//   bVar2 = param_8 & 0x7f;
//   *(byte *)((int)*(undefined4 *)0x6694 + local_4 * 0x14 + 0x12) = param_8;
//   *(undefined2 *)((int)*(undefined4 *)0x6694 + local_4 * 0x14 + 2) = param_6;
//   *(undefined2 *)((int)*(undefined4 *)0x6694 + local_4 * 0x14 + 6) = param_5;
//   uVar4 = FUN_24dd_4654(*(int *)((uint)bVar2 * 2 + 0x56c) << 1);
//   uVar1 = *(uint *)((uint)bVar2 * 2 + 0x56c);
//   uVar6 = (undefined2)((ulong)*(undefined4 *)0x6694 >> 0x10);
//   iVar5 = (int)*(undefined4 *)0x6694 + local_4 * 0x14;
//   *(int *)(iVar5 + 8) = (param_3 - uVar1) + uVar4;
//   *(int *)(iVar5 + 10) =
//        ((param_4 - ((int)uVar1 >> 0xf)) - (uint)(param_3 < uVar1)) +
//        (uint)CARRY2(param_3 - uVar1,uVar4);
//   uVar4 = FUN_24dd_4654(*(int *)((uint)bVar2 * 2 + 0x56c) << 1);
//   uVar1 = *(uint *)((uint)bVar2 * 2 + 0x56c);
//   uVar6 = (undefined2)((ulong)*(undefined4 *)0x6694 >> 0x10);
//   iVar5 = (int)*(undefined4 *)0x6694 + local_4 * 0x14;
//   *(int *)(iVar5 + 0xc) = (param_1 - uVar1) + uVar4;
//   *(int *)(iVar5 + 0xe) =
//        ((param_2 - ((int)uVar1 >> 0xf)) - (uint)(param_1 < uVar1)) +
//        (uint)CARRY2(param_1 - uVar1,uVar4);
//   if (*(char *)(bVar2 + 0x645) == '\0') {
//     if (param_7 < 1) {
//       *(undefined1 *)((int)*(undefined4 *)0x6694 + local_4 * 0x14 + 0x13) =
//            *(undefined1 *)(bVar2 + 0x68d);
//     }
//     else {
//       *(undefined1 *)((int)*(undefined4 *)0x6694 + local_4 * 0x14 + 0x13) = (undefined1)param_7;
//     }
//   }
//   else {
//     uVar3 = FUN_24dd_4654(*(byte *)(bVar2 + 0x65d) + 1);
//     *(undefined1 *)((int)*(undefined4 *)0x6694 + local_4 * 0x14 + 0x13) = uVar3;
//   }
//   iVar5 = FUN_24dd_4654(*(undefined2 *)((uint)bVar2 * 2 + 0x7c4));
//   *(int *)((int)*(undefined4 *)0x6694 + local_4 * 0x14 + 0x10) =
//        *(int *)((uint)bVar2 * 2 + 0x794) - iVar5;
//   return;
// }
// 
// --- end reference ---
procedure FUN_202c_14b6;
begin
  { TODO: translate from asm/FUN_202c_14b6.s — UNMATCHED until an oracle passes }
end;

