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

void FUN_24dd_3fb1(uint8_t param_1);
void FUN_24dd_3f14(uint8_t *param_1, uint16_t param_2);
void FUN_24dd_3eaf(uint8_t param_1, int param_2, int param_3, uint8_t *param_4, uint16_t param_5);

void __stdcall16far FUN_1ec2_0018(uint param_1, uint32_t param_2) {
    uint8_t local_402[256];
    uint8_t local_302[256];
    uint8_t local_202[256];
    uint8_t local_102[256];

    uint8_t *puVar3 = local_102;
    uint16_t uVar4 = (uint16_t)(param_1 >> 12);
    FUN_24dd_3fb1(*(uint8_t *)((param_1 >> 12) + 0x4a6));
    uint8_t *puVar1 = local_202;
    uint16_t uVar2 = (uint16_t)(param_1 >> 8);
    FUN_24dd_3fb1(*(uint8_t *)(((param_1 >> 8) & 0xf) + 0x4a6));
    FUN_24dd_3f14(puVar1, uVar2);
    puVar1 = local_302;
    uVar2 = (uint16_t)(param_1 >> 4);
    FUN_24dd_3fb1(*(uint8_t *)(((param_1 >> 4) & 0xf) + 0x4a6));
    FUN_24dd_3f14(puVar1, uVar2);
    puVar1 = local_402;
    FUN_24dd_3fb1(*(uint8_t *)((param_1 & 0xf) + 0x4a6));
    FUN_24dd_3f14(puVar1, (uint16_t)param_1);
    FUN_24dd_3eaf(0xff, (int)param_2, (int)(param_2 >> 16), puVar3, uVar4);
    return;
}