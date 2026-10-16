{ liero::FUN_1ec2_1008 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1ec2_1008.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1ec2_1008.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far
// FUN_1ec2_1008(byte *param_1,undefined4 param_2,byte param_3,byte param_4,int param_5,uint param_6,
//              int param_7,int param_8)
// 
// {
//   int iVar1;
//   int iVar2;
//   byte bVar3;
//   uint uVar4;
//   byte *pbVar5;
//   byte *pbVar6;
//   undefined2 uVar7;
//   undefined2 uVar8;
//   
//   if ((((param_7 < 0x9e) && (param_8 < 0x9e)) && (-1 < param_7 + param_5)) &&
//      (-1 < (int)(param_8 + param_6))) {
//     uVar8 = (undefined2)((ulong)param_1 >> 0x10);
//     pbVar5 = (byte *)param_1;
//     uVar7 = (undefined2)((ulong)param_2 >> 0x10);
//     pbVar6 = (byte *)((int)param_2 + param_7 * 0x140 + param_8);
//     iVar1 = 0x140 - (param_6 & 0xff);
//     do {
//       while (uVar4 = param_6 & 0xff, -1 < param_7) {
//         iVar2 = param_8;
//         if (0x9d < param_7) {
//           return;
//         }
//         do {
//           if (-1 < iVar2) {
//             if (0x9d < iVar2) {
//               pbVar6 = pbVar6 + uVar4 + iVar1;
//               pbVar5 = pbVar5 + uVar4;
//               goto joined_r0x0001fcb8;
//             }
//             if ((*pbVar5 != 0) &&
//                ((bVar3 = *pbVar6, bVar3 < 7 || ((param_4 <= bVar3 && (bVar3 <= param_3)))))) {
//               *pbVar6 = *pbVar5;
//             }
//           }
//           pbVar6 = pbVar6 + 1;
//           pbVar5 = pbVar5 + 1;
//           iVar2 = iVar2 + 1;
//           bVar3 = (char)uVar4 - 1;
//           uVar4 = (uint)bVar3;
//         } while (bVar3 != 0);
//         pbVar6 = pbVar6 + iVar1;
//         param_7 = param_7 + 1;
//         param_5._0_1_ = (char)param_5 + -1;
//         if ((char)param_5 == '\0') {
//           return;
//         }
//       }
//       pbVar6 = pbVar6 + 0x140;
//       pbVar5 = pbVar5 + uVar4;
// joined_r0x0001fcb8:
//       param_5._0_1_ = (char)param_5 + -1;
//       param_7 = param_7 + 1;
//     } while ((char)param_5 != '\0');
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_1ec2_1008;
begin
  { TODO: translate from asm/FUN_1ec2_1008.s — UNMATCHED until an oracle passes }
end;

