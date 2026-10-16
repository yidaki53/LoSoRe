/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1000_a816
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = lenient
 * Dual-judge: qwen=4 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>
#include <string.h>

// External function declarations
extern void FUN_24dd_0530(void);
extern char FUN_202c_0843(uint16_t, uint16_t);
extern void FUN_24dd_3639(uint16_t, uint16_t, uint8_t *, uint16_t);
extern void FUN_24dd_36b7(uint16_t, uint8_t *);
extern void FUN_24dd_04f4(void);
extern void FUN_24dd_3988(uint8_t, uint8_t *, uint16_t);
extern void FUN_24dd_38f0(uint8_t *, uint16_t);
extern uint16_t FUN_24dd_4654(uint16_t);
extern void FUN_24dd_3711(uint8_t *, uint16_t);

void FUN_1000_a816(uint8_t param_1) {
    char cVar1;
    uint16_t uVar2;
    uint8_t local_206[256];
    uint8_t local_106[256];
    uint16_t local_6 = 0xa821;
    int local_4 = 0x1000;

    FUN_24dd_0530();
    cVar1 = FUN_202c_0843(0xa80c, 0x24dd);
    if (cVar1 != '\0') {
        FUN_24dd_3639(0xa80c, 0x202c, local_106, 0);
        FUN_24dd_36b7(0x24dd, local_106);
        FUN_24dd_04f4();
        local_4 = -1;
        do {
            FUN_24dd_3988(0xff, local_206, 0);
            FUN_24dd_38f0(local_106, 0);
            FUN_24dd_04f4();
            local_4++;
        } while (local_206[0] != '\0');
        if (-1 < local_4) {
            FUN_24dd_36b7(0x24dd, local_106);
            FUN_24dd_04f4();
            uVar2 = FUN_24dd_4654(local_4);
            if (uVar2 < 0x8000) {
                local_6 = 0;
                while (true) {
                    FUN_24dd_3988(0x14, (uint16_t)param_1 * 0x15 + 0x66ec, 0);
                    FUN_24dd_38f0(local_106, 0);
                    FUN_24dd_04f4();
                    if (local_6 == uVar2) break;
                    local_6++;
                }
            }
        }
        FUN_24dd_3711(local_106, 0);
        FUN_24dd_04f4();
    }
}
