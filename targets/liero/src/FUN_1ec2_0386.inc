{ liero::FUN_1ec2_0386 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1ec2_0386.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1ec2_0386.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far
// FUN_1ec2_0386(char param_1,char param_2,undefined4 param_3,byte *param_4,int param_5,int param_6)
// 
// {
//   byte *pbVar1;
//   byte *pbVar2;
//   int iVar3;
//   byte *pbVar4;
//   byte *pbVar5;
//   undefined2 uVar6;
//   undefined2 uVar7;
//   undefined2 unaff_SS;
//   int local_108;
//   int local_104;
//   byte local_102 [256];
//   
//   pbVar5 = local_102;
//   pbVar4 = (byte *)param_4;
//   for (iVar3 = 0x100; iVar3 != 0; iVar3 = iVar3 + -1) {
//     pbVar2 = pbVar5;
//     pbVar5 = pbVar5 + 1;
//     pbVar1 = pbVar4;
//     pbVar4 = pbVar4 + 1;
//     *pbVar2 = *pbVar1;
//   }
//   uVar6 = (undefined2)param_3;
//   uVar7 = (undefined2)((ulong)param_3 >> 0x10);
//   if (param_1 == '\0') {
//     if (param_2 == '\0') {
//       local_108 = 0;
//       while( true ) {
//         local_104 = 2;
//         while( true ) {
//           if (0x74 < local_102[local_108 * 0x10 + local_104]) {
//             FUN_1ec2_0dc8(uVar6,uVar7,local_102[local_108 * 0x10 + local_104] - 5,
//                           param_5 + local_108,(0xe - local_104) + param_6);
//           }
//           if (local_104 == 0xd) break;
//           local_104 = local_104 + 1;
//         }
//         if (local_108 == 0xf) break;
//         local_108 = local_108 + 1;
//       }
//     }
//     else {
//       local_108 = 0;
//       while( true ) {
//         local_104 = 2;
//         while( true ) {
//           if (0x74 < local_102[local_108 * 0x10 + local_104]) {
//             FUN_1ec2_0dc8(uVar6,uVar7,local_102[local_108 * 0x10 + local_104] - 5,
//                           param_5 + local_108,param_6 + local_104);
//           }
//           if (local_104 == 0xd) break;
//           local_104 = local_104 + 1;
//         }
//         if (local_108 == 0xf) break;
//         local_108 = local_108 + 1;
//       }
//     }
//   }
//   else if (param_1 == '\x01') {
//     if (param_2 == '\0') {
//       local_108 = 0;
//       while( true ) {
//         local_104 = 2;
//         while( true ) {
//           if (0x72 < local_102[local_108 * 0x10 + local_104]) {
//             FUN_1ec2_0dc8(uVar6,uVar7,local_102[local_108 * 0x10 + local_104] - 3,
//                           param_5 + local_108,(0xe - local_104) + param_6);
//           }
//           if (local_104 == 0xd) break;
//           local_104 = local_104 + 1;
//         }
//         if (local_108 == 0xf) break;
//         local_108 = local_108 + 1;
//       }
//     }
//     else {
//       local_108 = 0;
//       while( true ) {
//         local_104 = 2;
//         while( true ) {
//           if (0x72 < local_102[local_108 * 0x10 + local_104]) {
//             FUN_1ec2_0dc8(uVar6,uVar7,local_102[local_108 * 0x10 + local_104] - 3,
//                           param_5 + local_108,param_6 + local_104);
//           }
//           if (local_104 == 0xd) break;
//           local_104 = local_104 + 1;
//         }
//         if (local_108 == 0xf) break;
//         local_108 = local_108 + 1;
//       }
//     }
//   }
//   else if (param_1 == '\x02') {
//     if (param_2 == '\0') {
//       local_108 = 0;
//       while( true ) {
//         local_104 = 2;
//         while( true ) {
//           if (0x70 < local_102[local_108 * 0x10 + local_104]) {
//             FUN_1ec2_0dc8(uVar6,uVar7,local_102[local_108 * 0x10 + local_104] - 1,
//                           param_5 + local_108,(0xe - local_104) + param_6);
//           }
//           if (local_104 == 0xd) break;
//           local_104 = local_104 + 1;
//         }
//         if (local_108 == 0xf) break;
//         local_108 = local_108 + 1;
//       }
//     }
//     else {
//       local_108 = 0;
//       while( true ) {
//         local_104 = 2;
//         while( true ) {
//           if (0x70 < local_102[local_108 * 0x10 + local_104]) {
//             FUN_1ec2_0dc8(uVar6,uVar7,local_102[local_108 * 0x10 + local_104] - 1,
//                           param_5 + local_108,param_6 + local_104);
//           }
//           if (local_104 == 0xd) break;
//           local_104 = local_104 + 1;
//         }
//         if (local_108 == 0xf) break;
//         local_108 = local_108 + 1;
//       }
//     }
//   }
//   else if (param_2 == '\0') {
//     local_108 = 0;
//     while( true ) {
//       for (local_104 = 2; iVar3 = (0xe - local_104) + param_6,
//           FUN_1ec2_0dc8(uVar6,uVar7,
//                         CONCAT11((char)((uint)iVar3 >> 8),local_102[local_108 * 0x10 + local_104]),
//                         param_5 + local_108,iVar3), local_104 != 0xd; local_104 = local_104 + 1) {
//       }
//       if (local_108 == 0xf) break;
//       local_108 = local_108 + 1;
//     }
//   }
//   else {
//     local_108 = 0;
//     while( true ) {
//       for (local_104 = 2;
//           FUN_1ec2_0dc8(uVar6,uVar7,
//                         CONCAT11((char)((uint)(param_6 + local_104) >> 8),
//                                  local_102[local_108 * 0x10 + local_104]),param_5 + local_108,
//                         param_6 + local_104), local_104 != 0xd; local_104 = local_104 + 1) {
//       }
//       if (local_108 == 0xf) break;
//       local_108 = local_108 + 1;
//     }
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_1ec2_0386;
begin
  { TODO: translate from asm/FUN_1ec2_0386.s — UNMATCHED until an oracle passes }
end;

