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

void __stdcall16far FUN_1ec2_1008(uint16_t *param_1, uint16_t *param_2, uint8_t param_3, uint8_t param_4, int param_5, uint param_6, int param_7, int param_8) {
    int iVar1;
    int iVar2;
    uint8_t bVar3;
    uint uVar4;
    uint8_t *pbVar5;
    uint8_t *pbVar6;
    uint16_t uVar7;
    uint16_t uVar8;

    if ((((param_7 < 0x9e) && (param_8 < 0x9e)) && (-1 < param_7 + param_5)) &&
        (-1 < (int)(param_8 + param_6))) {
        uVar8 = (uint16_t)((uintptr_t)param_1 >> 16);
        pbVar5 = (uint8_t *)param_1;
        uVar7 = (uint16_t)((uintptr_t)param_2 >> 16);
        pbVar6 = (uint8_t *)((uintptr_t)param_2 + param_7 * 0x140 + param_8);
        iVar1 = 0x140 - (param_6 & 0xff);
        do {
            while (uVar4 = param_6 & 0xff, -1 < param_7) {
                iVar2 = param_8;
                if (0x9d < param_7) {
                    return;
                }
                do {
                    if (-1 < iVar2) {
                        if (0x9d < iVar2) {
                            pbVar6 = pbVar6 + uVar4 + iVar1;
                            pbVar5 = pbVar5 + uVar4;
                            goto joined_r0x0001fcb8;
                        }
                        if ((*pbVar5 != 0) &&
                            ((bVar3 = *pbVar6, bVar3 < 7 || ((param_4 <= bVar3 && (bVar3 <= param_3)))))) {
                            *pbVar6 = *pbVar5;
                        }
                    }
                    pbVar6 = pbVar6 + 1;
                    pbVar5 = pbVar5 + 1;
                    iVar2 = iVar2 + 1;
                    bVar3 = (char)uVar4 - 1;
                    uVar4 = (uint)bVar3;
                } while (bVar3 != 0);
                pbVar6 = pbVar6 + iVar1;
                param_7 = param_7 + 1;
                param_5 = param_5 + -1;
                if ((char)param_5 == '\0') {
                    return;
                }
            }
            pbVar6 = pbVar6 + 0x140;
            pbVar5 = pbVar5 + uVar4;
joined_r0x0001fcb8:
            param_5 = param_5 + -1;
            param_7 = param_7 + 1;
        } while ((char)param_5 != '\0');
    }
    return;
}