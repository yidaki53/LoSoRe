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

void FUN_24dd_48cf(uint16_t, uint16_t, uint8_t, uint16_t);

void __stdcall16far FUN_235c_04bc(uint16_t param_1, uint8_t *param_2) {
    uint8_t *pbVar1;
    uint32_t uVar2;
    uint8_t *pbVar3;
    uint8_t local_102;
    uint8_t abStack_101[255];

    pbVar3 = param_2;
    local_102 = *param_2;
    pbVar1 = abStack_101;
    for (uVar2 = (uint32_t)local_102; pbVar3 = pbVar3 + 1, uVar2 != 0; uVar2 = uVar2 - 1) {
        pbVar1 = pbVar1 + 1;
        *pbVar1 = *pbVar3;
    }

    *(uint8_t *)0x7690 = 1;
    FUN_24dd_48cf(0x7692, 0, local_102, 0xff);
}