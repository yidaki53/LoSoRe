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

void FUN_24dd_0673(void) {
    uint16_t *puVar1;
    uint16_t *puVar2;
    int iVar3;
    uint16_t *puVar4;
    uint16_t *puVar5;
    uint16_t *seg_d8 = (uint16_t *)0xd8;

    puVar4 = (uint16_t *)*(uint16_t *)seg_d8;
    puVar5 = puVar4 - 6;
    *(uint16_t *)seg_d8 = (uint16_t)puVar5;
    for (iVar3 = 6; iVar3 != 0; iVar3--) {
        puVar2 = puVar5;
        puVar5 = puVar5 + 1;
        puVar1 = puVar4;
        puVar4 = puVar4 + 1;
        *puVar2 = *puVar1;
    }
    return;
}