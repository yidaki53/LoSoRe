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

void FUN_1ec2_1008(uint16_t *param_1, uint16_t *param_2, char param_3, char param_4, char param_5, char param_6, uint8_t param_7, int param_8, uint param_9, int param_10, int param_11) {
    int iVar1;
    int iVar2;
    uint8_t bVar3;
    uint uVar4;
    uint8_t *pbVar5;
    uint8_t *pbVar6;
    uint16_t uVar7;
    uint16_t uVar8;

    if ((param_11 < 0x9e) && (param_10 < 0x9e) && (-1 < param_11 + param_8) && (-1 < (int)(param_10 + param_9))) {
        uVar8 = (uint16_t)((uintptr_t)param_1 >> 16);
        pbVar5 = (uint8_t *)param_1;
        uVar7 = (uint16_t)((uintptr_t)param_2 >> 16);
        pbVar6 = (uint8_t *)((int)param_2 + param_11 * 0x140 + param_10);
        iVar1 = 0x140 - param_9;

        while (param_11 != 0) {
            uVar4 = param_9;
            while (uVar4 != 0) {
                iVar2 = param_8;
                while (iVar2 != 0) {
                    bVar3 = *pbVar5;
                    *pbVar6 = bVar3;
                    pbVar5++;
                    pbVar6++;
                    iVar2--;
                }
                uVar4--;
                pbVar5 = (uint8_t *)((int)pbVar5 + iVar1);
                pbVar6 = (uint8_t *)((int)pbVar6 + iVar1);
            }
            param_11--;
            pbVar5 = (uint8_t *)((int)pbVar5 + iVar1);
            pbVar6 = (uint8_t *)((int)pbVar6 + iVar1);
        }
    }
}