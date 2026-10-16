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

extern void FUN_24dd_0530(void);

uint16_t FUN_1000_9e7a(void) {
    char cVar1;
    int iVar2;
    uint16_t uVar3;
    int iVar4;
    uint16_t uVar5;
    uint16_t local_3;

    local_3 = 0x10;
    FUN_24dd_0530();
    cVar1 = *(char *)0x66ac;
    uVar3 = ((uint16_t)extraout_AH << 8) | cVar1;
    if (cVar1 != '\0') {
        if (cVar1 != '\x01') {
            if ((cVar1 != '\x02') && (cVar1 != '\x03')) goto LAB_1000_9f40;
            uVar3 = *(uint16_t *)0x66a3;
            uVar5 = (uint16_t)((*(uint32_t *)0x6670) >> 16);
            iVar4 = (int)*(uint32_t *)0x6670;
            iVar2 = *(int *)(iVar4 + 0x42);
            if (((int)uVar3 >> 0xf < iVar2) ||
                (((int)uVar3 >> 0xf <= iVar2 && (uVar3 <= *(uint16_t *)(iVar4 + 0x40))))) {
LAB_1000_9f3b:
                uVar3 = ((uint16_t)(uVar3 >> 8) << 8) | 1;
            } else {
                uVar3 = *(uint16_t *)0x66a3;
                uVar5 = (uint16_t)((*(uint32_t *)0x6670) >> 16);
                iVar4 = (int)*(uint32_t *)0x6670;
                iVar2 = *(int *)(iVar4 + 0xec);
                if (((int)uVar3 >> 0xf < iVar2) ||
                    (((int)uVar3 >> 0xf <= iVar2 && (uVar3 <= *(uint16_t *)(iVar4 + 0xea))))) goto LAB_1000_9f3b;
                uVar3 = uVar3 & 0xff00;
            }
            local_3 = (uint16_t)uVar3;
            goto LAB_1000_9f40;
        }
        uVar3 = *(uint16_t *)0x66a1;
        uVar5 = (uint16_t)((*(uint32_t *)0x6670) >> 16);
        iVar4 = (int)*(uint32_t *)0x6670;
        iVar2 = *(int *)(iVar4 + 0x46);
        if (((int)uVar3 >> 0xf < iVar2) ||
            (((int)uVar3 >> 0xf <= iVar2 && (uVar3 <= *(uint16_t *)(iVar4 + 0x44))))) {
LAB_1000_9efa:
            uVar3 = ((uint16_t)(uVar3 >> 8) << 8) | 1;
        } else {
            uVar3 = *(uint16_t *)0x66a1;
            uVar5 = (uint16_t)((*(uint32_t *)0x6670) >> 16);
            iVar4 = (int)*(uint32_t *)0x6670;
            iVar2 = *(int *)(iVar4 + 0xf0);
            if (((int)uVar3 >> 0xf < iVar2) ||
                (((int)uVar3 >> 0xf <= iVar2 && (uVar3 <= *(uint16_t *)(iVar4 + 0xee))))) goto LAB_1000_9efa;
            uVar3 = uVar3 & 0xff00;
        }
        local_3 = (uint16_t)uVar3;
        goto LAB_1000_9f40;
    }
    uVar5 = (uint16_t)((*(uint32_t *)0x6670) >> 16);
    iVar4 = (int)*(uint32_t *)0x6670;
    iVar2 = *(int *)(iVar4 + 0x3a);
    if ((iVar2 < 0) || ((iVar2 < 1 && (*(int