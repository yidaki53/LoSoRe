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

void __stdcall16far FUN_1ec2_0e8f(char *param_1, uint32_t param_2, int param_3, uint param_4, int param_5, int param_6) {
    int iVar1;
    int iVar2;
    uint8_t bVar3;
    uint uVar4;
    char *pcVar5;
    char *pcVar6;

    if ((((param_5 < 0x9e) && (param_6 < 0x9e)) && (-1 < param_5 + param_3)) &&
        (-1 < (int)(param_6 + param_4))) {
        pcVar5 = (char *)param_1;
        pcVar6 = (char *)((int)param_2 + param_5 * 0x140 + param_6);
        iVar1 = 0x140 - (param_4 & 0xff);
        do {
            while (uVar4 = param_4 & 0xff, -1 < param_5) {
                iVar2 = param_6;
                if (0x9d < param_5) {
                    return;
                }
                do {
                    if (-1 < iVar2) {
                        if (0x9d < iVar2) {
                            pcVar6 = pcVar6 + uVar4 + iVar1;
                            pcVar5 = pcVar5 + uVar4;
                            goto joined_r0x0001fb40;
                        }
                        if (*pcVar5 != '\0') {
                            *pcVar6 = *pcVar5;
                        }
                    }
                    pcVar6 = pcVar6 + 1;
                    pcVar5 = pcVar5 + 1;
                    iVar2 = iVar2 + 1;
                    bVar3 = (uint8_t)uVar4 - 1;
                    uVar4 = (uint)bVar3;
                } while (bVar3 != 0);
                pcVar6 = pcVar6 + iVar1;
                param_5 = param_5 + 1;
                param_3 = param_3 + -1;
                if ((char)param_3 == '\0') {
                    return;
                }
            }
            pcVar6 = pcVar6 + 0x140;
            pcVar5 = pcVar5 + param_4;
joined_r0x0001fb40:
            param_3 = param_3 + -1;
            param_5 = param_5 + 1;
        } while ((char)param_3 != '\0');
    }
    return;
}