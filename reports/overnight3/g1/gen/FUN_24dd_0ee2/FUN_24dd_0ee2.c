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

void FUN_24dd_0ee2(uint16_t *param_1, uint16_t *param_2, uint16_t *param_3) {
    uint16_t uVar1;
    uint8_t bVar2;
    uint8_t bVar3;
    uint16_t uVar4;
    uint16_t uVar5;
    uint8_t bVar6;
    uint16_t uVar7;
    uint16_t uVar8;
    uint16_t uVar9;
    uint16_t uVar10;
    uint16_t uVar11;
    uint16_t uVar12;
    uint16_t uVar13;
    uint16_t uVar14;
    uint16_t *puVar15;
    int iVar16;
    bool bVar18;
    uint8_t local_7;
    uint16_t local_6;
    char local_4;
    int iVar17;

    bVar2 = (uint8_t)param_2[5] ^ (uint8_t)param_3[5];
    uVar5 = param_3[4];
    uVar14 = param_2[4];
    bVar18 = uVar5 < 0x4001;
    puVar15 = param_3;
    if ((int)uVar5 < 0x4001) {
        if (0x4000 < (int)uVar14) {
            bVar18 = false;
            local_7 = FUN_24dd_0e57();
            puVar15 = param_2;
            if (bVar18) {
                return;
            }
            goto LAB_24dd_0f75;
        }
        if ((int)uVar5 < (int)uVar14) {
            bVar6 = (uint8_t)param_2[5];
            uVar8 = uVar14;
            uVar14 = uVar5;
            puVar15 = param_2;
        } else {
            bVar6 = (uint8_t)param_3[5];
            uVar8 = uVar5;
            param_3 = param_2;
        }
        local_6 = puVar15[4];
        local_7 = bVar6;
        if ((-0x3fff < (int)uVar14) && ((int)(uVar8 - uVar14) < 0x41)) {
            bVar3 = (uint8_t)(uVar8 - uVar14);
            uVar14 = *param_3;
            uVar8 = param_3[1];
            uVar12 = param_3[2];
            uVar9 = param_3[3];
            local_4 = '\0';
            while (bVar18 = '\a' < (char)bVar3, bVar3 = bVar3 - 8, bVar18) {
                local_4 = (char)uVar14;
                uVar14 = ((uint16_t)uVar8 << 8) | (uVar14 >> 8);
                uVar8 = ((uint16_t)uVar12 << 8) | (uVar8 >> 8);
                uVar12 = ((uint16_t)uVar9 << 8) | (uVar12 >> 8);
                uVar9 = uVar9 >> 8;
            }
            for (bVar3 = bVar3 & 7; bVar3 != 0; bVar3 = bVar3 - 1) {
                uVar5 = uVar9 & 1;
                uVar9 = uVar9 >> 1;
                uVar4 = uVar12 & 1;
                local_4 = (char)((uVar14 & 1) != 0) >> 1;
                uVar14 = ((uVar8 & 1) != 0) >> 1;
                uVar12 = (uVar5 != 0) >> 1;
                uVar8 = (uVar4 != 0) >> 1;
            }
            if (bVar2 == 0) {
                uVar4 = uVar14 + *puVar15;
                uVar5 = (uint16_t)(uVar14 < *puVar15);
                uVar14 = uVar8 + puVar15[1];
                uVar13 = uVar14 + uVar5;