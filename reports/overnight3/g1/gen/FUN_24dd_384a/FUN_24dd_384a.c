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

void FUN_24dd_384a(uint16_t bx, uint16_t dx) {
    uint16_t *puVar1;
    uint32_t uVar2;
    uint32_t uVar3;
    uint32_t uVar4;
    bool bVar5;

    if (*(uint32_t *)(0x6410) == 0) {
        if (*(uint32_t *)(bx + 2) != -0x284e) {
            *(uint16_t *)(0x6410) = 0x69;
            return;
        }
        do {
            uVar3 = *(uint32_t *)(bx + 4) - *(uint32_t *)(bx + 8);
            bVar5 = dx < uVar3;
            dx = dx - uVar3;
            if (bVar5) {
                uVar3 = uVar3 + dx;
                dx = 0;
            }
            uVar2 = *(uint32_t *)(bx + 0xc);
            uVar4 = (uint32_t)uVar2;
            puVar1 = (uint16_t *)(*(uint32_t *)(bx + 8) + uVar4);
            for (; uVar3 != 0; uVar3 = uVar3 - 1) {
                *puVar1 = 0x20;
                puVar1 = puVar1 + 1;
            }
            uVar4 = (uint32_t)puVar1 - uVar4;
            *(uint32_t *)(bx + 8) = uVar4;
            if (uVar4 == *(uint32_t *)(bx + 4)) {
                FUN_24dd_396c();
            }
        } while (dx != 0);
    }
    return;
}