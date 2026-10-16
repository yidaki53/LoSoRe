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

void FUN_24dd_46f6(void);

void __stdcall16far FUN_24dd_47d9(int param_1, uint8_t *param_2, int param_3) {
    uint8_t *puVar1;
    int in_CX;
    uint8_t *puVar2;
    uint8_t *puVar3;
    uint16_t uVar4;

    FUN_24dd_46f6();
    uVar4 = (uint16_t)((uintptr_t)param_2 >> 16);
    if (param_1 < param_3) {
        param_3 = param_1;
    }
    if (param_1 < in_CX) {
        in_CX = param_1;
    }
    if (param_3 < in_CX) {
        param_3 = in_CX;
    }
    puVar3 = param_2 + 1;
    *param_2 = (uint8_t)param_3;
    param_3 = param_3 - in_CX;
    puVar2 = (uint8_t *)0xfffe;
    if (param_3 != 0) {
        for (; puVar2 = (uint8_t *)0xfffe, param_3 != 0; param_3 = param_3 + -1) {
            puVar1 = puVar3;
            puVar3 = puVar3 + 1;
            *puVar1 = 0x20;
        }
    }
    for (; in_CX != 0; in_CX = in_CX + -1) {
        puVar1 = puVar3;
        puVar3 = puVar3 + 1;
        *puVar1 = *puVar2;
        puVar2 = puVar2 + 1;
    }
    return;
}