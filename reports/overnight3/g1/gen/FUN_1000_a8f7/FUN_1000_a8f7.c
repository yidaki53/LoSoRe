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

void FUN_24dd_0530(void);
uint FUN_24dd_3d80(void);

void FUN_1000_a8f7(uint16_t param_1, int *param_2, uint8_t *param_3) {
    uint8_t local_102[252];
    uint8_t *pbVar1;
    uint32_t uVar2;
    uint32_t uVar3;
    uint32_t uVar4;
    int iVar5;
    uint8_t *pbVar6;
    int *piVar7;
    uint16_t uVar8;
    uint16_t local_10a;
    int local_108;
    uint8_t bVar9;

    local_102[0] = *param_3;
    pbVar1 = local_102;
    pbVar6 = param_3;
    uVar4 = (uint32_t)local_102[0];
    for (; uVar4 != 0; uVar4--) {
        *pbVar1++ = *pbVar6++;
    }
    uVar8 = (uint16_t)((uint32_t)param_2 >> 16);
    piVar7 = (int *)param_2;
    *param_2 = 0;
    piVar7[1] = 0;
    uVar4 = (uint32_t)local_102[0];
    if (uVar4 != 0) {
        local_10a = 1;
        local_108 = 0;
        while (true) {
            iVar5 = piVar7[1];
            uVar2 = FUN_24dd_3d80();
            uVar3 = local_102[local_10a] - 0x30;
            *param_2 = uVar3 + uVar2;
            piVar7[1] = ((int)uVar3 >> 15) + iVar5 + (uint32_t)((uVar3 + uVar2) < uVar3);
            if ((local_108 == 0) && (local_10a == uVar4)) break;
            bVar9 = 0xfffe < local_10a;
            local_10a = local_10a + 1;
            local_108 = local_108 + (uint32_t)bVar9;
        }
    }
}