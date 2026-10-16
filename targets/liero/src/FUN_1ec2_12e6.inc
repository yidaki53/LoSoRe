{ liero::FUN_1ec2_12e6 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1ec2_12e6.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1ec2_12e6.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far
// FUN_1ec2_12e6(undefined1 param_1,char *param_2,undefined4 param_3,int param_4,uint param_5)
// 
// {
//   char *pcVar1;
//   byte bVar2;
//   char cVar3;
//   undefined1 uVar4;
//   char cVar5;
//   char cVar6;
//   char *pcVar7;
//   undefined1 *puVar8;
//   undefined1 *puVar9;
//   undefined2 uVar10;
//   undefined2 uVar11;
//   
//   uVar10 = (undefined2)((ulong)param_3 >> 0x10);
//   pcVar7 = (char *)param_2;
//   uVar11 = (undefined2)((ulong)param_2 >> 0x10);
//   if ((((param_5 + 8 < 8) || (0x13f < param_5 + 8)) || (param_4 + 7U < 7)) || (199 < param_4 + 7U))
//   {
//     bVar2 = (byte)param_4;
//     puVar8 = (undefined1 *)((int)param_3 + param_4 * 0x140 + param_5);
//     cVar5 = '\a';
//     do {
//       cVar6 = '\b';
//       do {
//         puVar9 = puVar8;
//         pcVar1 = pcVar7;
//         pcVar7 = pcVar7 + 1;
//         cVar3 = (char)param_5;
//         if (((param_5 < 0x140) && (bVar2 < 200)) && (*pcVar1 != '\0')) {
//           *puVar9 = param_1;
//         }
//         uVar4 = (undefined1)(param_5 >> 8);
//         param_5 = CONCAT11(uVar4,cVar3 + '\x01');
//         cVar6 = cVar6 + -1;
//         puVar8 = puVar9 + 1;
//       } while (cVar6 != '\0');
//       puVar8 = puVar9 + 0x139;
//       param_5 = CONCAT11(uVar4,cVar3 + -7);
//       bVar2 = bVar2 + 1;
//       cVar5 = cVar5 + -1;
//     } while (cVar5 != '\0');
//   }
//   else {
//     puVar8 = (undefined1 *)((int)param_3 + param_4 * 0x140 + param_5);
//     cVar5 = '\a';
//     do {
//       cVar6 = '\b';
//       do {
//         puVar9 = puVar8;
//         pcVar1 = pcVar7;
//         pcVar7 = pcVar7 + 1;
//         if (*pcVar1 != '\0') {
//           *puVar9 = param_1;
//         }
//         cVar6 = cVar6 + -1;
//         puVar8 = puVar9 + 1;
//       } while (cVar6 != '\0');
//       puVar8 = puVar9 + 0x139;
//       cVar5 = cVar5 + -1;
//     } while (cVar5 != '\0');
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_1ec2_12e6;
begin
  { TODO: translate from asm/FUN_1ec2_12e6.s — UNMATCHED until an oracle passes }
end;

