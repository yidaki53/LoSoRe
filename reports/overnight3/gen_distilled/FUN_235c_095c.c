#include <stdint.h>
#include <stddef.h>
typedef unsigned char undefined1, byte, uchar;
typedef unsigned short undefined2, ushort, word;
typedef unsigned int undefined4;
typedef unsigned long undefined8;
typedef long long longlong;
typedef unsigned long long ulonglong;
typedef unsigned int uint;
typedef short int16;
#define __cdecl16near
#define __cdecl16far
#define __stdcall16near
#define __stdcall16far
#define __cdecl
#define __stdcall
#define __fastcall
#define __pascal
#define __near
#define __far
#define __interrupt
#define __declspec(x)
/* BSD/kernel types some models assume (not Ghidra, but harmless to accept) */
typedef unsigned char u_char;
typedef unsigned short u_short, u_int16;
typedef unsigned int u_int, u32, uint32;
typedef unsigned short uint16, ushort_t;
typedef unsigned char uint8;
#ifndef true
#define true 1
#define false 0
#endif

#include <stdint.h>

void FUN_235c_095c(uint16_t param_1, uint16_t param_2, uint8_t param_3, uint8_t param_4) {
    uint8_t local_4 = 0xff;
    uint8_t local_3 = 0;

    while (true) {
        if (*(char *)(0x67fc + local_3) == '\0') {
            local_4 = local_3;
            break;
        }
        local_3++;
    }

    if (local_3 == 0xff) {
        return;
    }

    uint16_t uVar5 = (uint16_t)(local_3 * 10);
    uint16_t uVar6 = (uint16_t)(local_4 * 10);

    *(uint16_t *)(0x6804 + uVar5) = param_1;
    *(uint16_t *)(0x6806 + uVar5) = param_2;
    *(uint8_t *)(0x6808 + uVar5) = param_3;
    *(uint16_t *)(0x6809 + uVar5) = 0;
    *(uint16_t *)(0x680b + uVar5) = 0;
    *(uint8_t *)(0x680d + uVar5) = param_4;
    *(uint16_t *)(0x67fc + local_3) = 1;
}