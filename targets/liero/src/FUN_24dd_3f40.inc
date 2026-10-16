{ liero::FUN_24dd_3f40 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_3f40.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_3f40.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// byte * __stdcall16far FUN_24dd_3f40(byte *param_1,byte *param_2)
// 
// {
//   byte *pbVar1;
//   int iVar2;
//   int iVar3;
//   uint uVar4;
//   byte *pbVar5;
//   byte *pbVar6;
//   byte *pbVar7;
//   undefined2 uVar8;
//   undefined2 uVar9;
//   bool bVar10;
//   
//   uVar9 = (undefined2)((ulong)param_2 >> 0x10);
//   if (*param_2 != 0) {
//     uVar4 = (uint)*param_2;
//     uVar8 = (undefined2)((ulong)param_1 >> 0x10);
//     if (uVar4 <= *param_1) {
//       iVar2 = (*param_1 - uVar4) + 1;
//       pbVar7 = (byte *)param_1 + 1;
//       pbVar6 = pbVar7;
//       do {
//         pbVar5 = (byte *)param_2 + 1;
//         bVar10 = pbVar6 == (byte *)0x0;
//         do {
//           if (iVar2 == 0) break;
//           iVar2 = iVar2 + -1;
//           pbVar1 = pbVar7;
//           pbVar7 = pbVar7 + 1;
//           bVar10 = *pbVar5 == *pbVar1;
//         } while (!bVar10);
//         if (!bVar10) {
//           return (byte *)0x0;
//         }
//         iVar3 = uVar4 - 1;
//         bVar10 = iVar3 == 0;
//         pbVar6 = pbVar7;
//         do {
//           pbVar5 = pbVar5 + 1;
//           if (iVar3 == 0) break;
//           iVar3 = iVar3 + -1;
//           pbVar1 = pbVar6;
//           pbVar6 = pbVar6 + 1;
//           bVar10 = *pbVar5 == *pbVar1;
//         } while (bVar10);
//         if (bVar10) {
//           return pbVar7 + (-1 - (int)(byte *)param_1);
//         }
//         pbVar6 = (byte *)param_2 + 1;
//       } while( true );
//     }
//   }
//   return (byte *)0x0;
// }
// 
// --- end reference ---
procedure FUN_24dd_3f40;
begin
  { TODO: translate from asm/FUN_24dd_3f40.s — UNMATCHED until an oracle passes }
end;

