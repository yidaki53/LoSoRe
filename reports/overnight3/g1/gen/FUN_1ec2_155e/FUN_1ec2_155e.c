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

void FUN_2971_65df(uint16_t, uint8_t, uint8_t, uint8_t, uint8_t);

void __stdcall16far FUN_1ec2_155e(uint32_t param_1) {
    uint8_t local_3 = 0;
    while (true) {
        uint16_t uVar2 = (uint16_t)(param_1 >> 16);
        uint16_t iVar1 = (uint16_t)param_1;
        FUN_2971_65df(0x1ec2,
                      ((uint8_t)((uint32_t)local_3 * 3 >> 8) << 8) | *(uint8_t *)(iVar1 + (uint32_t)local_3 * 3 + 2),
                      ((uint8_t)((uint32_t)local_3 * 3 >> 8) << 8) | *(uint8_t *)(iVar1 + (uint32_t)local_3 * 3 + 1),
                      ((uint8_t)((uint32_t)local_3 * 3 >> 8) << 8) | *(uint8_t *)(iVar1 + (uint32_t)local_3 * 3),
                      local_3);
        if (local_3 == 0xff) break;
        local_3++;
    }
    return;
}