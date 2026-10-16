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
bool FUN_24dd_4161(void);
void FUN_24dd_3d80(void);
int FUN_24dd_3dbd(void);
void FUN_202c_1b84(uint16_t, uint16_t, uint16_t, uint8_t);

void FUN_1000_5aef(int param_1) {
    uint32_t *puVar1;
    uint8_t bVar2;
    uint32_t uVar3;
    int iVar4;
    uint32_t uVar5;
    int iVar6;
    uint16_t *puVar7;
    uint16_t uVar8;
    uint16_t uVar11;
    uint16_t uVar12;
    uint16_t *puVar10;
    uint16_t uVar13;
    uint16_t uVar14;

    uVar12 = 0x1000;
    uVar11 = 0x5afa;
    FUN_24dd_0530();
    uVar8 = *(uint16_t *)0x6698;
    iVar6 = *(uint32_t *)0x6698 + param_1 * 0xe;
    puVar10 = (uint16_t *)(((uint32_t)uVar8 << 16) | (iVar6 - 0xe));
    uVar5 = *(uint32_t *)(iVar6 - 8);
    iVar4 = *(int *)(iVar6 - 6);
    puVar1 = (uint32_t *)(iVar6 - 0xc);
    uVar3 = *puVar1;
    *puVar1 = *puVar1 + uVar5;
    *(int *)(iVar6 - 10) = *(int *)(iVar6 - 10) + iVar4 + (uVar3 + uVar5 < uVar3);
    iVar4 = 0x20;
    bVar2 = FUN_24dd_4161();
    puVar7 = puVar10;
    uVar8 = *(uint16_t *)puVar10;
    if (*(uint8_t *)(iVar4 + 0x14c0) & bVar2) {
        puVar1 = puVar7 + 3;
        uVar3 = *puVar1;
        *puVar1 = *puVar1 + 0x5dc;
        puVar7[4] = puVar7[4] + (0xfa23 < uVar3);
    }
    iVar4 = puVar7[2] + puVar7[4] + (puVar7[1] + puVar7[3] < puVar7[1]);
    iVar6 = 0x20;
    bVar2 = FUN_24dd_4161(puVar10, puVar7[1] + puVar7[3], iVar4, uVar11, uVar12);
    if (*(uint8_t *)(iVar6 + 0x6604) & bVar2 || iVar4 > 0x15c) {
        uVar3 = puVar10[4];
        FUN_24dd_3d80();
        iVar4 = FUN_24dd_3dbd();
        uVar8 = *(uint16_t *)puVar10;
        puVar7 = puVar10;
        puVar7[3] = -iVar4;
        puVar7[4] = (~uVar3 + 1) - (iVar4 != 0);
        uVar3 = puVar7[3];
        uVar5 = puVar7[4];
        if ((int)uVar5 < 0) {
            bool bVar9 = uVar3 != 0;
            uVar3 = -uVar3;
            uVar5 = (~uVar5 + 1) - bVar9;
        }
        if ((int)uVar5 < 0 || ((int)uVar5 < 1 && uVar3 < 100)) {
            puVar7[3] = 0;
            puVar7[4] = 0;
        }
    }
    uVar8 = *(uint16_t *)puVar10;
    puVar7 = puVar10;
    puVar7[5] = puVar7[5] - 1;
    if (puVar7[5] == 0) {
        FUN_202c