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

void __stdcall16far FUN_1ec2_12e6(uint8_t param_1, char *param_2, uint32_t param_3, uint32_t param_4, uint32_t param_5) {
    char *pcVar1;
    uint8_t bVar2;
    char cVar3;
    uint8_t uVar4;
    char cVar5;
    char cVar6;
    char *pcVar7;
    uint8_t *puVar8;
    uint8_t *puVar9;
    uint16_t uVar10;
    uint16_t uVar11;

    uVar10 = (uint16_t)(param_3 >> 16);
    pcVar7 = param_2;
    uVar11 = (uint16_t)(param_2 >> 16);
    if ((((param_5 + 8 < 8) || (0x13f < param_5 + 8)) || (param_4 + 7 < 7)) || (199 < param_4 + 7)) {
        bVar2 = (uint8_t)param_4;
        puVar8 = (uint8_t *)((int)param_3 + param_4 * 0x140 + param_5);
        cVar5 = '\a';
        do {
            cVar6 = '\b';
            do {
                puVar9 = puVar8;
                pcVar1 = pcVar7;
                pcVar7 = pcVar7 + 1;
                cVar3 = (char)param_5;
                if (((param_5 < 0x140) && (bVar2 < 200)) && (*pcVar1 != '\0')) {
                    *puVar9 = param_1;
                }
                uVar4 = (uint8_t)(param_5 >> 8);
                param_5 = ((uint16_t)uVar4 << 8) | (cVar3 + 1);
                cVar6 = cVar6 - 1;
                puVar8 = puVar9 + 1;
            } while (cVar6 != '\0');
            puVar8 = puVar9 + 0x139;
            param_5 = ((uint16_t)uVar4 << 8) | (cVar3 - 7);
            bVar2 = bVar2 + 1;
            cVar5 = cVar5 - 1;
        } while (cVar5 != '\0');
    } else {
        puVar8 = (uint8_t *)((int)param_3 + param_4 * 0x140 + param_5);
        cVar5 = '\a';
        do {
            cVar6 = '\b';
            do {
                puVar9 = puVar8;
                pcVar1 = pcVar7;
                pcVar7 = pcVar7 + 1;
                if (*pcVar1 != '\0') {
                    *puVar9 = param_1;
                }
                cVar6 = cVar6 - 1;
                puVar8 = puVar9 + 1;
            } while (cVar6 != '\0');
            puVar8 = puVar9 + 0x139;
            cVar5 = cVar5 - 1;
        } while (cVar5 != '\0');
    }
    return;
}