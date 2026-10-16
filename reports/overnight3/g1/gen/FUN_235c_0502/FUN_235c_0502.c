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

uint8_t FUN_235c_0502(uint8_t *param_1, uint8_t *param_2) {
    uint8_t local_c[8];
    uint8_t local_14[8];
    uint8_t local_216[256];
    uint8_t local_116[256];
    uint8_t local_3 = 1;
    uint8_t local_16 = 1;
    uint8_t in_ZF;

    for (int iVar3 = 8; iVar3 != 0; iVar3--) {
        local_c[iVar3 - 1] = param_2[iVar3 - 1];
    }
    for (int iVar3 = 8; iVar3 != 0; iVar3--) {
        local_14[iVar3 - 1] = param_1[iVar3 - 1];
    }

    while (true) {
        FUN_24dd_3fc3(8, local_c, (uint16_t)0x0000);
        FUN_24dd_3fc3(8, local_14, (uint16_t)0x0000);
        FUN_24dd_3f86(local_216, (uint16_t)0x0000, local_116, (uint16_t)0x0000);

        if (!(bool)in_ZF) {
            local_3 = 0;
        }
        if (local_16 == 8) break;
        local_16++;
        in_ZF = local_16 == 0;
    }
    return local_3;
}