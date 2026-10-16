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

void FUN_24dd_2361(void);

void FUN_24dd_0e57(uint16_t *unaff_SI, uint16_t *in_BX, uint16_t *unaff_DI) {
    uint16_t *puVar1;
    uint16_t *puVar2;
    int iVar3;

    if ((((unaff_SI[3] & 0x7fff) == 0 && unaff_SI[0] == 0) && unaff_SI[1] == 0) && unaff_SI[2] == 0) {
        if (in_BX == (uint16_t *)0xffff) {
            return;
        }
        if ((int)in_BX[4] < 0x4001) {
            return;
        }
        if ((((in_BX[3] & 0x7fff) == 0 && in_BX[0] == 0) && in_BX[1] == 0) && in_BX[2] == 0) {
            return;
        }
    } else if (((((in_BX == (uint16_t *)0xffff) || ((int)in_BX[4] < 0x4001)) ||
                ((((in_BX[3] & 0x7fff) == 0 && in_BX[0] == 0) && in_BX[1] == 0) && in_BX[2] == 0)) ||
               (in_BX[3] < unaff_SI[3])) ||
              ((in_BX[3] <= unaff_SI[3] &&
               ((in_BX[2] < unaff_SI[2] ||
                ((in_BX[2] <= unaff_SI[2] &&
                 ((in_BX[1] < unaff_SI[1] || ((in_BX[1] <= unaff_SI[1] && in_BX[0] < unaff_SI[0])))))))))))
              ) goto LAB_24dd_0ece;
    unaff_SI = in_BX;
LAB_24dd_0ece:
    FUN_24dd_2361();
    for (iVar3 = 6; iVar3 != 0; iVar3 = iVar3 + -1) {
        puVar2 = unaff_DI;
        unaff_DI = unaff_DI + 1;
        puVar1 = unaff_SI;
        unaff_SI = unaff_SI + 1;
        *puVar2 = *puVar1;
    }
    return;
}