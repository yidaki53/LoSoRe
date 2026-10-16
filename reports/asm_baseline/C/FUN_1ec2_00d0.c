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

void FUN_24dd_3dbd(void);
void FUN_24dd_3eaf(int, uint16_t*, uint16_t, uint16_t, uint16_t);
void FUN_24dd_3e95(uint16_t*, uint16_t);
void FUN_202c_076d(uint16_t, int);
void FUN_24dd_3f14(uint16_t*, uint16_t);

void __stdcall16far FUN_1ec2_00d0(uint16_t param_1, int param_2, uint32_t param_3) {
    uint16_t uVar1;
    int iVar2;
    uint16_t local_20c[256];
    uint16_t local_10c[256];
    uint16_t local_c[6];
    uint16_t local_6;
    int local_4;

    local_6 = FUN_24dd_3dbd();
    uVar1 = 0x3c;
    iVar2 = 0;
    local_4 = param_2;
    FUN_24dd_3dbd();
    local_c[0] = 0;
    if ((local_4 < 0) || ((local_4 < 1 && (local_6 < 10)))) {
        FUN_24dd_3eaf(5, local_c, __CS__, 0xcc, 0x24dd);
    }
    FUN_24dd_3e95(local_c, __CS__);
    FUN_202c_076d(local_6, local_4);
    FUN_24dd_3f14(local_10c, __CS__);
    FUN_24dd_3f14(0xce, 0x24dd);
    FUN_24dd_3eaf(5, local_c, __CS__, local_20c, __CS__);
    if ((iVar2 < 0) || ((iVar2 < 1 && (uVar1 < 10)))) {
        FUN_24dd_3e95(local_c, __CS__);
        FUN_24dd_3f14(0xcc, 0x24dd);
        FUN_24dd_3eaf(5, local_c, __CS__, local_10c, __CS__);
    }
    FUN_24dd_3e95(local_c, __CS__);
    FUN_202c_076d(uVar1, iVar2);
    FUN_24dd_3f14(local_10c, __CS__);
    FUN_24dd_3eaf(5, local_c, __CS__, local_20c, __CS__);
    FUN_24dd_3eaf(0xff, (int)param_3, (int)((uint32_t)param_3 >> 0x10), local_c, __CS__);
    return;
}