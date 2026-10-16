{ liero::FUN_1ec2_0e8f — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1ec2_0e8f.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1ec2_0e8f.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far
// FUN_1ec2_0e8f(char *param_1,undefined4 param_2,int param_3,uint param_4,int param_5,int param_6)
// 
// {
//   int iVar1;
//   int iVar2;
//   byte bVar3;
//   uint uVar4;
//   char *pcVar5;
//   char *pcVar6;
//   
//   if ((((param_5 < 0x9e) && (param_6 < 0x9e)) && (-1 < param_5 + param_3)) &&
//      (-1 < (int)(param_6 + param_4))) {
//     pcVar5 = (char *)param_1;
//     pcVar6 = (char *)((int)param_2 + param_5 * 0x140 + param_6);
//     iVar1 = 0x140 - (param_4 & 0xff);
//     do {
//       while (uVar4 = param_4 & 0xff, -1 < param_5) {
//         iVar2 = param_6;
//         if (0x9d < param_5) {
//           return;
//         }
//         do {
//           if (-1 < iVar2) {
//             if (0x9d < iVar2) {
//               pcVar6 = pcVar6 + uVar4 + iVar1;
//               pcVar5 = pcVar5 + uVar4;
//               goto joined_r0x0001fb40;
//             }
//             if (*pcVar5 != '\0') {
//               *pcVar6 = *pcVar5;
//             }
//           }
//           pcVar6 = pcVar6 + 1;
//           pcVar5 = pcVar5 + 1;
//           iVar2 = iVar2 + 1;
//           bVar3 = (char)uVar4 - 1;
//           uVar4 = (uint)bVar3;
//         } while (bVar3 != 0);
//         pcVar6 = pcVar6 + iVar1;
//         param_5 = param_5 + 1;
//         param_3._0_1_ = (char)param_3 + -1;
//         if ((char)param_3 == '\0') {
//           return;
//         }
//       }
//       pcVar6 = pcVar6 + 0x140;
//       pcVar5 = pcVar5 + param_4;
// joined_r0x0001fb40:
//       param_3._0_1_ = (char)param_3 + -1;
//       param_5 = param_5 + 1;
//     } while ((char)param_3 != '\0');
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_1ec2_0e8f;
begin
  { TODO: translate from asm/FUN_1ec2_0e8f.s — UNMATCHED until an oracle passes }
end;

