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

void FUN_24dd_3899(uint16_t in_AX, uint16_t in_BX, uint16_t in_DX) {
    uint16_t *puVar1;
    uint16_t *puVar2;
    uint32_t uVar3;
    uint16_t uVar4;
    bool bVar7;
    uint16_t *unaff_SI;

    if (*(uint32_t *)(0x6410) == 0) {
        if (*(uint32_t *)(in_BX + 2) != -0x284e) {
            *(uint16_t *)(0x6410) = 0x69;
            return;
        }
        do {
            uVar4 = *(uint32_t *)(in_BX + 4) - *(uint32_t *)(in_BX + 8);
            bVar7 = in_AX < uVar4;
            in_AX = in_AX - uVar4;
            if (bVar7) {
                uVar4 = uVar4 + in_AX;
                in_AX = 0;
            }
            uVar3 = *(uint32_t *)(in_BX + 0xc);
            int iVar5 = (int)uVar3;
            puVar6 = (uint16_t *)(*(uint32_t *)(in_BX + 8) + iVar5);
            for (; uVar4 != 0; uVar4 = uVar4 - 1) {
                puVar2 = puVar6;
                puVar6 = puVar6 + 1;
                puVar1 = unaff_SI;
                unaff_SI = unaff_SI + 1;
                *puVar2 = *puVar1;
            }
            iVar5 = (int)puVar6 - iVar5;
            *(uint32_t *)(in_BX + 8) = iVar5;
            if (iVar5 == *(uint32_t *)(in_BX + 4)) {
                FUN_24dd_396c();
            }
        } while (in_AX != 0);
    }
    return;
}