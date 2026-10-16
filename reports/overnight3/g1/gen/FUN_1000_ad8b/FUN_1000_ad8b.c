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

extern void FUN_24dd_0530();
extern void FUN_24ba_00c4();
extern void FUN_202c_076d(uint param_1, int param_2);
extern void FUN_24dd_3eaf(uint param_1, byte *param_2, uint param_3, byte *param_4, uint param_5);
extern void FUN_24dd_3e95(byte *param_1, uint param_2);
extern void FUN_24dd_3f14(uint param_1, uint param_2);
extern uint FUN_202c_0673(byte *param_1, uint param_2);
extern void FUN_1ec2_00a5(uint param_1, int param_2, int param_3, int param_4, int param_5, int param_6);
extern void FUN_1ec2_0d88(uint param_1, uint param_2, uint param_3, int param_4, int param_5);
extern void FUN_1ec2_13e9(uint param_1, uint param_2, int param_3, int param_4, uint param_5, byte *param_6, uint param_7, int param_8, int param_9);
extern byte FUN_249c_019d();
extern void FUN_24dd_403d(uint param_1, byte param_2, byte *param_3, uint param_4);
extern void FUN_24dd_3fb1(byte param_1);
extern void FUN_1000_a8f7(int param_1, uint *param_2, uint param_3, byte *param_4, uint param_5);
extern void FUN_235c_095c(uint param_1, uint param_2, uint param_3, uint param_4);

uint FUN_1000_ad8b(int param_1, int param_2, uint param_3, uint param_4, int param_5, int param_6) {
    int iVar1;
    int iVar2;
    byte extraout_AH;
    int iVar3;
    byte local_313[256];
    byte local_213[256];
    uint local_113;
    byte local_111[256];
    byte local_11;
    uint local_10;
    uint local_e;
    uint local_8;
    int local_6;
    uint local_4;

    local_4 = 0x1000;
    local_6 = -0x526a;
    FUN_24dd_0530();
    *((byte *)(param_1 - 0x20e)) = 1;
    FUN_24ba_00c4();
    byte *pbVar4 = local_213;
    uint uVar5 = (uint)&local_213;
    FUN_202c_076d(param_2, param_2 >> 0xf);
    FUN_24dd_3eaf(0xff, local_111, uVar5, pbVar4, uVar5);
    pbVar4 = local_213;
    iVar3 = (int)param_3 >> 0xf;
    uVar5 = (uint)&local_213;
    FUN_202c_076d(param_3, iVar3);
    local_10 = (uint)*pbVar4;
    local_e = 0;
    do {
        pbVar4 = local_213;
        uVar5 = (uint)&local_213;
        FUN_24dd_3e95(local_111, uVar5);
        FUN_24dd_3f14(0xad89, 0x24dd);
        local_113 = FUN_202c_0673(pbVar4, uVar5);
        FUN_1ec2_00a5(8, (0x14a - param_5) + (local_113 >> 1),
                      (int)*(uint32_t *)0x65d7 + param_6 * 0x140 +
                      ((param_5 + -10) - (local_113 >> 1)), (int)((uint)*(uint32_t *)0x65d7 >> 0x10),
                      (int)*(uint3