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

void FUN_24dd_2e94(uint16_t param_1, uint16_t *param_2) {
    uint16_t uVar1;
    uint16_t *puVar2;
    uint16_t uVar3;
    uint16_t uVar4;
    uint8_t bVar5;
    uint16_t uVar6;
    uint16_t uVar7;

    if ((param_1 & 2) != 0) {
        asm volatile (
            "sti"
            : "=si" (puVar2), "=ax" (uVar1)
            : "0" (param_2), "1" (0x8000)
            : "memory"
        );
        uVar4 = (uint16_t)((uint8_t)(param_1 >> 8));
        if ((param_1 & 0x80) != 0) {
            puVar2 = puVar2 - 2;
            uVar6 = *puVar2;
            uVar3 = uVar6 & 0xff;
            if ((uVar3 < 9) && ((uVar6 & 0x100) != 0)) {
                puVar2 = puVar2 - 2;
                uVar7 = *puVar2;
                bVar5 = (uint8_t)(uVar7 >> 8);
                if ((bVar5 == 0) || ((bVar5 & 0x80) != 0)) {
                    puVar2 = puVar2 - 2;
                    uVar1 = *puVar2;
                    *puVar2 = ((uint16_t)(uVar1 >> 8) << 16) | 0x9b90;
                }
            }
        } else if ((param_1 & 0x40) != 0) {
            puVar2 = puVar2 - 2;
            uVar1 = *puVar2;
            *puVar2 = ((uint16_t)(uVar1 >> 8) << 16) | 0x9b;
        }
    }
    return;
}