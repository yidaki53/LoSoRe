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

void FUN_1ec2_00d0(uint16_t param1, uint16_t param2) {
    uint16_t local_4;
    uint16_t local_2;
    uint8_t local_a;
    uint16_t ax, dx, cx, bx;

    // Stack frame setup
    ax = param1;
    dx = param2;
    cx = 0x3c;
    bx = 0;
    CALLF(0x2000, 0x8b8d);
    local_4 = ax;
    local_2 = dx;

    ax = param1;
    dx = param2;
    cx = 0x3c;
    bx = 0;
    CALLF(0x2000, 0x8b8d);
    ax = cx;
    dx = bx;
    param1 = ax;
    param2 = dx;

    local_a = 0;

    if (local_2 < 0) {
        goto loc_1000_ed36;
    }
    if (local_2 > 0) {
        goto loc_1000_ed47;
    }
    if (local_4 >= 0xa) {
        goto loc_1000_ed47;
    }

    di = 0xcc;
    PUSH_CS();
    PUSH(di);
    LEA(di, &local_a);
    PUSH_SS();
    PUSH(di);
    PUSH(0x5);
    CALLF(0x2000, 0x8c7f);

    LEA(di, 0xfdf6);
    PUSH_SS();
    PUSH(di);
    LEA(di, &local_a);
    PUSH_SS();
    PUSH(di);
    CALLF(0x2000, 0x8c65);

    LEA(di, 0xfef6);
    PUSH_SS();
    PUSH(di);
    PUSH(local_2);
    PUSH(local_4);
    CALLF(0x2000, 0x0a2d);
    CALLF(0x2000, 0x8ce4);

    di = 0xce;
    PUSH_CS();
    PUSH(di);
    CALLF(0x2000, 0x8ce4);

    LEA(di, &local_a);
    PUSH_SS();
    PUSH(di);
    PUSH(0x5);
    CALLF(0x2000, 0x8c7f);

    if (param2 < 0) {
        goto loc_1000_ed91;
    }
    if (param2 > 0) {
        goto loc_1000_edb7;
    }
    if (param1 >= 0xa) {
        goto loc_1000_edb7;
    }

    LEA(di, 0xfef6);
    PUSH_SS();
    PUSH(di);
    LEA(di, &local_a);
    PUSH_SS();
    PUSH(di);
    CALLF(0x2000, 0x8c65);

    di = 0xcc;
    PUSH_CS();
    PUSH(di);
    CALLF(0x2000, 0x8ce4);

    LEA(di, &local_a);
    PUSH_SS();
    PUSH(di);
    PUSH(0x5);
    CALLF(0x2000, 0x8c7f);

    LEA(di, 0xfdf6);
    PUSH_SS();
    PUSH(di);
    LEA(di, &local_a);
    PUSH_SS();
    PUSH(di);
    CALLF(0x2000, 0x8c65);

    LEA(di, 0xfef6);
    PUSH_SS();
    PUSH(di);
    PUSH(param2);
    PUSH(param1);
    CALLF(0x2000, 0x0a2d);
    CALLF(0x2000, 0x8ce4);

    LEA(di, &local_a);
    PUSH_SS();
    PUSH(di);
    PUSH(0x5);
    CALLF(0x2000, 0x8c7f);

    LEA(di, &local_a);
    PUSH_SS();
    PUSH(di);
    LES(di, *(uint16_t*)(BP + 0xa));
    PUSH(ES);
    PUSH(di);
    PUSH(0xff);
    CALLF(0x2000, 0x8c7f);

    // Stack frame teardown
    LEAVE();
    RETF(0x4);
}