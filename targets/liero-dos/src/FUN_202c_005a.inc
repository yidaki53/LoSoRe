{ liero-dos::FUN_202c_005a — game Pascal draft (oracle: none).
  Drafted from asm/FUN_202c_005a.s via skeleton(compile-gate); UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_202c_005a.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: recon:real decompiler C (unmatched) ---
// #include <stdint.h>
// 
// extern uint8_t FUN_24dd_4161(void);
// extern uint32_t* DAT_6674;
// 
// void FUN_202c_005a(char param_1, uint32_t param_2, uint32_t param_3, int param_4, int param_5) {
//     char cVar1;
//     uint32_t uVar2;
//     uint8_t bVar3;
//     uint32_t uVar4;
//     uint32_t uVar5;
//     int iVar6;
//     uint16_t uVar7;
//     uint16_t uVar8;
//     int local_a;
//     int local_8;
// 
//     uVar7 = (uint16_t)(param_3 >> 0x10);
//     uVar8 = (uint16_t)(param_2 >> 0x10);
// 
//     if (param_1 == '\0') {
//         for (local_a = 0; (uVar4 = local_a + param_4) < 0x15d; local_a++) {
//             if (uVar4 < 0x8000) {
//                 local_8 = 0;
//                 while (true) {
//                     uVar5 = local_8 + param_5;
//                     if (uVar5 < 0x8000 && uVar5 < 0x1f8) {
//                         cVar1 = *(char *)((int)param_3 + local_a * 0x10 + local_8);
//                         if (cVar1 == '\n' || cVar1 == '\x06') {
//                             iVar6 = 0x20;
//                             bVar3 = FUN_24dd_4161();
//                             if ((*(uint8_t *)(iVar6 + 0x14c0) & bVar3) != 0) {
//                                 uVar2 = *(uint32_t *)(*(uint32_t *)DAT_6674 + uVar4 * 4);
//                                 *(uint8_t *)((int)uVar2 + uVar5) =
//                                     *(uint8_t *)((int)param_2 + (uVar4 & 0xf) * 0x10 + (uVar5 & 0xf));
//                             }
//                         } else if (cVar1 == '\x02') {
//                             iVar6 = 0x20;
//                             bVar3 = FUN_24dd_4161();
//                             if ((*(uint8_t *)(iVar6 + 0x14c0) & bVar3) != 0) {
//                                 uVar2 = *(uint32_t *)(*(uint32_t *)DAT_6674 + uVar4 * 4);
//                                 *(uint8_t *)((int)uVar2 + uVar5) = 2;
//                             }
//                         } else if (cVar1 == '\x01') {
//                             iVar6 = 0x20;
//                             bVar3 = FUN_24dd_4161();
//                             if ((*(uint8_t *)(iVar6 + 0x14c0) & bVar3) != 0) {
//                                 uVar2 = *(uint32_t *)(*(uint32_t *)DAT_6674 + uVar4 * 4);
//                                 *(uint8_t *)((int)uVar2 + uVar5) = 1;
//                             }
//                         }
//                     }
//                     if (local_8 == 0xf) break;
//                     local_8++;
//                 }
//             }
//             if (local_a == 0xf) {
//                 return;
//             }
//         }
//     } else {
//         for (local_a = 0; (uVar4 = local_a + param_4) < 0x15d; local_a++) {
//             if (uVar4 < 0x8000) {
//                 local_8 = 0;
//                 while (true) {
//                     uVar5 = local_8 + param_5;
//                     if (uVar5 < 0x8000 && uVar5 < 0x1f8) {
//                         cVar1 = *(char *)((int)param_3 + local_a * 0x10 + local_8);
//                         if (cVar1 == '\x06') {
//                             iVar6 = 0x20;
//                             bVar3 = FUN_24dd_4161();
//                             if ((*(uint8_t *)(iVar6 + 0x6624) & bVar3) != 0) {
//                                 uVar2 = *(uint32_t *)(*(uint32_t *)DAT_6674 + uVar4 * 4);
//                                 *(uint8_t *)((int)uVar2 + uVar5) =
//                                     *(uint8_t *)((int)param_2 + (uVar4 & 0xf) * 0x10 + (uVar5 & 0xf));
//                             }
//                         } else if (cVar1 == '\x01') {
//                             iVar6 = 0x20;
//                             bVar3 = FUN_24dd_4161();
//                             if ((*(uint8_t *)(iVar6 + 0x1460) & bVar3) != 0) {
//                                 uVar2 = *(uint32_t *)(*(uint32_t *)DAT_6674 + uVar4 * 4);
//                                 *(uint8_t *)((int)uVar2 + uVar5) = 1;
//                             }
//                             iVar6 = 0x20;
//                             bVar3 = FUN_24dd_4161();
//                             if ((*(uint8_t *)(iVar6 + 0x1480) & bVar3) != 0) {
//                                 uVar2 = *(uint32_t *)(*(uint32_t *)DAT_6674 + uVar4 * 4);
//                                 *(uint8_t *)((int)uVar2 + uVar5) = 2;
//                             }
//                         }
//                     }
//                     if (local_8 == 0xf) break;
//                     local_8++;
//                 }
//             }
//             if (local_a == 0xf) {
//                 return;
//             }
//         }
//     }
// }
// --- end reference ---
procedure FUN_202c_005a(param_1: Char; param_2, param_3: Longint; param_4, param_5: Integer);
begin
  { TODO: translate from asm/FUN_202c_005a.s — UNMATCHED until an oracle passes }
end;

