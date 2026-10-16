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
uint16_t FUN_24dd_0303(void);
uint32_t FUN_24dd_028a(uint16_t param_1);

// Global variable
extern uint8_t DAT_65ee;

uint8_t FUN_1ea2_0000(uint16_t param_1, uint16_t param_2, uint32_t *param_3) {
    uint32_t iVar1;
    uint32_t uVar2;
    uint32_t uVar3;
    uint16_t *puVar4;
    uint16_t uVar5;
    uint8_t local_3 = 0;

    if (DAT_65ee < 3) {
        *(uint16_t *)(DAT_65ee * 2 + 0x65e2) = param_2;
        *(uint32_t *)(DAT_65ee * 2 + 0x65e8) = param_1;
        uVar2 = FUN_24dd_0303();
        if ((param_1 < 0x8000) &&
            ((0 < (int)param_1 ||
             ((uint32_t)(*(uint16_t *)(DAT_65ee * 2 + 0x65e2) * *(uint32_t *)(DAT_65ee * 2 + 0x65e8)) <=
              uVar2)))) {
            uVar3 = FUN_24dd_028a(*(uint32_t *)(DAT_65ee * 2 + 0x65e8) << 2);
            uVar2 = (uint32_t)((uint64_t)uVar3 >> 16);
            *param_3 = (uint32_t)uVar3;
            *(uint32_t *)((int)param_3 + 2) = uVar2;
            iVar1 = *(uint32_t *)(DAT_65ee * 2 + 0x65e8);
            int local_6 = 0;
            while (true) {
                uVar2 = FUN_24dd_0303();
                if (0x7fff < uVar2) {
                    return 0;
                }
                if (((int)uVar2 < 1) && (uVar2 < *(uint16_t *)(DAT_65ee * 2 + 0x65e2))) {
                    return 0;
                }
                uVar3 = FUN_24dd_028a(*(uint16_t *)(DAT_65ee * 2 + 0x65e2));
                uVar2 = (uint32_t)((uint64_t)uVar3 >> 16);
                uVar5 = (uint16_t)((uint64_t)*param_3 >> 16);
                puVar4 = (uint16_t *)((int)*param_3 + local_6 * 4);
                *puVar4 = (uint16_t)uVar3;
                puVar4[1] = uVar2;
                if (local_6 == iVar1 - 1) break;
                local_6++;
            }
            DAT_65ee++;
            local_3 = 1;
        }
    }
    return local_3;
}