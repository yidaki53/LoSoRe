```c
#include <stdint.h>

uint16_t FUN_24dd_2e94(uint32_t stack_param) {
    uint8_t bVar1;
    uint16_t in_AX;
    uint8_t uVar3;
    uint32_t uVar2;
    int32_t iVar4;
    uint16_t uVar5;

    uVar5 = (uint16_t)(stack_param >> 16);
    iVar4 = (int32_t)stack_param;
    uVar2 = *(uint32_t *)(iVar4 - 1);
    uVar3 = (uint8_t)(uVar2 >> 8);
    bVar1 = (char)uVar2 - 0x34;
    if (bVar1 < 8) {
        *(int32_t *)(iVar4 - 2) = *(int32_t *)(iVar4 - 2) - 0x5c32;
    } else if (bVar1 < 9) {
        if ((uVar2 & 0x2000) == 0) {
            *(uint8_t *)(iVar4 - 2) = 0x9b;
            uVar2 = (uVar3 << 8) | uVar3;
            uVar2 &= 0x7c0;
            *(int32_t *)(iVar4 - 1) = (((char)(uVar2 >> 8) << 8) | (uVar2 >> 3)) ^ 0x18 + 0xd826;
        }
    } else if (bVar1 < 10) {
        *(uint16_t *)(iVar4 - 2) = 0x9b90;
    }
    return in_AX;
}
```