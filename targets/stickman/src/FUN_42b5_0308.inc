{ stickman::FUN_42b5_0308 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_42b5_0308.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_42b5_0308.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// uint * __cdecl16near FUN_42b5_0308(void)
// 
// {
//   uint uVar1;
//   uint uVar2;
//   uint uVar3;
//   byte bVar4;
//   int in_AX;
//   undefined2 *puVar5;
//   uint uVar6;
//   int in_DX;
//   uint uVar7;
//   uint uVar8;
//   uint *puVar9;
//   int iVar10;
//   int unaff_DS;
//   bool bVar11;
//   undefined4 uVar12;
//   uint *puVar13;
//   uint *puVar14;
//   
//   puVar9 = (uint *)0x0;
//   if (in_AX != 0) {
//     *(int *)0xed62 = in_AX;
//     while( true ) {
//       uVar12 = FUN_42b5_0491();
//       uVar8 = (uint)((ulong)uVar12 >> 0x10);
//       uVar6 = (uint)uVar12;
//       puVar9 = (uint *)0x382;
//       in_DX = unaff_DS;
//       while( true ) {
//         iVar10 = in_DX;
//         puVar14 = puVar9;
//         puVar13 = *(uint **)puVar14;
//         in_DX = (int)((ulong)puVar13 >> 0x10);
//         puVar9 = (uint *)puVar13;
//         if (in_DX == *(int *)0x37c) break;
//         uVar1 = puVar9[3];
//         bVar11 = uVar8 == uVar1;
//         if ((uVar8 <= uVar1) &&
//            ((uVar8 < uVar1 || (bVar11 = uVar6 == puVar9[2], uVar6 <= puVar9[2])))) {
//           uVar1 = puVar9[1];
//           puVar5 = (undefined2 *)*puVar13;
//           uVar7 = uVar1;
//           if (!bVar11) {
//             uVar2 = puVar9[2];
//             uVar3 = puVar9[3];
//             bVar4 = (byte)(uVar6 + (int)puVar9);
//             uVar7 = uVar8 + in_DX + (uint)(0xf < bVar4);
//             puVar5 = (undefined2 *)
//                      (CONCAT11((char)(uVar6 + (int)puVar9 >> 8),bVar4 - 0x10) & 0xff0f);
//             *puVar5 = (undefined2 *)*puVar13;
//             puVar5[1] = uVar1;
//             puVar5[2] = uVar2 - uVar6 & 0xf;
//             puVar5[3] = (uVar3 - uVar8) - (uint)(uVar2 < uVar6);
//           }
//           *puVar14 = (uint)puVar5;
//           puVar14[1] = uVar7;
//           goto LAB_42b5_0382;
//         }
//       }
//       bVar4 = (byte)(uVar6 + (int)puVar9);
//       uVar8 = uVar8 + in_DX + (uint)(0xf < bVar4);
//       uVar6 = CONCAT11((char)(uVar6 + (int)puVar9 >> 8),bVar4 - 0x10) & 0xff0f;
//       if ((uVar8 < *(uint *)0x380) || ((uVar8 <= *(uint *)0x380 && (uVar6 <= *(uint *)0x37e)))) {
//         *(uint *)0x37a = uVar6;
//         *(uint *)0x37c = uVar8;
//         *puVar14 = uVar6;
//         puVar14[1] = uVar8;
//         puVar14 = (uint *)0x0;
//         (*(code *)*(undefined2 *)0x38a)(0x42b5,0,puVar9,in_DX);
//         return (uint *)CONCAT22(puVar9,puVar14);
//       }
//       puVar13 = (uint *)(*(code *)*(undefined2 *)0x38a)(0x42b5,*(undefined2 *)0xed62);
//       in_DX = (int)((ulong)puVar13 >> 0x10);
//       puVar9 = (uint *)puVar13;
//       if ((char)puVar13 == '\0') break;
//       if ((char)puVar13 == '\x01') {
//         return (uint *)0x0;
//       }
//     }
//   }
// LAB_42b5_0382:
//   return (uint *)CONCAT22(in_DX,puVar9);
// }
// 
// --- end reference ---
procedure FUN_42b5_0308;
begin
  { TODO: translate from asm/FUN_42b5_0308.s — UNMATCHED until an oracle passes }
end;

