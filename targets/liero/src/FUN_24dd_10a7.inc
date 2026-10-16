{ liero::FUN_24dd_10a7 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_10a7.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_10a7.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void FUN_24dd_10a7(int *param_1,int param_2,int param_3)
// 
// {
//   uint uVar1;
//   uint uVar2;
//   ulong uVar3;
//   ulong uVar4;
//   uint uVar5;
//   int iVar6;
//   byte bVar7;
//   undefined2 in_CX;
//   uint uVar8;
//   uint uVar9;
//   int iVar10;
//   uint uVar11;
//   undefined2 unaff_ES;
//   undefined2 unaff_DS;
//   bool bVar12;
//   bool bVar13;
//   long lVar14;
//   
//   bVar7 = *(byte *)(param_3 + 10) ^ *(byte *)(param_2 + 10);
//   uVar8 = CONCAT11((char)((uint)in_CX >> 8),bVar7);
//   uVar11 = *(uint *)(param_2 + 8);
//   uVar1 = *(uint *)(param_3 + 8);
//   bVar12 = uVar1 < 0x4001;
//   if ((int)uVar1 < 0x4001) {
//     bVar12 = uVar11 < 0x4001;
//     if ((int)uVar11 < 0x4001) {
//       uVar5 = uVar1;
//       if ((int)uVar11 <= (int)uVar1) {
//         uVar5 = uVar11;
//         uVar11 = uVar1;
//       }
//       if (-0x3fff < (int)uVar5) {
//         iVar6 = uVar5 + uVar11;
//         if (iVar6 + -1 < 0x4001) {
//           if (iVar6 < -0x3ffe) {
//             FUN_24dd_2361();
//             goto LAB_24dd_112d;
//           }
//           FUN_24dd_0628();
//           FUN_24dd_0628();
//           lVar14 = FUN_24dd_1190();
//           *(int *)0xd8 = *(int *)0xd8 + 0x18;
//           if (-1 < lVar14) {
//             iVar6 = iVar6 + -1;
//             bVar13 = param_2 < 0;
//             param_2 = param_2 << 1;
//             uVar3 = (ulong)CONCAT12(bVar13,(int)lVar14) << 1;
//             bVar12 = (uVar3 & 0x10000) != 0;
//             uVar4 = (ulong)CONCAT12(bVar12,uVar11) << 1;
//             uVar11 = (uint)uVar4 | (uint)bVar12;
//             bVar12 = (uVar4 & 0x10000) != 0;
//             uVar4 = (ulong)CONCAT12(bVar12,uVar8) << 1;
//             uVar8 = (uint)uVar4 | (uint)bVar12;
//             lVar14 = CONCAT22((int)((ulong)lVar14 >> 0x10) << 1 | (uint)((uVar4 & 0x10000) != 0),
//                               (uint)uVar3 | (uint)bVar13);
//           }
//           uVar9 = (uint)((ulong)lVar14 >> 0x10);
//           uVar1 = (uint)CARRY2((uint)lVar14,(uint)(param_2 < 0));
//           uVar5 = (uint)CARRY2(uVar11,uVar1);
//           uVar2 = (uint)CARRY2(uVar8,uVar5);
//           iVar10 = uVar9 + uVar2;
//           if (CARRY2(uVar9,uVar2)) {
//             iVar10 = (int)(CONCAT12(1,iVar10) >> 1);
//             iVar6 = iVar6 + 1;
//           }
//           if (iVar6 < 0x4001) {
//             *param_1 = (uint)lVar14 + (uint)(param_2 < 0);
//             param_1[1] = uVar11 + uVar1;
//             param_1[2] = uVar8 + uVar5;
//             param_1[3] = iVar10;
//             param_1[4] = iVar6;
//             param_1[5] = (uint)bVar7;
//             return;
//           }
//         }
//         FUN_24dd_2361();
//       }
//       goto LAB_24dd_112d;
//     }
//     FUN_24dd_0e57();
//     if (bVar12) {
//       return;
//     }
//     iVar6 = *(int *)(param_3 + 8);
//   }
//   else {
//     FUN_24dd_0e57();
//     if (bVar12) {
//       return;
//     }
//     iVar6 = *(int *)(param_2 + 8);
//   }
//   if (iVar6 < -0x3ffe) {
//     FUN_24dd_060f();
//     return;
//   }
// LAB_24dd_112d:
//   FUN_24dd_05fd();
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_10a7;
begin
  { TODO: translate from asm/FUN_24dd_10a7.s — UNMATCHED until an oracle passes }
end;

