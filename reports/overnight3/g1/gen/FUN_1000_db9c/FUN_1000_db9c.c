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

void FUN_1000_db9c(void) {
    char cVar1;
    uint16_t local_294[9];
    uint8_t local_28b[256];
    int local_18b;
    int local_189;
    int local_187;
    uint8_t local_183[80];
    uint8_t local_133[49];
    uint8_t local_102[252];

    FUN_24dd_0530();
    FUN_24dd_46e9();
    FUN_24dd_3d68(0x9b, 0x669c, 0x1500, 0x1000);
    cVar1 = FUN_202c_0843(0xdb82, 0x24dd);
    if (cVar1 == '\0') {
        FUN_24dd_3eaf(8, 0x6664, 0x1000, 0xdb8c, 0x202c);
    } else {
        FUN_24dd_3639(0xdb82, 0x202c, local_28b, 0x1000);
        FUN_24dd_36b7(0x24dd, local_28b);
        FUN_24dd_04f4();
        FUN_24dd_3988(8, local_294, 0x1000);
        FUN_24dd_38f0(local_28b, 0x1000);
        FUN_24dd_04f4();
        FUN_24dd_3711(local_28b, 0x1000);
        FUN_24dd_04f4();
        if (*(char *)0x6664 == '\0') {
            FUN_24dd_3eaf(8, 0x6664, 0x1000, 0xdb8c, 0x24dd);
        }
    }
    FUN_202c_08b2(0x6664, 0x1000);
    FUN_24dd_3eaf(0xc, 0x65f2, 0x1000, 0x672e, 0x1000);
    if (*(char *)0x66ec == '\0') {
        FUN_1000_a816(0);
    }
    if (*(char *)0x6701 == '\0') {
        FUN_1000_a816(1);
    }
    FUN_202c_079e(0x6c00, 10, (int)*(uint32_t *)0x6678, (int)((*(uint32_t *)0x6678) >> 16), 0xdb92, 0x24dd);
    FUN_202c_079e(0x18e2, 0x6e0e, (int)*(uint32_t *)0x667c, (int)((*(uint32_t *)0x667c) >> 16), 0xdb92, 0x202c);
    FUN_202c_079e(0x1c0, 0x86f4, (int)*(uint32_t *)0x6680, (int)((*(uint32_t *)0x6680) >> 16), 0xdb92, 0x202c);
    local_187 = 0;
    while (true) {
        local_189 = 0;
        while (true) {
            for (local_18b = 0; local_18b != 0xf; local_18b++) {
                local_102[local_18b * 0x10 + local_189] = *(uint8_t *)(
                    (int)*(uint32_t *)0x6678 + local_187 * 0x100 + local_189 * 0x10 + local_18b);
            }
            if (local_189