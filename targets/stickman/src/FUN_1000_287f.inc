{ stickman::FUN_1000_287f — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_287f.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_287f.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined1 FUN_1000_287f(int param_1,int param_2)
// 
// {
//   undefined2 uVar1;
//   char cVar2;
//   int iVar3;
//   int iVar4;
//   undefined2 unaff_DS;
//   int *local_10;
//   int local_8;
//   int local_6;
//   undefined1 local_3;
//   
//   FUN_42b5_04df();
//   local_3 = 0;
//   iVar3 = *(int *)(param_1 * 0x275 + 0x465) + param_2 + -1;
//   if ((0 < param_2) && (iVar3 < 0x50)) {
//     if ((*(int *)0x3ae + 1 < param_2) ||
//        (((iVar3 < *(int *)0x3ae + -1 || (*(int *)0x3b0 + 2 < *(int *)(param_1 * 0x275 + 0x45b))) ||
//         (*(int *)(param_1 * 0x275 + 0x45b) + *(int *)(param_1 * 0x275 + 0x467) + -1 < *(int *)0x3b0)
//         ))) {
//       iVar4 = *(int *)(param_1 * 0x275 + 0x45b) + *(int *)(param_1 * 0x275 + 0x467) + -1;
//       local_6 = *(int *)(param_1 * 0x275 + 0x45b);
//       if (local_6 <= iVar4) {
//         while( true ) {
//           if (param_2 <= iVar3) {
//             local_8 = param_2;
//             while( true ) {
//               uVar1 = *(undefined2 *)(param_1 * 0x275 + 0x459);
//               *(undefined2 *)(param_1 * 0x275 + 0x459) = 0;
//               cVar2 = FUN_1000_0c8f(local_6,local_8);
//               *(undefined2 *)(param_1 * 0x275 + 0x459) = uVar1;
//               if (cVar2 != '\0') {
//                 return 0;
//               }
//               if (local_8 == iVar3) break;
//               local_8 = local_8 + 1;
//             }
//           }
//           if (local_6 == iVar4) break;
//           local_6 = local_6 + 1;
//         }
//       }
//       iVar4 = *(int *)(param_1 * 0x275 + 0x45b) + *(int *)(param_1 * 0x275 + 0x467);
//       if ((iVar4 < 0x14) && (param_2 <= iVar3)) {
//         local_8 = param_2;
//         while (*(char *)(iVar4 * 0x50 + local_8 + 0x1f6f) != '\0') {
//           if (local_8 == iVar3) goto LAB_1000_29fd;
//           local_8 = local_8 + 1;
//         }
//       }
//       else {
// LAB_1000_29fd:
//         param_1 = param_1 * 0x275;
//         _local_10 = (int *)CONCAT22(unaff_DS,(int *)(param_1 + 0x459));
//         if ((((*(int *)(param_1 + 0x463) != 1) || (*(int *)0x3b0 < *(int *)(param_1 + 0x45b))) ||
//             (*(int *)(param_1 + 0x467) <= *(int *)0x3b0 - *(int *)(param_1 + 0x45b))) ||
//            (((*(int *)(param_1 + 0x45f) < 1 || (*_local_10 <= *(int *)0x3ae)) &&
//             ((-1 < *(int *)(param_1 + 0x45f) || (*(int *)0x3ae <= *_local_10)))))) {
//           local_3 = 1;
//         }
//       }
//     }
//     else {
//       FUN_1000_1735(1);
//       FUN_1000_06a1();
//     }
//   }
//   return local_3;
// }
// 
// --- end reference ---
function FUN_1000_287f(param_1, param_2: Integer): Byte;
begin
  { TODO: translate from asm/FUN_1000_287f.s — UNMATCHED until an oracle passes }
end;

