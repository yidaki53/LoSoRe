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

uint16_t FUN_202c_0b0e(uint16_t param_1, uint16_t param_2) {
    uint8_t *pbVar1;
    uint8_t *pbVar2;
    uint32_t uVar3;
    uint16_t uVar4;
    uint8_t uVar5;
    uint8_t extraout_AH;
    uint32_t uVar6;
    uint8_t *pbVar7;
    uint8_t local_188[2];
    int local_186;
    uint8_t local_184[128];
    uint8_t local_104;
    uint8_t abStack_103[256];
    char local_3;

    pbVar7 = (uint8_t *)param_2;
    local_104 = *param_2;
    pbVar2 = abStack_103;
    for (uVar6 = (uint32_t)local_104; pbVar7 = pbVar7 + 1, uVar6 != 0; uVar6 = uVar6 - 1) {
        pbVar1 = pbVar2;
        pbVar2 = pbVar2 + 1;
        *pbVar1 = *pbVar7;
    }
    uVar4 = FUN_202c_0843(&local_104, param_1);
    local_3 = (char)uVar4;
    uVar5 = (uint8_t)((uint32_t)uVar4 >> 8);
    if (local_3 != '\0') {
        FUN_24dd_3b22(&local_104, param_1, local_184, param_1);
        FUN_24dd_3b5d(1, local_184, param_1);
        FUN_24dd_04f4();
        local_186 = 0;
        while (true) {
            uVar3 = *(uint32_t *)((int)*(uint32_t *)0x6674 + local_186 * 4);
            FUN_24dd_3c48(local_188, param_1, 0x1f8, (int)uVar3, (int)((uint64_t)uVar3 >> 0x10), local_184, param_1);
            FUN_24dd_04f4();
            if (local_186 == 0x15d) break;
            local_186 = local_186 + 1;
        }
        FUN_24dd_3bde(local_184, param_1);
        FUN_24dd_04f4();
        uVar5 = extraout_AH;
    }
    return ((uint16_t)uVar5 << 8) | local_3;
}