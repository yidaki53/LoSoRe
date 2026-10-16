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

void FUN_1ec2_10cf(uint16_t, uint16_t, uint16_t, uint16_t, uint16_t, uint16_t, uint16_t, uint16_t);

void FUN_1ec2_10ea(int param_1, uint8_t *param_2) {
    uint8_t local_302[768];
    uint8_t *pbVar5 = param_2;
    uint8_t *pbVar4 = local_302;
    int iVar3 = 0x300;

    while (iVar3 != 0) {
        *pbVar4++ = *pbVar5++;
        iVar3--;
    }

    uint8_t local_303 = 0;
    while (true) {
        uint local_306 = (uint8_t)local_302[(uint16_t)local_303 * 3] * param_1 >> 5;
        uint local_308 = (uint8_t)local_302[(uint16_t)local_303 * 3 + 1] * param_1 >> 5;
        uint local_30a = (uint8_t)local_302[(uint16_t)local_303 * 3 + 2] * param_1 >> 5;
        uint local_30e = (uint8_t)local_302[(uint16_t)local_303 * 3 + 1] * param_1 >> 5;

        if (local_303 == 0xff) break;

        FUN_1ec2_10cf(local_306, local_308, local_30a, local_30e, local_303, 0, 0, 0);
    }
}