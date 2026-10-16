/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_202c_08b2
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=4 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>
#include <stdbool.h>

extern void FUN_24dd_3eaf(uint8_t, uint16_t, uint16_t, uint8_t*, uint16_t);
extern void FUN_24dd_3e95(uint8_t*, uint16_t);
extern void FUN_24dd_3f14(uint16_t, uint16_t);
extern void FUN_202c_079e(uint8_t, uint8_t, uint16_t, uint16_t, uint8_t*, uint16_t);

void __stdcall16far FUN_202c_08b2(uint8_t *param_1) {
    uint8_t *pbVar4 = param_1;
    uint8_t local_102 = *param_1;
    uint8_t abStack_101[255];
    uint8_t local_382[640];
    uint8_t *pbVar2 = abStack_101;
    uint32_t uVar3 = local_102;

    for (; uVar3 != 0; uVar3--) {
        *pbVar2++ = *pbVar4++;
    }

    FUN_24dd_3eaf(8, 0x6664, 0, &local_102, 0);
    FUN_24dd_3e95(&local_102, 0);
    FUN_24dd_3f14(0x8ad, 0x24dd);
    FUN_202c_079e(0x9b, 0, 0x669c, 0, local_382, 0);

    *(bool *)0x666e = *(char *)0x66ec == '\0';
    *(bool *)0x666f = *(char *)0x6701 == '\0';
}
