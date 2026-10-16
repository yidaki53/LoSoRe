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
char FUN_24dd_4654(int param_1);

void FUN_1000_0be1(uint16_t param_1, uint16_t param_2, uint16_t param_3, uint16_t param_4,
                  uint16_t param_5, uint16_t param_6) {
    char cVar1;
    int iVar2;
    uint16_t uVar3;
    uint16_t local_4;

    FUN_24dd_0530();
    for (local_4 = 0;
         (*(char *)((uint32_t)*(uint32_t *)0x6690 + local_4 * 0x11) != '\0' && (local_4 < 700));
         local_4 = local_4 + 1) {
    }
    cVar1 = FUN_24dd_4654(2);
    *(char *)((uint32_t)*(uint32_t *)0x6690 + local_4 * 0x11) = cVar1 + 'P';
    *(uint16_t *)((uint32_t)*(uint32_t *)0x6690 + local_4 * 0x11 + 3) = param_6;
    *(uint16_t *)((uint32_t)*(uint32_t *)0x6690 + local_4 * 0x11 + 7) = param_5;
    uVar3 = (uint16_t)((uint32_t)*(uint32_t *)0x6690 >> 0x10);
    iVar2 = (int)*(uint32_t *)0x6690 + local_4 * 0x11;
    *(uint16_t *)(iVar2 + 9) = param_3;
    *(uint16_t *)(iVar2 + 0xb) = param_4;
    uVar3 = (uint16_t)((uint32_t)*(uint32_t *)0x6690 >> 0x10);
    iVar2 = (int)*(uint32_t *)0x6690 + local_4 * 0x11;
    *(uint16_t *)(iVar2 + 0xd) = param_1;
    *(uint16_t *)(iVar2 + 0xf) = param_2;
    return;
}