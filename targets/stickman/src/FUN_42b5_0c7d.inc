{ stickman::FUN_42b5_0c7d — game Pascal draft (oracle: none).
  Drafted from asm/FUN_42b5_0c7d.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_42b5_0c7d.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// int __stdcall16far FUN_42b5_0c7d(byte *param_1,byte *param_2)
// 
// {
//   byte bVar1;
//   byte *pbVar2;
//   byte *pbVar3;
//   uint uVar4;
//   uint uVar5;
//   int iVar6;
//   byte *pbVar7;
//   byte *pbVar8;
//   undefined2 uVar9;
//   undefined2 uVar10;
//   bool bVar11;
//   
//   uVar10 = (undefined2)((ulong)param_2 >> 0x10);
//   uVar9 = (undefined2)((ulong)param_1 >> 0x10);
//   uVar5 = (uint)*param_1;
//   if (uVar5 != 0) {
//     pbVar8 = (byte *)param_1 + 1;
//     pbVar7 = (byte *)param_2 + 1;
//     bVar1 = *param_2;
//     bVar11 = bVar1 == 1;
//     if (bVar1 == 0) {
// LAB_42b5_0cbf:
//       return (int)pbVar8 - (int)(byte *)param_1;
//     }
//     if (bVar1 < 2) {
//       do {
//         if (uVar5 == 0) break;
//         uVar5 = uVar5 - 1;
//         pbVar2 = pbVar8;
//         pbVar8 = pbVar8 + 1;
//         bVar11 = *pbVar7 == *pbVar2;
//       } while (!bVar11);
//       if (bVar11) {
//         pbVar8 = pbVar8 + -1;
//         goto LAB_42b5_0cbf;
//       }
//     }
//     else {
//       uVar4 = (uint)bVar1;
//       if (uVar4 <= uVar5) {
//         iVar6 = (uVar5 - uVar4) + 1;
//         bVar11 = iVar6 == 0;
//         uVar5 = uVar4;
// code_r0x000437fb:
//         do {
//           if (uVar5 != 0) {
//             uVar5 = uVar5 - 1;
//             pbVar3 = pbVar8;
//             pbVar8 = pbVar8 + 1;
//             pbVar2 = pbVar7;
//             pbVar7 = pbVar7 + 1;
//             bVar11 = *pbVar2 == *pbVar3;
//             if (bVar11) goto code_r0x000437fb;
//           }
//           if (bVar11) {
//             pbVar8 = pbVar8 + -uVar4;
//             goto LAB_42b5_0cbf;
//           }
//           pbVar7 = pbVar7 + (uVar5 - uVar4);
//           pbVar8 = pbVar8 + (uVar5 - uVar4) + 1;
//           iVar6 = iVar6 + -1;
//           bVar11 = iVar6 == 0;
//           uVar5 = uVar4;
//         } while (!bVar11);
//       }
//     }
//   }
//   return 0;
// }
// 
// --- end reference ---
function FUN_42b5_0c7d(param_1, param_2: Pointer): Integer;
begin
  { TODO: translate from asm/FUN_42b5_0c7d.s — UNMATCHED until an oracle passes }
end;

