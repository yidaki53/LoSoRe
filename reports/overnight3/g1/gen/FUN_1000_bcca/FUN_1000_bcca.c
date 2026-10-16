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

extern void FUN_24dd_0530(void);
extern void FUN_24dd_3eaf(uint16_t, uint16_t, uint16_t, uint16_t, uint16_t);
extern void FUN_202c_076d(uint16_t, uint16_t);
extern void FUN_1ec2_00d0(uint16_t, uint16_t);
extern void FUN_24dd_3f14(uint16_t, uint16_t);
extern void FUN_24dd_3e95(uint16_t, uint16_t);
extern char FUN_202c_0843(uint16_t, uint16_t);

void FUN_1000_bcca(uint16_t param_1) {
    char cVar1;
    uint16_t uVar2;
    uint16_t uVar4;
    uint16_t uStack_6;
    uint16_t uStack_4;
    uint8_t local_202[256];
    uint8_t local_102[252];

    uStack_4 = 0x1000;
    uStack_6 = 0xbcd5;
    FUN_24dd_0530();
    FUN_24dd_3eaf(0x10, param_1 - 0x10b, 0, ((uint8_t)*(uint16_t*)0x66ac) * 0x11 + 0x43a, 0);
    cVar1 = *(uint8_t*)0x66ac;
    if (cVar1 == '\0') {
        FUN_202c_076d(*(uint16_t*)0x669f, *(uint16_t*)0x669f >> 0xf);
        FUN_24dd_3eaf(0x10, param_1 - 0xfa, 0, (uint16_t)local_102, 0);
        FUN_24dd_3eaf(0x14, 599, 0, 0xbc7c, 0x24dd);
    } else if (cVar1 == '\x01') {
        FUN_1ec2_00d0(*(uint16_t*)0x66a1, *(uint16_t*)0x66a1 >> 0xf);
        FUN_24dd_3eaf(0x10, param_1 - 0xfa, 0, (uint16_t)local_102, 0);
        FUN_24dd_3eaf(0x14, 599, 0, 0xbc82, 0x24dd);
    } else if (cVar1 == '\x02' || cVar1 == '\x03') {
        FUN_202c_076d(*(uint16_t*)0x66a3, *(uint16_t*)0x66a3 >> 0xf);
        FUN_24dd_3eaf(0x10, param_1 - 0xfa, 0, (uint16_t)local_102, 0);
        FUN_24dd_3eaf(0x14, 599, 0, 0xbc8f, 0x24dd);
    }
    FUN_202c_076d(*(uint16_t*)0x669d, 0);
    FUN_24dd_3f14(0xbc9c, 0x202c);
    FUN_24dd_3eaf(0x10, param_1 - 0xe9, 0, (uint16_t)local_102, 0);
    FUN_202c_076d(*(uint8_t*)0x669c, 0);
    FUN_24dd_3eaf(0x10, param_1 - 0xd8, 0, (uint16_t)local_102, 0);
    FUN_24dd_3eaf(0x10, param_1 - 199, 0, ((uint8_t)*(uint16_t*)0x66ad) * 4 + 4, 0);
    FUN_24dd_3eaf(0