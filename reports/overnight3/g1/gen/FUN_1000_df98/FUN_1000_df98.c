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
int FUN_24dd_3d2f(void);
void FUN_24dd_3ce0(int param_1);
void FUN_24dd_3eaf(uint8_t param_1, uint8_t *param_2, uint16_t param_3, uint8_t *param_4, uint16_t param_5);
void FUN_24dd_3ed3(int param_1, int param_2, uint8_t *param_3, uint16_t param_4);
void FUN_24dd_3f86(uint16_t param_1, uint16_t param_2, uint8_t *param_3, uint16_t param_4);
uint16_t FUN_202c_0706(uint8_t *param_1, uint16_t param_2);
void FUN_24dd_3e95(uint16_t param_1, uint16_t param_2);
uint16_t FUN_24dd_4919(uint16_t param_1);
void FUN_24dd_3fb1(uint16_t param_1);
void FUN_24dd_3f14(uint8_t *param_1, uint16_t param_2);

void FUN_1000_df98(void) {
    int *piVar1;
    uint16_t uVar2;
    uint8_t extraout_AH;
    uint16_t uVar3;
    uint8_t extraout_AH_00;
    uint32_t uVar4;
    uint16_t uVar5;
    uint16_t unaff_SS;
    uint16_t unaff_DS;
    uint8_t uVar6;
    uint8_t uVar7;
    uint8_t local_50a[256];
    uint8_t local_40a[2];
    uint8_t local_408[254];
    uint32_t local_30a;
    uint8_t local_308[256];
    uint8_t local_208[256];
    int local_108;
    uint8_t local_106[256];
    uint32_t local_6;
    int local_4;

    local_4 = 0x1000;
    local_6 = 0xdfa3;
    FUN_24dd_0530();
    local_108 = FUN_24dd_3d2f();
    uVar6 = local_108 == 1;
    if (local_108 < 1) {
        return;
    }
    local_4 = 1;
    do {
        uint8_t *puVar9 = local_208;
        uVar2 = unaff_SS;
        FUN_24dd_3ce0(local_4);
        FUN_24dd_3eaf(0xff, local_106, unaff_SS, puVar9, uVar2);
        puVar9 = local_208;
        uVar2 = unaff_SS;
        FUN_24dd_3ed3(2, 1, local_106, unaff_SS);
        FUN_24dd_3f86(0xdf56, 0x24dd, puVar9, uVar2);
        if (uVar6) {
LAB_1000_e022:
            puVar9 = local_408;
            uVar2 = unaff_SS;
            FUN_24dd_3ed3(local_106[0] - 2, 3, local_106, unaff_SS);
            uVar5 = 0x202c;
            uVar2 = FUN_202c_0706(puVar9, uVar2);
            *(uint16_t *)0x66aa = uVar2;
            if (0xc < *(int *)0x66aa % 0x19) {
                *(int *)0x66aa = *(int *)0x66aa + 0x19;
            }
            piVar1 = (int *)0x66aa;
            *piVar1 = *piVar1 - *(int *)0x66aa % 0x19;
            uVar7 = *piVar1 == 0;
        } else {
            puVar9 = local_308;
            uVar2