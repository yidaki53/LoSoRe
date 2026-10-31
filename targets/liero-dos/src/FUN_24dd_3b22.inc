{ liero-dos::FUN_24dd_3b22 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_3b22.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_3b22.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: recon:real decompiler C (unmatched) ---
// #include <stdint.h>
// 
// void FUN_24dd_3b22(uint8_t *param_1, uint16_t *param_2) {
//     uint8_t *pbVar6 = (uint8_t *)(param_2 + 1);
//     *param_2 = 0;
//     pbVar6[0] = 0xb0;
//     pbVar6[1] = 0xd7;
//     
//     for (int iVar3 = 0x16; iVar3 != 0; iVar3--) {
//         pbVar6[0] = 0;
//         pbVar6[1] = 0;
//         pbVar6 += 2;
//     }
//     
//     uint8_t *pbVar5 = param_1 + 1;
//     uint32_t uVar4 = (uint32_t)*param_1;
//     
//     if (0x4e < *param_1) {
//         for (uVar4 = (uint32_t)*param_1; uVar4 != 0; uVar4--) {
//             uint8_t *pbVar1 = pbVar5;
//             pbVar5++;
//             if (*pbVar1 == 0) break;
//             *pbVar6++ = *pbVar1;
//         }
//     }
//     
//     *pbVar6 = 0;
// }
// --- end reference ---
procedure FUN_24dd_3b22(param_1, param_2: Pointer);
begin
  { TODO: translate from asm/FUN_24dd_3b22.s — UNMATCHED until an oracle passes }
end;

