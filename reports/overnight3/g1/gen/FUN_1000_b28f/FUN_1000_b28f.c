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

void FUN_24dd_0530(void);
void FUN_202c_076d(uint16_t, uint16_t);
void FUN_24dd_3f14(uint16_t, uint16_t);
void FUN_24dd_3eaf(uint16_t, uint16_t, uint16_t, uint16_t, uint16_t);

void FUN_1000_b28f(uint16_t param_1) {
    uint16_t local_103[253];
    uint16_t uStack_6 = 0xb29a;
    uint8_t local_3 = 0x10;

    FUN_24dd_0530();
    FUN_202c_076d(*(uint16_t *)((uint8_t)(param_1 + 6) * 2 + 0x66e8), 0);
    FUN_24dd_3f14(0xb28d, 0x202c);
    FUN_24dd_3eaf(0xc, param_1 - 0xa1, 0, (uint16_t)local_103, 0);

    FUN_202c_076d(*(uint16_t *)((uint8_t)(param_1 + 6) * 3 + 0x66d8), 0);
    FUN_24dd_3eaf(0xc, param_1 - 0x94, 0, (uint16_t)local_103, 0);

    FUN_202c_076d(*(uint16_t *)((uint8_t)(param_1 + 6) * 3 + 0x66d9), 0);
    FUN_24dd_3eaf(0xc, param_1 - 0x87, 0, (uint16_t)local_103, 0);

    FUN_202c_076d(*(uint16_t *)((uint8_t)(param_1 + 6) * 3 + 0x66da), 0);
    FUN_24dd_3eaf(0xc, param_1 - 0x7a, 0, (uint16_t)local_103, 0);

    local_3 = 0;
    while (true) {
        FUN_24dd_3eaf(0xc, param_1 + (local_3 + 5) * 0xd - 0xae, 0,
                      (uint16_t)(*(uint8_t *)((uint8_t)(param_1 + 6) * 7 + (uint8_t)local_3 + 0x6720) * 0xd + 0x5b19), 0);
        if (local_3 == 6) break;
        local_3++;
    }

    FUN_24dd_3eaf(0xc, param_1 - 0x12, 0, *(uint16_t *)(*(uint8_t *)(param_1 + 6) + 0x66a7) * 6 + 900, 0);
    return;
}