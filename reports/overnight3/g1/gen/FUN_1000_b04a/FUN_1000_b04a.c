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

void FUN_24dd_0530(void);
void FUN_24ba_00c4(void);
void FUN_24dd_3e95(uint8_t *param_1, uint16_t param_2);
void FUN_24dd_3f14(uint16_t param_1, uint16_t param_2);
uint32_t FUN_202c_0673(uint8_t *param_1, uint16_t param_2);
void FUN_1ec2_00a5(uint8_t param_1, int param_2, int param_3, int param_4, int param_5, int param_6);
void FUN_1ec2_0d88(uint8_t param_1, uint8_t param_2, uint32_t param_3, int param_4, int param_5);
void FUN_1ec2_13e9(uint16_t param_1, uint16_t param_2, int param_3, int param_4, uint8_t param_5, uint8_t *param_6, uint16_t param_7, int param_8, int param_9);
void FUN_24dd_403d(uint8_t param_1, uint8_t param_2, uint8_t *param_3, uint16_t param_4);
uint8_t FUN_249c_019d(void);
void FUN_24dd_3fb1(uint16_t param_1);
void FUN_24dd_3eaf(uint8_t param_1, int param_2, int param_3, uint8_t *param_4, uint16_t param_5);
void FUN_24ba_0090(void);
void FUN_235c_095c(uint8_t param_1, uint8_t param_2, uint16_t param_3, uint16_t param_4);

void FUN_1000_b04a(int param_1, uint8_t *param_2, int param_3, int param_4, int param_5, uint32_t param_6) {
    uint8_t local_309[256];
    uint8_t local_209[256];
    uint32_t local_109;
    char local_107;
    uint8_t local_102;
    uint8_t abStack_101[251];

    uint16_t unaff_SS = 0x1000;
    uint16_t unaff_DS = 0xb055;

    FUN_24dd_0530();
    uint8_t *pbVar6 = param_2;
    local_102 = *param_2;
    uint8_t *pbVar2 = abStack_101;
    for (uint32_t uVar5 = (uint32_t)local_102; pbVar6 = pbVar6 + 1, uVar5 != 0; uVar5 = uVar5 - 1) {
        uint8_t *pbVar1 = pbVar2;
        pbVar2 = pbVar2 + 1;
        *pbVar1 = *pbVar6;
    }
    *(uint8_t *)(param_1 + -0x20e) = 1;
    FUN_24ba_00c4();
    do {
        uint8_t *puVar7 = local_209;
        uint16_t uVar9 = unaff_SS;
        FUN_24dd_3e95(&local_102, unaff_SS);
        FUN_24dd_3f14(0xb048, 0x24dd);
        local_109 = FUN_202c_0673(puVar7, uVar9);
        FUN_1ec2_00a5(8, (0x14a - param_4) + (local_109 >> 1),
                      (int)*(uint32_t *)0x65d7 + param_5 * 0x140 +
                      ((param_4 + -10) - (local_109 >> 1)), (int)((uint64_t)*(uint32_t *)0x65d7 >> 0x10),
                      (int)*(uint32_t *)0x6684 + param_5 * 0x140 +
                      ((param_