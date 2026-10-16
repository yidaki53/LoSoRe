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
void FUN_24dd_3d80(void);
void FUN_2494_0060(uint16_t, uint16_t);
uint32_t FUN_235c_0b33(int, uint16_t);

void FUN_235c_0f57(char param_1, uint param_2, uint *param_3, uint16_t *param_4) {
    uint uVar1;
    uint uVar2;
    uint uVar3;
    uint uVar4;
    int iVar5;
    uint uVar6;
    uint16_t *puVar7;
    uint *puVar8;
    uint16_t uVar9;
    uint16_t uVar10;
    uint16_t unaff_DS;
    uint32_t uVar11;
    int local_a;
    uint16_t uVar12;

    uVar9 = (uint16_t)((uintptr_t)param_4 >> 16);
    puVar7 = (uint16_t *)param_4;
    uVar1 = puVar7[3];
    uVar2 = puVar7[4];
    local_a = 0x6856;
    *(uint16_t *)0x782a = *param_4;
    *(uint16_t *)0x7830 = 0;
    uVar12 = unaff_DS;
    while (param_2 != 0) {
        uVar10 = (uint16_t)((uintptr_t)param_3 >> 16);
        puVar8 = (uint *)param_3;
        uVar4 = (uVar2 - puVar8[1]) - (uint)(uVar1 < *param_3);
        if (((int)uVar4 < 1) && ((0x7fff < uVar4 || (uVar1 - *param_3 <= param_2)))) {
            uVar4 = *param_3;
            uVar6 = puVar8[1];
            *(int *)0x7826 = uVar1 - *param_3;
            *(int *)0x7828 = (uVar2 - uVar6) - (uint)(uVar1 < uVar4);
        } else {
            *(uint *)0x7826 = param_2;
            *(uint16_t *)0x7828 = 0;
        }
        uVar4 = puVar7[1];
        iVar5 = puVar7[2];
        uVar6 = *param_3;
        uVar3 = puVar8[1];
        *(int *)0x782c = uVar4 + *param_3;
        *(int *)0x782e = iVar5 + uVar3 + (uint)((uVar4 + uVar6) >> 16);
        uVar4 = *param_3;
        uVar6 = puVar8[1];
        uVar3 = *(uint *)0x7826;
        iVar5 = *(int *)0x7828;
        *param_3 = uVar4 + *(uint *)0x7826;
        puVar8[1] = uVar6 + iVar5 + (uint)((uVar4 + uVar3) >> 16);
        if (param_1 != '\0') {
            uVar4 = uVar1;
            uVar6 = uVar2;
            FUN_24dd_3dbd();
            *param_3 = uVar4;
            puVar8[1] = uVar6;
        }
        *(int *)0x7832 = local_a;
        *(uint16_t *)0x7834 = uVar12;
        uVar11 = FUN_235c_0b33(local_a + *(int *)0x7826, uVar12);
        uVar12 = (uint16_t)((uintptr_t)uVar11 >> 16);
        local_a = (int)uVar11;
        param_2 = param_2 - *(int *)0x7826;
        iVar5 = *(int *)0x7828 + (uint)(0xfffe < *(uint *)0x7826);
        FUN_24dd_3dbd();
        uVar10 = FUN_24dd_3d80();
        *(uint16_t *)0x7826 = uVar10;