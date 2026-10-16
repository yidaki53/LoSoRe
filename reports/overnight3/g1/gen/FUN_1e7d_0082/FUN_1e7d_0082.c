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

// External function declarations
void FUN_24dd_3eaf(uint8_t, uint8_t*, uint16_t, uint8_t*, uint16_t);
void FUN_24dd_3fb1(uint16_t);
int FUN_24dd_3f40(uint8_t*, uint16_t, uint8_t*, uint16_t);
void FUN_24dd_403d(uint16_t, uint16_t, uint8_t*, uint16_t);
void FUN_24dd_3e95(uint8_t, uint16_t);
void FUN_24dd_3fde(uint8_t, uint8_t, uint8_t*, uint16_t, uint8_t*, uint16_t);
uint16_t FUN_24dd_4824(int*, uint16_t, uint8_t*, uint16_t);

uint16_t FUN_1e7d_0082(char param_1, uint8_t param_2, uint8_t *param_3) {
    uint8_t *pbVar1;
    uint8_t *pbVar2;
    uint8_t extraout_AH;
    int iVar3;
    uint16_t uVar4;
    uint32_t uVar5;
    uint8_t *pbVar6;
    uint16_t unaff_SS;
    uint8_t *puVar7;
    uint16_t uVar8;
    uint8_t *puVar9;
    uint16_t uVar10;
    uint8_t local_408[254];
    uint8_t local_30a[2];
    uint8_t local_308[256];
    int local_208[2];
    uint8_t local_204[256];
    uint8_t local_104;
    uint8_t abStack_103[255];
    uint16_t local_4;

    pbVar6 = param_3;
    local_104 = *param_3;
    pbVar2 = abStack_103;
    for (uVar5 = (uint32_t)local_104; pbVar6 = pbVar6 + 1, uVar5 != 0; uVar5 = uVar5 - 1) {
        pbVar1 = pbVar2;
        pbVar2 = pbVar2 + 1;
        *pbVar1 = *pbVar6;
    }
    FUN_24dd_3eaf(0xff, local_204, unaff_SS, &local_104, unaff_SS);
    puVar9 = local_308;
    uVar4 = unaff_SS;
    FUN_24dd_3fb1(((uint16_t)extraout_AH << 8) | param_2);
    iVar3 = FUN_24dd_3f40(local_204, unaff_SS, puVar9, uVar4);
    if (iVar3 == 0) {
        local_4 = 0xff;
    } else {
        puVar9 = local_204;
        uVar8 = 1;
        puVar7 = local_408;
        uVar4 = unaff_SS;
        uVar10 = unaff_SS;
        FUN_24dd_3fb1(param_2);
        uVar4 = FUN_24dd_3f40(local_204, unaff_SS, puVar7, uVar4);
        FUN_24dd_403d(uVar4, uVar8, puVar9, uVar10);
        puVar9 = local_204;
        puVar7 = local_30a;
        uVar4 = unaff_SS;
        uVar10 = unaff_SS;
        FUN_24dd_3e95(0x7e, 0x24dd);
        uVar4 = FUN_24dd_3f40(local_204, unaff_SS, puVar7, uVar4);
        FUN_24dd_403d(0xff, uVar4, puVar9, uVar10);
        if (param_1 != '\0') {
            puVar9 = local_30a;
            uVar4 = unaff_SS;
            FUN_24dd_3e95(0x80, 0x24dd);
            FUN_24dd_3fde(1, 0xff, local_2