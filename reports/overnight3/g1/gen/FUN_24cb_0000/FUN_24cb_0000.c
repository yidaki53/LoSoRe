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

void FUN_24cb_0000(void) {
    uint8_t *pbVar1;
    void (*pcVar2)(void);
    uint8_t bVar3;
    uint8_t *pbVar5;
    uint8_t *pbVar6;
    uint8_t *in_stack_0000000a;
    int iVar4;

    pbVar5 = in_stack_0000000a;
    pbVar6 = (uint8_t *)0xffae;
    bVar3 = *in_stack_0000000a;
    if (0x4e < bVar3) {
        bVar3 = 0x4f;
    }
    for (iVar4 = (int)bVar3; pbVar5 = pbVar5 + 1, iVar4 != 0; iVar4 = iVar4 - 1) {
        pbVar1 = pbVar6;
        pbVar6 = pbVar6 + 1;
        *pbVar1 = *pbVar5;
    }
    *pbVar6 = 0;
    pcVar2 = (void (*)(void))0x21;
    (*pcVar2)();
    pcVar2 = (void (*)(void))0x21;
    (*pcVar2)();
    FUN_24cb_0058();
    return;
}