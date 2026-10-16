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

void FUN_24dd_0530(void);
char FUN_24dd_4654(uint16_t);
char FUN_1000_0961(int, uint16_t, uint16_t);
void FUN_202c_1b84(uint16_t, uint16_t, uint16_t, int);

void FUN_1000_0ac7(void) {
    char cVar1;
    int iVar2;
    uint16_t uVar3;
    int iVar4;
    uint16_t uVar5;
    uint16_t local_8;
    int local_4;

    FUN_24dd_0530();
    for (local_4 = 1;
         (*(char *)((uint16_t)*(uint32_t *)0x6698 + local_4 * 0xe + -2) != '\0' &&
         (local_4 <= (int)(uint8_t)*(uint8_t *)0x669c)); local_4++) {
    }
    if (local_4 <= (int)(uint8_t)*(uint8_t *)0x669c) {
        uVar5 = (uint16_t)((uint32_t)*(uint32_t *)0x6698 >> 0x10);
        iVar4 = (int)*(uint32_t *)0x6698 + local_4 * 0xe;
        local_8 = (uint16_t)CONCAT2(uVar5, (uint16_t)(iVar4 + -0xe));
        cVar1 = FUN_24dd_4654(2);
        *(char *)(iVar4 + -2) = cVar1 + '\x01';
        iVar2 = FUN_24dd_4654(*(uint16_t *)((uint8_t)*(uint8_t *)(iVar4 + -2) * 2 + 0x1364));
        *(int *)(iVar4 + -4) = *(int *)((uint8_t)*(uint8_t *)(iVar4 + -2) * 2 + 0x1360) + iVar2;
        if (*(char *)(iVar4 + -2) == '\x01') {
            cVar1 = FUN_24dd_4654(0x28);
            *(char *)(iVar4 + -1) = cVar1 + '\x01';
            while (*(char *)(*(uint8_t *)(iVar4 + -1) + 0x66af) == '\x02') {
                cVar1 = FUN_24dd_4654(0x28);
                *(char *)(iVar4 + -1) = cVar1 + '\x01';
            }
        }
        *(uint16_t *)(iVar4 + -8) = 0;
        *(uint16_t *)(iVar4 + -6) = 0;
        do {
            uVar3 = FUN_24dd_4654(0x1f8);
            *local_8 = uVar3;
            uVar3 = FUN_24dd_4654(0x15e);
            *(uint16_t *)(iVar4 + -10) = uVar3;
            cVar1 = FUN_1000_0961(local_4, *(uint16_t *)(iVar4 + -10), *local_8);
        } while (cVar1 == '\0');
        FUN_202c_1b84(0x24dd, *(uint16_t *)(iVar4 + -10), *local_8, 8);
    }
    return;
}