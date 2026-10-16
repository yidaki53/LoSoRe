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

void FUN_2971_67f6(uint16_t, uint16_t, uint16_t, uint16_t, int, uint16_t, int, int);

void __stdcall16far FUN_1ec2_13e9(uint32_t param_1, uint32_t param_2, uint8_t param_3, uint8_t *param_4, int param_5, int param_6) {
    uint8_t bVar1;
    uint8_t bVar2;
    uint8_t local_102[256];
    uint8_t local_105;
    uint32_t local_104;
    uint32_t uVar6;
    uint16_t uVar9;
    uint16_t uVar10;

    bVar1 = *param_4;
    local_102[0] = bVar1;
    for (uVar6 = bVar1; uVar6 != 0; uVar6--) {
        local_102[uVar6] = param_4[uVar6];
    }

    uVar9 = (uint16_t)(param_1 >> 16);
    uint16_t iVar8 = (uint16_t)param_1;
    *((uint8_t *)0x65f0) = *((uint8_t *)(iVar8 + 0x273f));

    if (bVar1 != 0) {
        local_104 = 1;
        while (true) {
            local_105 = local_102[local_104];
            if (local_105 == 0) {
                param_5 += (uint32_t)*((uint8_t *)0x65f0);
                param_6 = param_6;
            } else {
                if (local_105 == 0xff) {
                    if (param_3 == 1) {
                        param_3 = local_102[local_104 + 1];
                    }
                    local_105 = local_102[local_104 + 2];
                    local_104 += 2;
                }
                local_105 -= 2;
                bVar2 = *((uint8_t *)(iVar8 + local_105 * 0x40 + 0x3f));
                uVar10 = (uint16_t)(param_2 >> 16);
                if ((0x13f - (uint32_t)bVar2) < param_6) {
                    param_5 += (uint32_t)*((uint8_t *)0x65f0);
                    FUN_2971_67f6(0x1ec2, ((uint16_t)local_105 * 0x40 >> 8) | param_3, iVar8 + local_105 * 0x40, uVar9, (int)param_2, uVar10, param_5, param_6);
                    param_6 = param_6;
                } else {
                    FUN_2971_67f6(0x1ec2, ((uint16_t)local_105 * 0x40 >> 8) | param_3, iVar8 + local_105 * 0x40, uVar9, (int)param_2, uVar10, param_5, param_6);
                }
                param_6 += (uint32_t)bVar2;
            }
            if (local_104 == bVar1) break;
            local_104++;
        }
    }
}