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

void FUN_24dd_3eaf(uint16_t, uint16_t, uint16_t, uint8_t *, uint16_t);
void FUN_24dd_3e95(uint8_t *, uint16_t);
void FUN_24dd_3f14(uint16_t, uint16_t);
void FUN_202c_079e(uint8_t, uint8_t, uint16_t, uint16_t, uint8_t *, uint16_t);

void __stdcall16far FUN_202c_08b2(uint8_t *param_1) {
    uint8_t local_382[640];
    uint8_t local_102 = *param_1;
    uint8_t abStack_101[255];
    uint8_t *pbVar1;
    uint8_t *pbVar2 = abStack_101;
    uint32_t uVar3 = local_102;

    while (uVar3 != 0) {
        pbVar1 = pbVar2;
        pbVar2 = pbVar2 + 1;
        *pbVar1 = *param_1;
        param_1 = param_1 + 1;
        uVar3 = uVar3 - 1;
    }

    FUN_24dd_3eaf(8, 0x6664, (uint16_t)param_1, &local_102, (uint16_t)abStack_101);
    FUN_24dd_3e95(&local_102, (uint16_t)abStack_101);
    FUN_24dd_3f14(0x8ad, 0x24dd);
    FUN_202c_079e(0x9b, 0, 0x669c, (uint16_t)local_382, (uint16_t)abStack_101);
    *(uint8_t *)0x666e = *(uint8_t *)0x66ec == '\0';
    *(uint8_t *)0x666f = *(uint8_t *)0x6701 == '\0';
}