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

void FUN_24dd_3c03(void);

void __stdcall16far FUN_24dd_3c4f(uint16_t *param_1, uint16_t param_2, uint16_t param_3, uint16_t param_4, uint32_t param_5) {
    uint16_t uVar3 = 0x65;
    uint16_t uVar4 = (uint16_t)(param_5 >> 16);
    FUN_24dd_3c03();
    int16_t iVar5 = (int16_t)(param_1 >> 16);
    if (__builtin_expect(param_2 == 0, 0)) {
        if (param_2 != 0) {
            bool bVar6 = (int16_t)((uint32_t)param_2 * *(uint32_t *)((uint32_t)param_5 + 4) >> 16) != 0;
            // Assuming swi(0x21) is a software interrupt, which is not directly translatable to C.
            // This part needs to be replaced with the actual function call or logic.
            uint16_t uVar2 = 0; // Placeholder for the result of the software interrupt
            if (bVar6) {
                *(uint16_t *)0x6410 = uVar2;
                goto LAB_24dd_3c9e;
            }
            uVar2 = uVar2 / *(uint32_t *)((uint32_t)param_5 + 4);
            uVar3 = param_4;
            // unaff_DS is dropped as it's not used in the function
        }
        if (iVar5 == 0 && (uint16_t *)param_1 == (uint16_t *)0x0) {
            if (uVar2 != param_2) {
                *(uint16_t *)0x6410 = uVar3;
            }
        } else {
            *param_1 = uVar2;
        }
    } else {
LAB_24dd_3c9e:
        if (iVar5 != 0 || (uint16_t *)param_1 != (uint16_t *)0x0) {
            *param_1 = 0;
        }
    }
    return;
}