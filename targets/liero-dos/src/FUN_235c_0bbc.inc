{ liero-dos::FUN_235c_0bbc — game Pascal draft (oracle: none).
  Drafted from asm/FUN_235c_0bbc.s via skeleton(compile-gate); UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_235c_0bbc.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: recon:real decompiler C (unmatched) ---
// #include <stdint.h>
// 
// // Forward declarations of external functions
// extern uint32_t FUN_235c_091d(uint8_t);
// extern uint32_t FUN_24dd_028a(uint16_t);
// extern uint32_t FUN_235c_0aff(uint16_t, uint16_t);
// extern uint32_t FUN_24dd_3dbd(void);
// extern uint32_t FUN_235c_0b33(int, int);
// extern void FUN_24dd_4905(int16_t, uint16_t, int, int);
// extern void FUN_235c_0b7c(void);
// extern void FUN_235c_0aad(uint8_t);
// extern void FUN_235c_03a1(void);
// 
// void FUN_235c_0bbc(void) {
//     uint8_t uVar1;
//     uint32_t uVar2;
//     uint16_t uVar3;
//     int iVar4;
//     uint16_t local_4;
//     uint32_t uVar5;
// 
//     for (local_4 = 0; FUN_235c_091d(local_4 & 0xff), local_4 != 7; local_4 = local_4 + 1) {
//     }
// 
//     *(uint8_t *)0x67ce = 0;
//     if (*(char *)0x67cd == '\0') {
//         uVar5 = FUN_24dd_028a(0x800);
//         *(uint16_t *)0x6e58 = (int)uVar5;
//         *(uint16_t *)0x6e5a = (int)((uint32_t)uVar5 >> 0x10);
//         FUN_235c_0aff(*(uint16_t *)0x6e58, *(uint16_t *)0x6e5a);
//         uVar2 = 0;
//         iVar4 = 1;
//         FUN_24dd_3dbd();
//         if ((int)(iVar4 + (uint32_t)(0xfbff < uVar2)) < 1) {
//             uVar3 = *(uint16_t *)0x6e5a;
//             *(uint16_t *)0x6e5c = *(uint16_t *)0x6e58;
//             *(uint16_t *)0x6e5e = uVar3;
//         } else {
//             uVar5 = FUN_235c_0b33((int)*(uint32_t *)0x6e58 + 0x400,
//                                   (int)((uint32_t)*(uint32_t *)0x6e58 >> 0x10));
//             *(uint16_t *)0x6e5c = (int)uVar5;
//             *(uint16_t *)0x6e5e = (int)((uint32_t)uVar5 >> 0x10);
//         }
//         local_4 = 1;
//         while (true) {
//             uVar5 = FUN_235c_0b33((int)*(uint32_t *)0x6e5c + local_4 * 0x200 + -0x200,
//                                   (int)((uint32_t)*(uint32_t *)0x6e5c >> 0x10));
//             *(uint16_t *)(local_4 * 4 + 0x6e60) = (int)uVar5;
//             *(uint16_t *)(local_4 * 4 + 0x6e62) = (int)((uint32_t)uVar5 >> 0x10);
//             if (local_4 == 2) break;
//             local_4 = local_4 + 1;
//         }
//         uVar5 = FUN_235c_0aff(*(uint16_t *)0x6e5c, *(uint16_t *)0x6e5e);
//         *(uint16_t *)0x6e70 = (int)uVar5;
//         *(uint16_t *)0x6e72 = (int)((uint32_t)uVar5 >> 0x10);
//         uVar1 = FUN_24dd_3dbd();
//         *(uint8_t *)0x6e74 = uVar1;
//         uVar3 = 0;
//         FUN_24dd_3dbd();
//         *(uint16_t *)0x6e76 = uVar3;
//         local_4 = 1;
//         while (true) {
//             uVar5 = FUN_235c_0aff(*(uint16_t *)(local_4 * 4 + 0x6e60),
//                                   *(uint16_t *)(local_4 * 4 + 0x6e62));
//             *(uint16_t *)(local_4 * 4 + 0x6e74) = (int)uVar5;
//             *(uint16_t *)(local_4 * 4 + 0x6e76) = (int)((uint32_t)uVar5 >> 0x10);
//             if (local_4 == 2) break;
//             local_4 = local_4 + 1;
//         }
//         local_4 = 1;
//         while (true) {
//             uVar1 = FUN_24dd_3dbd();
//             *(uint8_t *)(local_4 + 0x6e7f) = uVar1;
//             if (local_4 == 2) break;
//             local_4 = local_4 + 1;
//         }
//         local_4 = 1;
//         while (true) {
//             uVar3 = 0;
//             FUN_24dd_3dbd();
//             *(uint16_t *)(local_4 * 2 + 0x6e80) = uVar3;
//             if (local_4 == 2) break;
//             local_4 = local_4 + 1;
//         }
//         FUN_24dd_4905(0xff80, 0x400, (int)*(uint32_t *)0x6e5c,
//                       (int)((uint32_t)*(uint32_t *)0x6e5c >> 0x10));
//         FUN_235c_0b7c();
//     } else {
//         uVar5 = FUN_24dd_028a(0x1000);
//         *(uint16_t *)0x6e58 = (int)uVar5;
//         *(uint16_t *)0x6e5a = (int)((uint32_t)uVar5 >> 0x10);
//         FUN_235c_0aff(*(uint16_t *)0x6e58, *(uint16_t *)0x6e5a);
//         FUN_24dd_3dbd();
//         uVar2 = 0;
//         iVar4 = 1;
//         FUN_24dd_3dbd();
//         if ((int)(iVar4 + (uint32_t)(0xfbff < uVar2)) < 1) {
//             uVar3 = *(uint16_t *)0x6e5a;
//             *(uint16_t *)0x6e60 = *(uint16_t *)0x6e58;
//             *(uint16_t *)0x6e62 = uVar3;
//         } else {
//             uVar5 = FUN_235c_0b33((int)*(uint32_t *)0x6e58 + 0x800,
//                                   (int)((uint32_t)*(uint32_t *)0x6e58 >> 0x10));
//             *(uint16_t *)0x6e60 = (int)uVar5;
//             *(uint16_t *)0x6e62 = (int)((uint32_t)uVar5 >> 0x10);
//         }
//         local_4 = 1;
//         while (true) {
//             uVar5 = FUN_235c_0b33((int)*(uint32_t *)0x6e60 + local_4 * 0x400 + -0x400,
//                                   (int)((uint32_t)*(uint32_t *)0x6e60 >> 0x10));
//             *(uint16_t *)(local_4 * 4 + 0x6e60) = (int)uVar5;
//             *(uint16_t *)(local_4 * 4 + 0x6e62) = (int)((uint32_t)uVar5 >> 0x10);
//             if (local_4 == 2) break;
//             local_4 = local_4 + 1;
//         }
//         uVar5 = FUN_235c_0aff(*(uint16_t *)0x6e60, *(uint16_t *)0x6e62);
//         *(uint16_t *)0x6e70 = (int)uVar5;
//         *(uint16_t *)0x6e72 = (int)((uint32_t)uVar5 >> 0x10);
//         uVar1 = FUN_24dd_3dbd();
//         *(uint8_t *)0x6e74 = uVar1;
//         FUN_24dd_3dbd();
//         uVar3 = 0;
//         FUN_24dd_3dbd();
//         *(uint16_t *)0x6e76 = uVar3;
//         local_4 = 1;
//         while (true) {
//             uVar5 = FUN_235c_0aff(*(uint16_t *)(local_4 * 4 + 0x6e60),
//                                   *(uint16_t *)(local_4 * 4 + 0x6e62));
//             *(uint16_t *)(local_4 * 4 + 0x6e74) = (int)uVar5;
//             *(uint16_t *)(local_4 * 4 + 0x6e76) = (int)((uint32_t)uVar5 >> 0x10);
//             if (local_4 == 2) break;
//             local_4 = local_4 + 1;
//         }
//         local_4 = 1;
//         while (true) {
//             uVar1 = FUN_24dd_3dbd();
//             *(uint8_t *)(local_4 + 0x6e7f) = uVar1;
//             if (local_4 == 2) break;
//             local_4 = local_4 + 1;
//         }
//         local_4 = 1;
//         while (true) {
//             FUN_24dd_3dbd();
//             uVar3 = 0;
//             FUN_24dd_3dbd();
//             *(uint16_t *)(local_4 * 2 + 0x6e80) = uVar3;
//             if (local_4 == 2) break;
//             local_4 = local_4 + 1;
//         }
//         FUN_24dd_4905(0, 0x800, (int)*(uint32_t *)0x6e60,
//                       (int)((uint32_t)*(uint32_t *)0x6e60 >> 0x10));
//     }
//     FUN_24dd_4905(0, 0x400, 0x6a58, *(uint16_t *)0x67c0);
//     FUN_235c_0aad(1);
//     *(uint16_t *)0x67c2 = 0;
//     *(uint16_t *)0x67c4 = 0;
//     FUN_235c_03a1();
// }
// --- end reference ---
procedure FUN_235c_0bbc;
begin
  { TODO: translate from asm/FUN_235c_0bbc.s — UNMATCHED until an oracle passes }
end;

