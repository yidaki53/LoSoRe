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

void FUN_1000_5e66() {
    uint16_t local_338;
    uint16_t local_2;
    uint16_t local_6520;
    uint16_t local_6684;
    uint16_t local_6670;
    uint16_t local_6688;
    uint16_t local_fec8;
    uint16_t local_feca;
    uint16_t local_fed4;
    uint16_t local_fed6;
    uint16_t local_fed0;
    uint16_t local_fed2;
    uint16_t local_fecc;
    uint16_t local_fece;
    uint16_t local_feda;
    uint16_t local_4;
    uint16_t local_258;

    local_338 = 0x338;
    CALLF(0x2000, 0x5300, &local_338);
    local_2 = *(uint16_t *)0x2;
    int32_t temp = (int32_t)local_2;
    uint16_t cx = (uint16_t)(temp >> 16);
    uint16_t dx = (uint16_t)temp;
    local_6520 = *(uint16_t *)0x6520;
    dx = 0;
    CALLF(0x2000, 0x8b8d, cx, dx);
    cx = local_6520;
    dx = 0;
    if (cx != 0 || dx != 0) {
        goto label_5e9a;
    }
    uint16_t es;
    uint16_t di;
    *(uint16_t *)&es = *(uint16_t *)0x6684;
    di = *(uint16_t *)((uint16_t *)&es + 2);
    PUSH(es);
    PUSH(di);
    CALLF(0x1000, 0xfff3);
label_5e9a:
    local_2 = 0;
    goto label_5ea4;
label_5ea1:
    local_2++;
label_5ea4:
    temp = (int32_t)local_2 * 0xaa;
    cx = (uint16_t)(temp >> 16);
    di = (uint16_t)temp;
    *(uint16_t *)&es = *(uint16_t *)0x6670;
    di += cx;
    *(uint16_t *)&local_fec8 = di;
    *(uint16_t *)&local_feca = es;
    if (*(uint16_t *)(es * 0x10 + di + 0x4c) != 0) {
        goto label_5ebc;
    }
    if (*(uint8_t *)(es * 0x10 + di + 0x9a) == 0) {
        goto label_6010;
    }
    cx = *(uint16_t *)(es * 0x10 + di + 0x6);
    cx -= 0x50;
    di = local_2;
    di <<= 1;
    *(uint16_t *)(di + 0x67b0) = cx;
    *(uint16_t *)&es = *(uint16_t *)&local_fec8;
    cx = *(uint16_t *)(es * 0x10 + di + 0xa);
    cx -= 0x50;
    di = local_2;
    di <<= 1;
    *(uint16_t *)(di + 0x67b4) = cx;
    local_fed4 = 0;
    local_fed6 = 0;
    local_fed0 = 0;
    local_fed2 = 0;
    local_fecc = 0;
    local_fece = 0;
    *(uint16_t *)&es = *(uint16_t *)&local_fec8;
    cx = *(uint16_t *)(es * 0x10 + di + 0x4e);
    cx <<= 1;
    di += cx;
    di = *(uint16_t *)(es * 0x10 + di + 0x73);
    if (*(uint8_t *)(di + 0x11a5) != 0x2) {
        goto label_5fc1;
    }
    local_4 = 0;
    goto label_5f32;
label_5f2f: