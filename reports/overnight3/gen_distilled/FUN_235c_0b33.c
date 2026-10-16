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

extern uint16_t FUN_24dd_415f(uint16_t, uint16_t, uint16_t, uint16_t);
extern uint16_t FUN_24dd_4193(uint16_t, uint16_t, uint16_t, uint16_t);

uint16_t FUN_235c_0b33(uint16_t param_1, uint16_t param_2) {
    uint16_t uVar1;
    uint16_t uVar2;
    uint16_t uVar3;
    uint16_t uVar4;
    uint16_t uVar5;
    uint16_t uVar6;
    uint16_t uVar7;

    uVar7 = FUN_24dd_415f(param_1, param_2, 0, 0);
    uVar6 = FUN_24dd_415f(param_1, param_2, 0, 0);
    uVar3 = 0x10;
    uVar5 = 0;
    uVar1 = FUN_24dd_4193(uVar3, 0, uVar7, uVar6);
    uVar2 = FUN_24dd_4193(uVar3, 0, uVar7, uVar6);
    return ((uint16_t)(uVar1 >> 16) << 16) | uVar2;
}