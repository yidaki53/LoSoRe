/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_3ce0
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=4 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>
#include <string.h>

extern uint16_t FUN_24dd_3d36(void);
extern uint16_t swi_21(void);

uint16_t __stdcall16far FUN_24dd_3ce0(int param_1, char *param_2) {
    char *pcVar1;
    char *pcVar5;
    uint8_t bVar3;
    int iVar4;
    uint16_t in_CX;
    char *unaff_SI;

    if (param_1 == 0) {
        bVar3 = swi_21();
        iVar4 = 0;
        if (2 < bVar3) {
            uint16_t unaff_ES = *(uint16_t *)0x2c;
            pcVar5 = (char *)0x0;
            while (*pcVar5 != '\0') {
                iVar4 = -1;
                while (iVar4 != 0) {
                    iVar4--;
                    pcVar1 = pcVar5;
                    pcVar5++;
                }
                pcVar5++;
            }
            unaff_SI = pcVar5 + 3;
            iVar4 = 0x100;
            pcVar5 = unaff_SI;
            while (iVar4 != 0) {
                iVar4--;
                pcVar1 = pcVar5;
                pcVar5++;
            }
            in_CX = 0;
            iVar4 = ((uint16_t)(iVar4 >> 8) << 8) | (uint16_t)~(uint8_t)iVar4;
        }
    } else {
        iVar4 = FUN_24dd_3d36();
    }

    pcVar5 = param_2;
    *param_2 = (char)iVar4;
    while (iVar4 != 0) {
        *pcVar5 = *unaff_SI;
        pcVar5++;
        unaff_SI++;
        iVar4--;
    }

    return in_CX;
}
