/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_202c_14b6
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern uint16_t FUN_24dd_4654(uint16_t);
extern uint16_t CARRY2(int, uint16_t);

void FUN_202c_14b6(uint16_t param_1, int16_t param_2, uint16_t param_3, int16_t param_4,
                  uint16_t param_5, uint16_t param_6, int16_t param_7, uint8_t param_8) {
    uint16_t *base_address = (uint16_t *)0x6694;
    uint16_t *data_ptr;
    uint16_t uVar1, uVar4;
    uint8_t bVar2;
    uint16_t uVar6;
    int16_t iVar5;
    uint16_t local_4 = 0;

    // Find the first empty slot in the data structure
    while (*(char *)(*(uint16_t *)base_address + local_4 * 0x14 + 0x12) != '\0' && (local_4 < 600)) {
        local_4++;
    }

    bVar2 = param_8 & 0x7f;
    data_ptr = (uint16_t *)(*(uint16_t *)base_address + local_4 * 0x14);

    // Update the data structure with input parameters
    *(data_ptr + 0x6) = param_6;
    *(data_ptr + 0x3) = param_5;
    *(data_ptr + 0x12) = param_8;

    // Perform arithmetic operations and update the data structure
    uVar4 = FUN_24dd_4654(*(uint16_t *)((uint)bVar2 * 2 + 0x56c) << 1);
    uVar1 = *(uint16_t *)((uint)bVar2 * 2 + 0x56c);
    *(data_ptr + 4) = (param_3 - uVar1) + uVar4;
    *(data_ptr + 5) = ((param_4 - (int16_t)(uVar1 >> 0xf)) - (uint16_t)(param_3 < uVar1)) +
                      (uint16_t)CARRY2(param_3 - uVar1, uVar4);

    uVar4 = FUN_24dd_4654(*(uint16_t *)((uint)bVar2 * 2 + 0x56c) << 1);
    uVar1 = *(uint16_t *)((uint)bVar2 * 2 + 0x56c);
    *(data_ptr + 6) = (param_1 - uVar1) + uVar4;
    *(data_ptr + 7) = ((param_2 - (int16_t)(uVar1 >> 0xf)) - (uint16_t)(param_1 < uVar1)) +
                      (uint16_t)CARRY2(param_1 - uVar1, uVar4);

    // Conditional logic based on input parameters
    if (*(char *)(bVar2 + 0x645) == '\0') {
        if (param_7 < 1) {
            *(data_ptr + 0x9) = *(uint8_t *)(bVar2 + 0x68d);
        } else {
            *(data_ptr + 0x9) = (uint8_t)param_7;
        }
    } else {
        uint8_t uVar3 = FUN_24dd_4654(*(uint8_t *)(bVar2 + 0x65d) + 1);
        *(data_ptr + 0x9) = uVar3;
    }

    // Final arithmetic operation and update
    iVar5 = FUN_24dd_4654(*(uint16_t *)((uint)bVar2 * 2 + 0x7c4));
    *(data_ptr + 8) = *(uint16_t *)((uint)bVar2 * 2 + 0x794) - iVar5;
}
