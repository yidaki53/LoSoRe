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
    uint8_t *pbVar1;
    uint16_t in_AX;
    int iVar2;
    int iVar3;
    uint8_t *pbVar4;
    int unaff_DI;
    uint8_t *pbVar5;
    uint8_t *pbVar6;
    bool in_CF;

    if (!in_CF) {
        pbVar5 = (uint8_t *)(unaff_DI + 0x1e);
        iVar2 = 0x100;
        do {
            if (iVar2 == 0) break;
            iVar2 = iVar2 - 1;
            pbVar1 = pbVar5;
            pbVar5 = pbVar5 + 1;
        } while (*pbVar1 != 0);
        iVar3 = ((uint8_t)iVar2 >> 8) | (~(uint8_t)iVar2);
        pbVar6 = pbVar5;
        while (true) {
            pbVar6 = pbVar6 - 1;
            pbVar4 = pbVar5 - 2;
            if (iVar3 == 0) break;
            iVar3 = iVar3 - 1;
            pbVar5 = pbVar5 - 1;
            *pbVar6 = *pbVar4;
        }
        *pbVar6 = ~(uint8_t)iVar2;
        in_AX = 0;
    }
    *(uint16_t *)0x78ee = in_AX;
    return;
}