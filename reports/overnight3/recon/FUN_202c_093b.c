/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_202c_093b
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = lenient
 * Dual-judge: qwen=5 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

// External function declarations
extern void FUN_24dd_3eaf(uint8_t, uint16_t*, uint16_t, uint16_t, uint16_t);
extern void FUN_24dd_3e95(uint16_t, uint16_t);
extern void FUN_24dd_3639(uint8_t*, uint16_t, uint8_t*, uint16_t);
extern void FUN_24dd_36bc(uint16_t, uint8_t*);
extern void FUN_24dd_04f4(void);
extern void FUN_24dd_3711(uint8_t*, uint16_t);
extern void FUN_24dd_39c3(uint16_t, uint16_t*, uint16_t);
extern void FUN_24dd_3930(uint8_t*, uint16_t);
extern void FUN_24dd_3f14(uint16_t, uint16_t);
extern void FUN_24dd_3b22(uint8_t*, uint16_t, uint8_t*, uint16_t);
extern void FUN_24dd_3b66(uint8_t, uint8_t*, uint16_t);
extern void FUN_24dd_3c4f(uint16_t, uint16_t, uint16_t, uint16_t, uint16_t, uint8_t*, uint16_t);
extern void FUN_24dd_3bde(uint8_t*, uint16_t);

void __stdcall16far FUN_202c_093b(uint8_t *param_1) {
    uint8_t *pbVar4 = param_1;
    uint8_t local_102 = *param_1;
    uint8_t abStack_101[255];
    uint8_t local_382[246];
    uint8_t local_28c[10];
    uint8_t local_282[256];
    uint8_t local_182[128];
    uint8_t *pbVar2 = abStack_101;
    uint8_t *pbVar1;
    uint32_t uVar3;

    for (uVar3 = (uint32_t)local_102; uVar3 != 0; uVar3--) {
        *pbVar2++ = *pbVar4++;
    }

    if (*(char *)0x666e != '\0') {
        *(uint8_t *)0x66ec = 0;
    }
    if (*(char *)0x666f != '\0') {
        *(uint8_t *)0x6701 = 0;
    }

    if (local_102 == 0) {
        FUN_24dd_3eaf(0xff, (uint16_t *)&local_102, 0, 0x926, 0x202c);
        FUN_24dd_3e95(0x92c, 0x24dd);
        FUN_24dd_3639(local_28c, 0, local_282, 0);
        FUN_24dd_36bc(0x24dd, local_282);
        FUN_24dd_04f4();
        if (*(char *)0x6664 == '\0') {
            FUN_24dd_3eaf(8, (uint16_t *)0x6664, 0, 0x926, 0x24dd);
        }
        FUN_24dd_39c3(0, (uint16_t *)0x6664, 0);
        FUN_24dd_3930(local_282, 0);
        FUN_24dd_04f4();
        FUN_24dd_3711(local_282, 0);
        FUN_24dd_04f4();
    }

    FUN_24dd_3eaf(8, (uint16_t *)0x6664, 0, &local_102, 0);
    FUN_24dd_3e95(&local_102, 0);
    FUN_24dd_3f14(0x936, 0x24dd);
    FUN_24dd_3b22(local_382, 0, local_182, 0);
    FUN_24dd_3b66(1, local_182, 0);
    FUN_24dd_04f4();
    FUN_24dd_3c4f(0, 0, 0x9b, 0x669c, 0, local_182, 0);
    FUN_24dd_04f4();
    FUN_24dd_3bde(local_182, 0);
    FUN_24dd_04f4();
}
