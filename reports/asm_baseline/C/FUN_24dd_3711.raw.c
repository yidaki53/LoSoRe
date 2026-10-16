```c
#include <stdint.h>

void FUN_24dd_374d(void);

void __stdcall16far FUN_24dd_3711(uint32_t param_1) {
    int iVar1;
    uint16_t uVar2;
    uint16_t ds = (uint16_t)(param_1 >> 16);
    
    uVar2 = ds;
    iVar1 = (int)param_1;
    if (*(int *)(iVar1 + 2) != -0x284f) {
        if (*(int *)(iVar1 + 2) != -0x284e) {
            *(uint16_t *)0x6410 = 0x67;
            return;
        }
        FUN_24dd_374d();
    }
    FUN_24dd_374d();
    *(uint16_t *)(iVar1 + 2) = 0xd7b0;
    return;
}
```