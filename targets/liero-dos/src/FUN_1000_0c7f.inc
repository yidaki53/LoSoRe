{ liero-dos::FUN_1000_0c7f — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_0c7f.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_0c7f.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: recon:real decompiler C (unmatched) ---
// #include <stdint.h>
// 
// extern uint8_t FUN_24dd_0530(void);
// extern uint8_t FUN_24dd_4161(void);
// 
// uint8_t FUN_1000_0c7f(int param_1, int param_2, int param_3, int param_4, int param_5, int param_6) {
//     uint8_t local_3 = 1;
//     uint32_t uVar4;
//     int iVar2, iVar3, iVar5;
//     uint8_t bVar1;
// 
//     FUN_24dd_0530();
// 
//     uVar4 = (param_4 - param_6) >> 0xF;
//     if (((((int)((param_4 - param_6) ^ uVar4) - uVar4) < 0xA1) &&
//          (uVar4 = (param_3 - param_5) >> 0xF, (int)((param_3 - param_5) ^ uVar4) - uVar4 < 0xA1)) ||
//         ((uVar4 = (param_2 - param_6) >> 0xF, (int)((param_2 - param_6) ^ uVar4) - uVar4 < 0xA1 &&
//          (uVar4 = (param_1 - param_5) >> 0xF, (int)((param_1 - param_5) ^ uVar4) - uVar4 < 0xA1)))) {
//         local_3 = 0;
//     } else {
//         for (iVar2 = param_6 - 3; iVar2 <= param_6 + 3; iVar2++) {
//             for (iVar3 = param_5 - 4; iVar3 <= param_5 + 4; iVar3++) {
//                 iVar5 = 0x20;
//                 bVar1 = FUN_24dd_4161();
//                 if ((*(uint8_t *)(iVar5 + 0x14A0) & bVar1) != 0) {
//                     return 0;
//                 }
//             }
//         }
//     }
//     return local_3;
// }
// --- end reference ---
function FUN_1000_0c7f(param_1, param_2, param_3, param_4, param_5, param_6: Integer): Byte;
begin
  { TODO: translate from asm/FUN_1000_0c7f.s — UNMATCHED until an oracle passes }
end;

