/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_0116
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=4 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern void FUN_24dd_3711(uint16_t, uint16_t);
extern void FUN_24dd_01f0(void);
extern void FUN_24dd_01fe(void);
extern void FUN_24dd_0218(void);
extern void FUN_24dd_0232(void);

void __cdecl16far FUN_24dd_0116(void) {
    uint16_t in_AX;
    uint16_t *DAT_2971_6406 = (uint16_t *)0x2971;
    uint16_t *DAT_2971_6408 = (uint16_t *)(0x2971 + 2);
    uint16_t *DAT_2971_640a = (uint16_t *)(0x2971 + 4);
    char **_DAT_2971_6402 = (char **)(0x2971 + 8);
    uint16_t *DAT_2971_6410 = (uint16_t *)(0x2971 + 10);

    *DAT_2971_6406 = in_AX;
    *DAT_2971_6408 = 0;
    *DAT_2971_640a = 0;

    char *pcVar3 = *_DAT_2971_6402;
    if ((int)((uint32_t)*_DAT_2971_6402 >> 0x10) == 0 && pcVar3 == NULL) {
        *DAT_2971_6408 = 0;
        FUN_24dd_3711(0x78f0, 0x2971);
        FUN_24dd_3711(0x79f0, 0x2971);

        for (int iVar2 = 0x13; iVar2 != 0; iVar2--) {
            // Simulate interrupt call
            asm("int 0x21");
        }

        if (*DAT_2971_6408 != 0 || *DAT_2971_640a != 0) {
            FUN_24dd_01f0();
            FUN_24dd_01fe();
            FUN_24dd_01f0();
            FUN_24dd_0218();
            FUN_24dd_0232();
            FUN_24dd_0218();
            pcVar3 = (char *)0x260;
            FUN_24dd_01f0();
        }

        // Simulate interrupt call
        asm("int 0x21");

        while (*pcVar3 != '\0') {
            FUN_24dd_0232();
            pcVar3++;
        }
    } else {
        *_DAT_2971_6402 = NULL;
        *DAT_2971_6410 = 0;
    }
}
