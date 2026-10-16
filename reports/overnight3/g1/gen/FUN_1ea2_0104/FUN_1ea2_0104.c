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

extern void FUN_24dd_029f(uint16_t, uint16_t, uint16_t);

uint16_t __stdcall16far FUN_1ea2_0104(uint16_t *param_1) {
    int iVar1;
    uint16_t in_AX;
    uint8_t uVar2;
    uint8_t extraout_AH;
    int *piVar3;
    uint16_t *puVar4;
    uint16_t uVar5;
    uint8_t local_3;

    uVar2 = (uint8_t)(in_AX >> 8);
    local_3 = 0;
    if (*(char *)0x65ee > -1) {
        iVar1 = *(int *)(*(char *)0x65ee * 2 + 0x65e8);
        int local_6 = 0;
        while (true) {
            uVar5 = (uint16_t)((uint32_t)*param_1 >> 16);
            piVar3 = (int *)((int)*param_1 + local_6 * 4);
            if (*piVar3 != 0 || piVar3[1] != 0) {
                uVar5 = (uint16_t)((uint32_t)*param_1 >> 16);
                puVar4 = (uint16_t *)((int)*param_1 + local_6 * 4);
                FUN_24dd_029f(*(uint16_t *)(*(char *)0x65ee * 2 + 0x65e2), *puVar4, puVar4[1]);
            }
            if (local_6 == iVar1 - 1) break;
            local_6++;
        }
        FUN_24dd_029f(*(int *)(*(char *)0x65ee * 2 + 0x65e8) << 2, *(uint16_t *)param_1,
                      *(uint16_t *)((int)(uint16_t *)param_1 + 2));
        *(char *)0x65ee = *(char *)0x65ee - 1;
        local_3 = 1;
        uVar2 = extraout_AH;
    }
    return (uVar2 << 8) | local_3;
}