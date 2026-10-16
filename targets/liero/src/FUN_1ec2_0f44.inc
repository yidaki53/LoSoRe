{ liero::FUN_1ec2_0f44 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1ec2_0f44.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1ec2_0f44.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far
// FUN_1ec2_0f44(char *param_1,undefined4 param_2,char param_3,byte param_4,byte param_5,int param_6,
//              uint param_7,int param_8,int param_9)
// 
// {
//   int iVar1;
//   int iVar2;
//   byte bVar3;
//   uint uVar4;
//   char *pcVar5;
//   byte *pbVar6;
//   undefined2 uVar7;
//   
//   if ((((param_8 < 0x9e) && (param_9 < 0x9e)) && (-1 < param_8 + param_6)) &&
//      (-1 < (int)(param_9 + param_7))) {
//     pcVar5 = (char *)param_1;
//     uVar7 = (undefined2)((ulong)param_2 >> 0x10);
//     pbVar6 = (byte *)((int)param_2 + param_8 * 0x140 + param_9);
//     iVar1 = 0x140 - (param_7 & 0xff);
//     do {
//       while (uVar4 = param_7 & 0xff, -1 < param_8) {
//         iVar2 = param_9;
//         if (0x9d < param_8) {
//           return;
//         }
//         do {
//           if (-1 < iVar2) {
//             if (0x9d < iVar2) {
//               pbVar6 = pbVar6 + uVar4 + iVar1;
//               pcVar5 = pcVar5 + uVar4;
//               goto joined_r0x0001fbf4;
//             }
//             if (((*pcVar5 != '\0') && (bVar3 = *pbVar6, param_5 <= bVar3)) && (bVar3 <= param_4)) {
//               *pbVar6 = bVar3 + param_3;
//             }
//           }
//           pbVar6 = pbVar6 + 1;
//           pcVar5 = pcVar5 + 1;
//           iVar2 = iVar2 + 1;
//           bVar3 = (char)uVar4 - 1;
//           uVar4 = (uint)bVar3;
//         } while (bVar3 != 0);
//         pbVar6 = pbVar6 + iVar1;
//         param_8 = param_8 + 1;
//         param_6._0_1_ = (char)param_6 + -1;
//         if ((char)param_6 == '\0') {
//           return;
//         }
//       }
//       pbVar6 = pbVar6 + 0x140;
//       pcVar5 = pcVar5 + uVar4;
// joined_r0x0001fbf4:
//       param_6._0_1_ = (char)param_6 + -1;
//       param_8 = param_8 + 1;
//     } while ((char)param_6 != '\0');
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_1ec2_0f44;
begin
  { TODO: translate from asm/FUN_1ec2_0f44.s — UNMATCHED until an oracle passes }
end;

