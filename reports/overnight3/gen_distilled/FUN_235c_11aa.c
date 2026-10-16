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

void FUN_235c_11aa(void) {
    int *piVar1;
    int *piVar2;
    int iVar3;
    int iVar4;
    uint8_t *puVar5;
    uint8_t *puVar6;

    iVar4 = *(int *)0x6e6c;
    puVar5 = (uint8_t *)*(uint16_t *)0x6a58;
    puVar6 = (uint8_t *)*(uint16_t *)0x6e86;
    iVar3 = 0x200;
    piVar2 = (int *)0x6a58;
    do {
        if (iVar3 == 0) break;
        iVar3--;
        piVar1 = piVar2;
        piVar2 = piVar2 + 1;
        puVar6 = puVar6 + 1;
        puVar5 = puVar5 + 1;
        *puVar6 = (uint8_t)*puVar5;
    } while (iVar3 != 0);
    return;
}