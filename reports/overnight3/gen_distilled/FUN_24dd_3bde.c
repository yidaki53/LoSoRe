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

void __cdecl16far FUN_24dd_3bde(uint16_t param_1) {
    int iVar1;
    uint16_t uVar2;
    uint8_t bVar3;

    bVar3 = 0;
    FUN_24dd_3b33();
    if (*(int *)(param_1 + 0x6410) < 4) {
        uVar2 = 0x4;
        while (true) {
            iVar1 = 0x21;
            bVar3 = in(iVar1) != 0;
            if (bVar3) break;
            uVar2 = uVar2 * 10 + *(uint8_t *)(param_1 + 0x6410);
        }
        *(uint16_t *)(param_1 + 0x6410) = 0;
        *(uint16_t *)((int)param_1 + 2) = 0xd7b0;
    }
    return;
}