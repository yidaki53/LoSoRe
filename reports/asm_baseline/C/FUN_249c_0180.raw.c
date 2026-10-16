```c
#include <stdint.h>

typedef uint16_t (*code)(void);

uint16_t __cdecl16far FUN_249c_0180(void) {
    code func = (code)0x21;
    uint16_t result = func();
    uint16_t uVar3 = result & 0xff00;
    if ((int8_t)result == -1) {
        uVar3 += 1;
    }
    return uVar3;
}
```