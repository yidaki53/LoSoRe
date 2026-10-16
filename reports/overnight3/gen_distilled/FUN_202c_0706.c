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

extern uint16_t FUN_24dd_4824(int *param1, uint16_t param2, uint8_t *param3, uint16_t param4);
extern void FUN_24dd_46e9();

uint16_t __stdcall16far FUN_202c_0706(uint8_t *param_1) {
    uint8_t *pbVar1;
    uint8_t *pbVar2;
    uint32_t uVar3;
    int local_10c;
    uint16_t local_10a;
    uint16_t local_108;
    uint8_t local_106;
    uint8_t abStack_105[259];

    pbVar2 = param_1;
    local_106 = *param_1;
    pbVar1 = abStack_105;
    for (uVar3 = (uint32_t)local_106; pbVar1 = pbVar1 + 1, pbVar2 = pbVar2 + 1, uVar3 != 0; uVar3 = uVar3 - 1) {
        *pbVar1 = *pbVar2;
    }

    local_108 = FUN_24dd_4824(&local_10c, 0, &local_106, 0);
    if (local_108 != 0) {
        return ((uint16_t)local_10c << 16) | local_10a;
    }

    FUN_24dd_46e9();
    if (local_108 != 0) {
        return ((uint16_t)local_10c << 16) | local_10a;
    }

    return ((uint16_t)local_10c << 16) | local_10a;
}