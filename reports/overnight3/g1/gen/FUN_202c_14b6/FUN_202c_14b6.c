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

extern uint16_t FUN_24dd_4654(uint16_t);

void __stdcall16far FUN_202c_14b6(uint16_t param_1, int param_2, uint16_t param_3, int param_4, uint16_t param_5,
                                 uint16_t param_6, int param_7, uint8_t param_8) {
    uint16_t local_4 = 0;
    uint8_t bVar2 = param_8 & 0x7f;
    uint16_t uVar4;
    int iVar5;
    uint16_t uVar6;
    uint16_t uVar1;

    while (*(char *)((*(uint16_t *)0x6694 + local_4 * 0x14 + 0x12) & 0xFFFF) != '\0' && local_4 < 600) {
        local_4++;
    }

    *(char *)((*(uint16_t *)0x6694 + local_4 * 0x14 + 0x12) & 0xFFFF) = param_8;
    *(uint16_t *)((*(uint16_t *)0x6694 + local_4 * 0x14 + 2) & 0xFFFF) = param_6;
    *(uint16_t *)((*(uint16_t *)0x6694 + local_4 * 0x14 + 6) & 0xFFFF) = param_5;

    uVar4 = FUN_24dd_4654(*(uint16_t *)((uint16_t)bVar2 * 2 + 0x56c) << 1);
    uVar1 = *(uint16_t *)((uint16_t)bVar2 * 2 + 0x56c);
    uVar6 = (uint16_t)((*(uint32_t *)0x6694 >> 16) & 0xFFFF);
    iVar5 = (*(uint16_t *)0x6694 + local_4 * 0x14) & 0xFFFF;
    *(uint16_t *)(iVar5 + 8) = (param_3 - uVar1) + uVar4;
    *(uint16_t *)(iVar5 + 10) =
        ((param_4 - ((int)uVar1 >> 15)) - (uint16_t)(param_3 < uVar1)) +
        (uint16_t)((param_3 - uVar1) < uVar4);

    uVar4 = FUN_24dd_4654(*(uint16_t *)((uint16_t)bVar2 * 2 + 0x56c) << 1);
    uVar1 = *(uint16_t *)((uint16_t)bVar2 * 2 + 0x56c);
    uVar6 = (uint16_t)((*(uint32_t *)0x6694 >> 16) & 0xFFFF);
    iVar5 = (*(uint16_t *)0x6694 + local_4 * 0x14) & 0xFFFF;
    *(uint16_t *)(iVar5 + 0xc) = (param_1 - uVar1) + uVar4;
    *(uint16_t *)(iVar5 + 0xe) =
        ((param_2 - ((int)uVar1 >> 15)) - (uint16_t)(param_1 < uVar1)) +
        (uint16_t)((param_1 - uVar1) < uVar4);

    if (*(char *)(bVar2 + 0x645) == '\0') {
        if (param_7 < 1) {
            *(uint8_t *)(iVar5 + 0x13) = *(uint8_t *)(bVar2 + 0x68d);
        } else {
            *(uint8_t *)(iVar5 + 0x13) = (uint8_t)param_7;
        }
    } else {
        uint8_t uVar3 = FUN_24dd_4654(*(uint8_t *)(bVar2 + 0x65d) + 1);
        *(uint8_t *)(iVar5 + 0x13) = uVar3;
    }

    iVar5 = FUN_24dd_4654(*(uint16_t *)((uint16_t)bVar2 * 2 + 0x7c4));
    *(uint16_t *)(