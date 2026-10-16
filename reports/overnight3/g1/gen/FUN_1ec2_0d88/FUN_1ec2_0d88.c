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

void __stdcall16far FUN_1ec2_0d88(uint8_t param_1, int param_2, int param_3, uint8_t *param_4) {
    uint8_t *puVar1;
    int iVar2;
    uint8_t *puVar3;
    uint16_t uVar4;

    uVar4 = (uint16_t)((uintptr_t)param_4 >> 16);
    param_2 = param_2 - 2;
    puVar3 = param_4;
    for (iVar2 = param_3 - 2; iVar2 != 0; iVar2--) {
        puVar3[1] = param_1;
        puVar3++;
    }
    puVar3 = puVar3 - param_3 + 0x142;
    iVar2 = param_3;
    do {
        for (; iVar2 != 0; iVar2--) {
            puVar1 = puVar3;
            puVar3++;
            *puVar1 = param_1;
        }
        puVar3 = puVar3 - param_3 + 0x140;
        param_2--;
        iVar2 = param_3;
    } while (param_2 != 0);
    for (param_3 = param_3 - 2; puVar3++; param_3--) {
        *puVar3 = param_1;
    }
    return;
}