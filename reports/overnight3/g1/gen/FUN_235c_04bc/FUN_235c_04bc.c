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

void FUN_235c_04bc(uint16_t ds, uint16_t es, uint16_t ss, uint16_t sp, uint16_t bp, uint16_t si, uint16_t di, uint16_t ax, uint16_t bx, uint16_t cx, uint16_t dx, uint16_t ip, uint16_t cs, uint16_t flags, uint16_t *param_1) {
    uint8_t *pbVar1;
    uint8_t *pbVar2;
    uint32_t uVar3;
    uint8_t *pbVar4;
    uint8_t local_102;
    uint8_t abStack_101[255];

    pbVar4 = (uint8_t *)param_1;
    local_102 = *param_1;
    pbVar2 = abStack_101;
    for (uVar3 = (uint32_t)local_102; pbVar4 = pbVar4 + 1, uVar3 != 0; uVar3 = uVar3 - 1) {
        pbVar1 = pbVar2;
        pbVar2 = pbVar2 + 1;
        *pbVar1 = *pbVar4;
    }
    *(uint8_t *)(0x7690) = 1;
    FUN_24dd_3eaf(0xff, 0x7692, ds, &local_102, ss);
    return;
}