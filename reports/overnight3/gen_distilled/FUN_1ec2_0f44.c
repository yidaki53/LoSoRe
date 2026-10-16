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

void FUN_1ec2_0f44(uint16_t *param_1, uint16_t *param_2, uint8_t param_3, uint8_t param_4, int param_5, int param_6, uint16_t param_7, int param_8, int param_9) {
    int iVar1;
    int iVar2;
    uint16_t uVar3;
    uint16_t *puVar4;
    uint16_t *puVar5;
    uint16_t uVar6;
    uint16_t uVar7;
    uint8_t bVar8;
    uint8_t *pbVar9;
    uint8_t *pbVar10;

    if ((param_8 < 0x9e) && (param_9 < 0x9e) && (-1 < param_8 + param_5) && (-1 < (int)(param_9 + param_6))) {
        uVar3 = (uint16_t)((uintptr_t)param_1 >> 16);
        puVar4 = (uint16_t *)param_1;
        uVar6 = (uint16_t)((uintptr_t)param_2 >> 16);
        puVar5 = (uint16_t *)param_2;
        iVar1 = 0x140 - param_6;

        while (param_8 != 0) {
            uVar7 = param_9;
            if (param_8 < 0x9e) {
                uVar7 = 0;
            }

            while (uVar7 != 0) {
                if (param_6 < 0x9e) {
                    iVar2 = 0;
                    if (param_9 < 0x9e) {
                        iVar2 = 0;
                    }

                    while (iVar2 != 0) {
                        uVar1 = param_8;
                        if (param_8 < 0x9e) {
                            uVar1 = 0;
                        }

                        while (uVar1 != 0) {
                            if (param_6 < 0x9e) {
                                pbVar9 = (uint8_t *)puVar4;
                                puVar4 = puVar4 + 1;
                                pbVar10 = (uint8_t *)puVar5;
                                puVar5 = puVar5 + 1;
                                bVar8 = param_3;
                                if (param_3 < 0x9f) {
                                    bVar8 = 0;
                                }

                                while (iVar1 != 0) {
                                    uVar2 = param_9;
                                    if (param_9 < 0x9e) {
                                        uVar2 = 0;
                                    }

                                    while (uVar2 != 0) {
                                        if (param_6 < 0x9e) {
                                            pbVar1 = (uint8_t *)puVar4;
                                            puVar4 = puVar4 + 1;
                                            pbVar3 = (uint8_t *)puVar5;
                                            puVar5 = puVar5 + 1;
                                            iVar3 = param_8;
                                            if (param_8 < 0x9e) {
                                                iVar3 = 0;
                                            }

                                            while (iVar3 != 0) {
                                                uVar4 = param_9;
                                                if (param_9 < 0x9e) {
                                                    uVar4 = 0;
                                                }

                                                while (uVar4 != 0) {
                                                    if (param_6 < 0x9e) {
                                                        pbVar5 = (uint8_t *)puVar4;
                                                        puVar4 = puVar4 + 1;
                                                        pbVar6 = (uint8_t *)puVar5;
                                                        puVar5 = puVar5 + 1;
                                                        bVar9 = param_3;
                                                        if (param_3 < 0x9f) {
                                                            bVar9 = 0;
                                                        }

                                                        while (iVar1 != 0) {
                                                            uVar8 = param_9;
                                                            if (param_9 < 0x9e) {
                                                                uVar8 = 0;
                                                            }

                                                            while (uVar8 != 0) {
                                                                if (param_6 < 0x9e) {
                                                                    pbVar7 = (uint8_t *)puVar4;
                                                                    puVar4 = puVar4 + 1;
                                                                    pbVar10 = (uint8_t *)puVar5;
                                                                    puVar5 = puVar5 + 1;
                                                                    bVar6 = param_4;
                                                                    if (param_4 < 0x9f) {
                                                                        bVar6 = 0;
                                                                    }

                                                                    while (iVar1 != 0) {