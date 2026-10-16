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

void FUN_24cb_0058(void) {
    uint16_t *puVar1;
    uint16_t uVar2;
    uint16_t *puVar3;
    uint16_t uVar4;
    uint16_t *puVar5;
    uint16_t uVar6;

    uVar6 = (uint16_t)((uint16_t)0x10000 >> 16);
    puVar1 = (uint16_t *)0x10000;
    do {
        for (uVar2 = 0x100; *puVar1 != 0; uVar2--) {
            puVar3 = puVar1;
            puVar1 = puVar1 + 1;
        }
        puVar5 = puVar1;
        puVar1 = puVar1 - 1;
        uVar4 = 0;
        do {
            for (uVar6 = 0x100; *puVar3 != 0; uVar6--) {
                puVar5 = puVar5 + 1;
                puVar3 = puVar3 + 1;
            }
            puVar5 = puVar5 - 1;
            puVar3 = puVar3 - 1;
            uVar4 = uVar4 + 1;
        } while (uVar4 != 0);
        puVar5 = puVar5 - 1;
        puVar3 = puVar3 - 1;
    } while (uVar6 != 0);
    *(uint16_t *)0x78ee = 0;
    return;
}