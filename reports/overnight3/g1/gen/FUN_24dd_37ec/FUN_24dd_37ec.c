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

void FUN_24dd_396c(int, int, int, int, int); // External symbol

void __cdecl16near FUN_24dd_37ec(void) {
    uint32_t uVar1;
    void (*in_AX)(int, int, int);
    uint16_t in_CX;
    uint16_t in_DX;
    int in_BX;
    int iVar2;
    uint16_t unaff_DI;
    uint16_t unaff_ES;
    uint16_t unaff_DS;

    if (*(int *)0x6410 == 0) {
        if (*(int *)(in_BX + 2) != -0x284f) {
            *(uint16_t *)0x6410 = 0x68;
            return;
        }
        iVar2 = *(int *)(in_BX + 8);
        if (iVar2 == *(int *)(in_BX + 10)) goto LAB_24dd_3830;
        while (true) {
            uVar1 = *(uint32_t *)(in_BX + 0xc);
            in_AX = (void (*)(int, int, int))(*(uint32_t *)(in_BX) + (uint32_t)unaff_ES * 16);
            in_AX(in_BX, unaff_ES, unaff_DS);
            *(int *)(in_BX + 8) = (iVar2 + (int)uVar1) - (int)((uint32_t)in_AX >> 16);
            if (in_AX == (void (*)(int, int, int))0x0) break;
LAB_24dd_3830:
            FUN_24dd_396c(in_BX, unaff_ES, unaff_DI, in_DX, in_CX);
            iVar2 = *(int *)(in_BX + 8);
            if (iVar2 == *(int *)(in_BX + 10)) {
                return;
            }
        }
    }
    return;
}