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

void FUN_1ec2_10cf(uint16_t, uint16_t, uint16_t, uint16_t); // External symbol

void __stdcall16far FUN_1ec2_10ea(int param_1, byte *param_2) {
    byte local_302[768];
    byte *pbVar5 = param_2;
    byte *pbVar6 = local_302;
    int iVar4;

    for (iVar4 = 0x300; iVar4 != 0; iVar4--) {
        *pbVar6++ = *pbVar5++;
    }

    byte local_303 = 0;
    while (true) {
        uint local_306 = (uint)local_302[(uint)local_303 * 3] * param_1 >> 5;
        uint local_308 = (uint)local_302[(uint)local_303 * 3 + 1] * param_1 >> 5;
        uint local_30a = (uint)local_302[(uint)local_303 * 3 + 2] * param_1 >> 5;
        if (local_306 > 0x3f) local_306 = 0x3f;
        if (local_308 > 0x3f) local_308 = 0x3f;
        if (local_30a > 0x3f) local_30a = 0x3f;
        byte bVar3 = (byte)((uint)local_302[(uint)local_303 * 3 + 2] * param_1 >> 0xd);
        FUN_1ec2_10cf(((uint16_t)bVar3 << 8) | local_30a, ((uint16_t)bVar3 << 8) | local_308,
                      ((uint16_t)bVar3 << 8) | local_306, ((uint16_t)bVar3 << 8) | local_303);
        if (local_303 == 0xff) break;
        local_303++;
    }
}