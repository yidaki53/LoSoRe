{ liero-dos::FUN_1ec2_0386 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1ec2_0386.s via skeleton(compile-gate); UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1ec2_0386.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: recon:real decompiler C (unmatched) ---
// #include <stdint.h>
// 
// void FUN_1ec2_0386(char param_1, char param_2, uint32_t param_3, uint8_t *param_4, int param_5, int param_6) {
//     uint8_t local_102[256];
//     int local_108;
//     int local_104;
//     uint16_t uVar6 = (uint16_t)param_3;
//     uint16_t uVar7 = (uint16_t)(param_3 >> 16);
// 
//     for (int i = 0; i < 256; i++) {
//         local_102[i] = param_4[i];
//     }
// 
//     if (param_1 == '\0') {
//         if (param_2 == '\0') {
//             for (local_108 = 0; local_108 < 16; local_108++) {
//                 for (local_104 = 2; local_104 < 14; local_104++) {
//                     if (local_102[local_108 * 16 + local_104] > 0x74) {
//                         FUN_1ec2_0dc8(uVar6, uVar7, local_102[local_108 * 16 + local_104] - 5,
//                                       param_5 + local_108, (0xe - local_104) + param_6);
//                     }
//                 }
//             }
//         } else {
//             for (local_108 = 0; local_108 < 16; local_108++) {
//                 for (local_104 = 2; local_104 < 14; local_104++) {
//                     if (local_102[local_108 * 16 + local_104] > 0x74) {
//                         FUN_1ec2_0dc8(uVar6, uVar7, local_102[local_108 * 16 + local_104] - 5,
//                                       param_5 + local_108, param_6 + local_104);
//                     }
//                 }
//             }
//         }
//     } else if (param_1 == '\x01') {
//         if (param_2 == '\0') {
//             for (local_108 = 0; local_108 < 16; local_108++) {
//                 for (local_104 = 2; local_104 < 14; local_104++) {
//                     if (local_102[local_108 * 16 + local_104] > 0x72) {
//                         FUN_1ec2_0dc8(uVar6, uVar7, local_102[local_108 * 16 + local_104] - 3,
//                                       param_5 + local_108, (0xe - local_104) + param_6);
//                     }
//                 }
//             }
//         } else {
//             for (local_108 = 0; local_108 < 16; local_108++) {
//                 for (local_104 = 2; local_104 < 14; local_104++) {
//                     if (local_102[local_108 * 16 + local_104] > 0x72) {
//                         FUN_1ec2_0dc8(uVar6, uVar7, local_102[local_108 * 16 + local_104] - 3,
//                                       param_5 + local_108, param_6 + local_104);
//                     }
//                 }
//             }
//         }
//     } else if (param_1 == '\x02') {
//         if (param_2 == '\0') {
//             for (local_108 = 0; local_108 < 16; local_108++) {
//                 for (local_104 = 2; local_104 < 14; local_104++) {
//                     if (local_102[local_108 * 16 + local_104] > 0x70) {
//                         FUN_1ec2_0dc8(uVar6, uVar7, local_102[local_108 * 16 + local_104] - 1,
//                                       param_5 + local_108, (0xe - local_104) + param_6);
//                     }
//                 }
//             }
//         } else {
//             for (local_108 = 0; local_108 < 16; local_108++) {
//                 for (local_104 = 2; local_104 < 14; local_104++) {
//                     if (local_102[local_108 * 16 + local_104] > 0x70) {
//                         FUN_1ec2_0dc8(uVar6, uVar7, local_102[local_108 * 16 + local_104] - 1,
//                                       param_5 + local_108, param_6 + local_104);
//                     }
//                 }
//             }
//         }
//     } else if (param_2 == '\0') {
//         for (local_108 = 0; local_108 < 16; local_108++) {
//             for (local_104 = 2; local_104 < 14; local_104++) {
//                 int iVar3 = (0xe - local_104) + param_6;
//                 FUN_1ec2_0dc8(uVar6, uVar7,
//                               ((uint16_t)((uint8_t)(iVar3 >> 8)) << 8) | local_102[local_108 * 16 + local_104],
//                               param_5 + local_108, iVar3);
//             }
//         }
//     } else {
//         for (local_108 = 0; local_108 < 16; local_108++) {
//             for (local_104 = 2; local_104 < 14; local_104++) {
//                 FUN_1ec2_0dc8(uVar6, uVar7,
//                               ((uint16_t)((uint8_t)((param_6 + local_104) >> 8)) << 8) | local_102[local_108 * 16 + local_104],
//                               param_5 + local_108, param_6 + local_104);
//             }
//         }
//     }
// }
// --- end reference ---
procedure FUN_1ec2_0386(param_1, param_2: Char; param_3: Longint; param_4: Pointer; param_5, param_6: Integer);
begin
  { TODO: translate from asm/FUN_1ec2_0386.s — UNMATCHED until an oracle passes }
end;

