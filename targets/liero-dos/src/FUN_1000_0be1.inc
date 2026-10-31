{ liero-dos::FUN_1000_0be1 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_0be1.s via skeleton(compile-gate); UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_0be1.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: recon:real decompiler C (unmatched) ---
// #include <stdint.h>
// 
// extern void FUN_24dd_0530(void);
// extern char FUN_24dd_4654(int);
// 
// void FUN_1000_0be1(uint16_t param_1, uint16_t param_2, uint16_t param_3, uint16_t param_4,
//                    uint16_t param_5, uint16_t param_6) {
//     char cVar1;
//     int iVar2;
//     uint16_t uVar3;
//     uint16_t *baseAddress = (uint16_t *)0x6690;
//     uint16_t local_4;
// 
//     FUN_24dd_0530();
//     for (local_4 = 0; (*(char *)(baseAddress[0] + local_4 * 0x11) != '\0') && (local_4 < 700); local_4++) {
//     }
// 
//     cVar1 = FUN_24dd_4654(2);
//     *(char *)(baseAddress[0] + local_4 * 0x11) = cVar1 + 'P';
//     *(uint16_t *)(baseAddress[0] + local_4 * 0x11 + 3) = param_6;
//     *(uint16_t *)(baseAddress[0] + local_4 * 0x11 + 7) = param_5;
//     uVar3 = baseAddress[0] >> 0x10;
//     iVar2 = baseAddress[0] + local_4 * 0x11;
//     *(uint16_t *)(iVar2 + 9) = param_3;
//     *(uint16_t *)(iVar2 + 0xb) = param_4;
//     uVar3 = baseAddress[0] >> 0x10;
//     iVar2 = baseAddress[0] + local_4 * 0x11;
//     *(uint16_t *)(iVar2 + 0xd) = param_1;
//     *(uint16_t *)(iVar2 + 0xf) = param_2;
// }
// --- end reference ---
procedure FUN_1000_0be1(param_1, param_2, param_3, param_4, param_5, param_6: Word);
begin
  { TODO: translate from asm/FUN_1000_0be1.s — UNMATCHED until an oracle passes }
end;

