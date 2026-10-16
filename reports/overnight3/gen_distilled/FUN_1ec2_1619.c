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

void __stdcall16far FUN_1ec2_1619(uint8_t param_1, uint8_t param_2, uint8_t param_3, uint8_t param_4) {
    uint8_t local_8;
    uint8_t local_4;

    FUN_1ec2_152f(0x2000, 0x161f, &local_4, &local_8, 0, 0);
    local_8 = param_4;
    if (param_3 == local_8) {
        local_4 = param_3;
        FUN_1ec2_152f(0x2000, 0x1652, &local_8, &local_4, 0, 0);
        return;
    }
    local_4 = local_8;
    FUN_1ec2_152f(0x2000, 0x168d, &local_8, &local_4, 0, 0);
    return;
}