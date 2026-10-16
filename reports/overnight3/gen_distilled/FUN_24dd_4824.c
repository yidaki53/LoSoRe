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

void FUN_24dd_4732(void);

void __stdcall16far FUN_24dd_4824(uint16_t param_1) {
    uint16_t uVar1;
    uint16_t *puVar2;
    uint16_t uVar3;
    uint16_t uVar4;

    uVar4 = (uint16_t)((uint16_t)param_1 >> 16);
    puVar2 = (uint16_t *)((int16_t)param_1 + 2);
    uVar3 = (uint16_t)((uint16_t)param_1 >> 16);

    while (*puVar2 != 0x20) {
        puVar2++;
        uVar1 = (uint16_t)((uint16_t)param_1 >> 16);
    }

    uVar1 = (uint16_t)((uint16_t)param_1 >> 16);
    do {
        uVar4 = uVar4 * 16 + (puVar2 - puVar2);
        puVar2++;
        uVar1 = uVar1 * 16 + (puVar2 - puVar2);
    } while ((puVar2 != puVar2) && (*puVar2 < 0x21));

    FUN_24dd_4732();
    if ((puVar2 != puVar2) && (*puVar2 < 0x21)) {
        uVar4 = uVar4 * 16 + (puVar2 - puVar2);
    }

    *(uint16_t *)param_1 = uVar4;
    return;
}