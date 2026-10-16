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

void FUN_24dd_36c4(uint32_t param_1) {
    int16_t iVar1;
    int16_t iVar2;
    bool bVar4;

    iVar2 = (int16_t)param_1;
    iVar1 = *(int16_t *)(param_1 + 2);
    if ((iVar1 == -0x284f) || (iVar1 == -0x284e)) {
        FUN_24dd_3711(iVar2, (uint16_t)(param_1 >> 16));
    } else if (iVar1 != -0x2850) {
        *(uint16_t *)0x6410 = 0x66;
        return;
    }
    bVar4 = true;
    *(uint16_t *)(param_1 + 2) = *(uint16_t *)0x2;
    *(uint16_t *)(param_1 + 8) = 0;
    *(uint16_t *)(param_1 + 10) = 0;
    FUN_24dd_374d();
    if (!bVar4) {
        *(uint16_t *)(param_1 + 2) = 0xd7b0;
    }
    return;
}