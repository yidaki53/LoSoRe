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

// External function declarations
void FUN_24dd_0530(void);
uint8_t FUN_24dd_4161(void);

// Global variables
extern uint8_t DAT_669c;
extern uint32_t DAT_6698;
extern uint8_t DAT_6604;
extern uint8_t DAT_14c0;

uint8_t FUN_1000_0961(uint param_1, int param_2, int param_3) {
    uint uVar1;
    uint8_t bVar2;
    int iVar3;
    int iVar4;
    int iVar5;

    FUN_24dd_0530();
    iVar3 = param_3 - 2;
    if (iVar3 <= param_3 + 2) {
        while (true) {
            iVar4 = param_2 - 2;
            if (iVar4 <= param_2 + 2) {
                while (true) {
                    iVar5 = 0x20;
                    bVar2 = FUN_24dd_4161();
                    if ((*(uint8_t *)(0x6604 + iVar5) & bVar2) != 0) {
                        return 0;
                    }
                    if (iVar4 == param_2 + 2) break;
                    iVar4++;
                }
            }
            if (iVar3 == param_3 + 2) break;
            iVar3++;
        }
    }
    while (true) {
        iVar3 = 0x20;
        bVar2 = FUN_24dd_4161();
        if ((*(uint8_t *)(0x14c0 + iVar3) & bVar2) == 0) break;
        param_2++;
    }
    if (DAT_669c != 0) {
        uVar1 = 1;
        while (true) {
            if ((((uVar1 != param_1) && (*(char *)((int)DAT_6698 + uVar1 * 0xe - 2) != '\0'))
                 && (param_3 - 0x1e < *(int *)((int)DAT_6698 + uVar1 * 0xe - 0xe))) &&
                (((*(int *)((int)DAT_6698 + uVar1 * 0xe - 0xe) < param_3 - 0x1e &&
                  (param_2 - 0x1e < *(int *)((int)DAT_6698 + uVar1 * 0xe - 10))) &&
                 (*(int *)((int)DAT_6698 + uVar1 * 0xe - 10) < param_2 - 0x1e)))) {
                return 0;
            }
            if (uVar1 == DAT_669c) break;
            uVar1++;
        }
    }
    return 1;
}