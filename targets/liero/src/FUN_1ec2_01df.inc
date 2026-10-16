{ liero::FUN_1ec2_01df — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1ec2_01df.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1ec2_01df.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far
// FUN_1ec2_01df(char param_1,char param_2,undefined4 param_3,undefined1 *param_4,int param_5,
//              int param_6)
// 
// {
//   undefined1 *puVar1;
//   undefined1 *puVar2;
//   int iVar3;
//   undefined1 *puVar4;
//   undefined1 *puVar5;
//   undefined2 uVar6;
//   undefined2 uVar7;
//   undefined2 unaff_SS;
//   int local_108;
//   int local_104;
//   undefined1 local_102 [256];
//   
//   puVar5 = local_102;
//   puVar4 = (undefined1 *)param_4;
//   for (iVar3 = 0x100; iVar3 != 0; iVar3 = iVar3 + -1) {
//     puVar2 = puVar5;
//     puVar5 = puVar5 + 1;
//     puVar1 = puVar4;
//     puVar4 = puVar4 + 1;
//     *puVar2 = *puVar1;
//   }
//   uVar6 = (undefined2)param_3;
//   uVar7 = (undefined2)((ulong)param_3 >> 0x10);
//   if (param_1 == '\0') {
//     if (param_2 == '\0') {
//       local_108 = 0;
//       while( true ) {
//         for (local_104 = 2;
//             FUN_1ec2_0dc8(uVar6,uVar7,
//                           CONCAT11((char)((uint)local_104 >> 8),
//                                    local_102[local_108 * 0x10 + local_104]),param_5 + local_108,
//                           (0xe - local_104) + param_6), local_104 != 0xb; local_104 = local_104 + 1)
//         {
//         }
//         if (local_108 == 8) break;
//         local_108 = local_108 + 1;
//       }
//     }
//     else {
//       local_108 = 0;
//       while( true ) {
//         for (local_104 = 2;
//             FUN_1ec2_0dc8(uVar6,uVar7,
//                           CONCAT11((char)((uint)local_104 >> 8),
//                                    local_102[local_108 * 0x10 + local_104]),param_5 + local_108,
//                           param_6 + local_104), local_104 != 0xb; local_104 = local_104 + 1) {
//         }
//         if (local_108 == 8) break;
//         local_108 = local_108 + 1;
//       }
//     }
//   }
//   else if (param_1 == '\x01') {
//     if (param_2 == '\0') {
//       local_108 = 0;
//       while( true ) {
//         for (local_104 = 2;
//             FUN_1ec2_0e06(uVar6,uVar7,
//                           CONCAT11((char)((uint)local_104 >> 8),
//                                    local_102[local_108 * 0x10 + local_104]),param_5 + local_108,
//                           (0xe - local_104) + param_6), local_104 != 0xb; local_104 = local_104 + 1)
//         {
//         }
//         if (local_108 == 8) break;
//         local_108 = local_108 + 1;
//       }
//     }
//     else {
//       local_108 = 0;
//       while( true ) {
//         for (local_104 = 2;
//             FUN_1ec2_0e06(uVar6,uVar7,
//                           CONCAT11((char)((uint)local_104 >> 8),
//                                    local_102[local_108 * 0x10 + local_104]),param_5 + local_108,
//                           param_6 + local_104), local_104 != 0xb; local_104 = local_104 + 1) {
//         }
//         if (local_108 == 8) break;
//         local_108 = local_108 + 1;
//       }
//     }
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_1ec2_01df;
begin
  { TODO: translate from asm/FUN_1ec2_01df.s — UNMATCHED until an oracle passes }
end;

