{ stickman::FUN_1000_0c8f — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_0c8f.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_0c8f.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined4 FUN_1000_0c8f(uint param_1,uint param_2)
// 
// {
//   long lVar1;
//   uint uVar2;
//   uint uVar3;
//   undefined2 uVar4;
//   undefined2 unaff_DS;
//   int *local_a;
//   uint local_6;
//   undefined1 local_3;
//   
//   FUN_42b5_04df();
//   local_3 = 1;
//   lVar1 = (ulong)param_1 * 0x50;
//   if (*(char *)((int)lVar1 + param_2 + 0x1f6f) == '\0') {
//     local_6 = 1;
//     while( true ) {
//       uVar4 = (undefined2)((ulong)local_6 * 0x275 >> 0x10);
//       uVar2 = (uint)((ulong)local_6 * 0x275);
//       _local_a = (int *)CONCAT22(unaff_DS,(int *)(uVar2 + 0x459));
//       uVar3 = uVar2;
//       if ((((*_local_a != 0) && (uVar3 = param_2, *_local_a <= (int)param_2)) &&
//           (uVar3 = (*_local_a + *(int *)(uVar2 + 0x465)) - 1, (int)param_2 <= (int)uVar3)) &&
//          (uVar3 = param_1, *(int *)(uVar2 + 0x45b) <= (int)param_1)) {
//         uVar3 = (*(int *)(uVar2 + 0x45b) + *(int *)(uVar2 + 0x467)) - 1;
//         lVar1 = CONCAT22(uVar4,uVar3);
//         if ((int)param_1 <= (int)uVar3) goto LAB_1000_0d26;
//       }
//       lVar1 = CONCAT22(uVar4,uVar3);
//       if (local_6 == 10) break;
//       local_6 = local_6 + 1;
//     }
//     local_3 = 0;
//   }
// LAB_1000_0d26:
//   return CONCAT22((int)((ulong)lVar1 >> 0x10),CONCAT11((char)((ulong)lVar1 >> 8),local_3));
// }
// 
// --- end reference ---
function FUN_1000_0c8f(param_1, param_2: Word): Longint;
begin
  { TODO: translate from asm/FUN_1000_0c8f.s — UNMATCHED until an oracle passes }
end;

