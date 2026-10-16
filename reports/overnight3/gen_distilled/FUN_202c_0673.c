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

uint16_t FUN_24dd_4161(uint16_t param_1) {
    uint16_t uVar1;
    uint8_t *pbVar2;
    uint8_t *pbVar3;
    uint32_t uVar4;
    int iVar5;
    uint16_t uVar6;
    uint16_t local_108;
    uint16_t local_106;
    uint16_t local_104;
    uint16_t local_102;
    uint16_t local_100;
    uint16_t local_09e;
    uint16_t local_09c;
    uint16_t local_09a;
    uint16_t local_098;
    uint16_t local_096;
    uint16_t local_094;
    uint16_t local_092;
    uint16_t local_090;
    uint16_t local_08e;
    uint16_t local_08c;
    uint16_t local_08a;
    uint16_t local_088;
    uint16_t local_086;
    uint16_t local_084;
    uint16_t local_082;
    uint16_t local_080;

    uVar4 = (uint32_t)param_1;
    uVar1 = 1;
    pbVar2 = (uint8_t *)0x0;
    while (true) {
        pbVar3 = (uint8_t *)0x0;
        while (true) {
            uVar6 = (uint16_t)(uVar4 >> 16);
            local_088 = (uint16_t)uVar4;
            uVar4 = uVar4 * 2;
            local_090 = local_088 + 1;
            local_092 = local_088 + 2;
            if (uVar6 == 0) break;
            uVar1 = uVar1 * 2;
        }
        if (uVar1 == param_1) break;
        uVar1 = uVar1 / 2;
    }
    local_096 = local_088 + 3;
    local_094 = local_088 + 4;
    local_092 = local_088 + 5;
    local_090 = local_088 + 6;
    local_08e = local_088 + 7;
    local_098 = local_088 + 8;
    local_096 = local_096 * 16 + 0x19e5;
    local_094 = local_094 * 16 + 0x19e5;
    local_092 = local_092 * 16 + 0x19e5;
    local_090 = local_090 * 16 + 0x19e5;
    local_08c = local_088 + 9;
    local_08a = local_088 + 10;
    local_088 = local_088;
    local_096 = local_096;
    local_094 = local_094;
    local_092 = local_092;
    local_090 = local_090;
    local_08e = local_08e;
    local_098 = local_098;
    local_096 = local_096;
    local_094 = local_094;
    local_092 = local_092;
    local_090 = local_090;
    local_08e = local_08e;
    local_098 = local_098;
    local_096 = local_096;
    local_094 = local_094;
    local_092 = local_092;
    local_090 = local_090;
    local_08e = local_08e;
    local_098 = local_098;
    local_096 = local_096;
    local_094 = local_094;
    local_092 = local_092;
    local_0