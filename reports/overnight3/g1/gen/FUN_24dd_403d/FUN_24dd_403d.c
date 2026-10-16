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

void FUN_24dd_3ed3(uint16_t, uint16_t, uint16_t, uint16_t);
void FUN_24dd_3f14(uint16_t*, uint16_t);
void FUN_24dd_3eaf(uint16_t, uint16_t, uint16_t, uint16_t*, uint16_t);

void __stdcall16far FUN_24dd_403d(int param_1, int param_2, uint32_t param_3) {
    uint16_t uVar1;
    uint16_t uVar2;
    uint16_t uVar5;
    uint8_t local_202[256];
    uint8_t local_102[256];

    if (((0 < param_1) && (0 < param_2)) && (param_2 < 0x100)) {
        if (0xff < param_1) {
            param_1 = 0xff;
        }
        uVar2 = (uint16_t)(param_3 >> 16);
        uVar1 = (uint16_t)param_3;
        uVar5 = _SS;
        FUN_24dd_3ed3(param_2 - 1, 1, uVar1, uVar2);
        FUN_24dd_3ed3(0xff, param_2 + param_1, uVar1, uVar2);
        FUN_24dd_3f14((uint16_t*)local_202, uVar5);
        FUN_24dd_3eaf(0xff, uVar1, uVar2, (uint16_t*)local_102, uVar5);
    }
    return;
}