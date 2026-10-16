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

int __stdcall16far FUN_202c_0673(uint16_t ds, uint16_t si, uint16_t di, uint16_t bp, uint16_t sp, uint16_t ss) {
    uint8_t *param_1 = (uint8_t *)(ds * 16 + si);
    uint8_t local_104[258];
    uint16_t local_108 = 1;
    uint16_t local_106 = 1;
    uint16_t uVar2;
    uint8_t *pbVar1;
    uint8_t *pbVar3;

    pbVar3 = param_1;
    local_104[0] = *param_1;
    pbVar1 = local_104;
    for (uVar2 = local_104[0]; pbVar1 = pbVar1 + 1, pbVar3 = pbVar3 + 1, uVar2 != 0; uVar2 = uVar2 - 1) {
        *pbVar1 = *pbVar3;
    }

    if (local_104[0] != 0) {
        while (true) {
            if (local_104[local_106] == 0xff) {
                local_106 = local_106 + 2;
            }
            local_108 = local_108 + (uint16_t)*(uint8_t *)((local_104[local_106] - 2) * 0x40 + 0x19e5);
            if (local_106 == local_104[0]) break;
            local_106 = local_106 + 1;
        }
    }
    return local_108 + 2;
}