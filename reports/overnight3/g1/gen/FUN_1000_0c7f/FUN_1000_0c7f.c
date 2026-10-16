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

// Global data
extern uint8_t DAT_14a0;

uint8_t FUN_1000_0c7f(int param_1, int param_2, int param_3, int param_4, int param_5, int param_6) {
    uint8_t local_3 = 1;
    uint32_t uVar4;

    FUN_24dd_0530();

    uVar4 = (param_4 - param_6) >> 0xf;
    if ((((int)((param_4 - param_6 ^ uVar4) - uVar4) < 0xa1) &&
         (uVar4 = (param_3 - param_5) >> 0xf, (int)((param_3 - param_5 ^ uVar4) - uVar4) < 0xa1)) ||
        ((uVar4 = (param_2 - param_6) >> 0xf, (int)((param_2 - param_6 ^ uVar4) - uVar4) < 0xa1 &&
         (uVar4 = (param_1 - param_5) >> 0xf, (int)((param_1 - param_5 ^ uVar4) - uVar4) < 0xa1)))) {
        local_3 = 0;
    } else {
        int iVar2 = param_6 + -3;
        if (iVar2 <= param_6 + 3) {
            while (true) {
                int iVar3 = param_5 + -4;
                if (iVar3 <= param_5 + 4) {
                    while (true) {
                        uint8_t bVar1 = FUN_24dd_4161();
                        if ((DAT_14a0 & bVar1) != 0) {
                            return 0;
                        }
                        if (iVar3 == param_5 + 4) break;
                        iVar3 = iVar3 + 1;
                    }
                }
                if (iVar2 == param_6 + 3) break;
                iVar2 = iVar2 + 1;
            }
        }
    }
    return local_3;
}