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

typedef void (*code)(void);

uint16_t FUN_24dd_3ce0(int param_1, char *param_2) {
    char *pcVar1;
    code *pcVar2;
    uint8_t bVar3;
    int iVar4;
    uint16_t in_CX;
    char *unaff_SI;
    char *pcVar5;
    uint16_t unaff_ES;
    uint16_t unaff_DS;

    if (param_1 == 0) {
        pcVar2 = (code *)0x21;
        bVar3 = (*pcVar2)();
        iVar4 = 0;
        if (2 < bVar3) {
            unaff_ES = *(uint16_t *)0x2c;
            pcVar5 = (char *)0x0;
LAB_24dd_3d06:
            if (*pcVar5 != '\0') {
                iVar4 = -1;
                do {
                    if (iVar4 == 0) break;
                    iVar4 = iVar4 + -1;
                    pcVar1 = pcVar5;
                    pcVar5 = pcVar5 + 1;
                } while (*pcVar1 != '\0');
                goto LAB_24dd_3d06;
            }
            unaff_SI = pcVar5 + 3;
            iVar4 = 0x100;
            pcVar5 = unaff_SI;
            do {
                if (iVar4 == 0) break;
                iVar4 = iVar4 + -1;
                pcVar1 = pcVar5;
                pcVar5 = pcVar5 + 1;
            } while (*pcVar1 != '\0');
            in_CX = 0;
            iVar4 = ((uint16_t)iVar4 >> 8) | (~(uint8_t)iVar4);
        }
    } else {
        iVar4 = FUN_24dd_3d36();
    }
    pcVar5 = (char *)param_2;
    *param_2 = (char)iVar4;
    for (; pcVar5 = pcVar5 + 1, iVar4 != 0; iVar4 = iVar4 + -1) {
        pcVar1 = unaff_SI;
        unaff_SI = unaff_SI + 1;
        *pcVar5 = *pcVar1;
    }
    return in_CX;
}