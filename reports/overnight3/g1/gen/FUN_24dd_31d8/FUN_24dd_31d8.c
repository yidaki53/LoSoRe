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

void FUN_24dd_31d8(uint16_t in_AX, uint16_t in_DX) {
    uint16_t iVar3;
    uint16_t extraout_DX;
    uint8_t uVar2;
    void (*pcVar1)(uint16_t);

    if ((char)in_AX != '\0') {
        iVar3 = ((uint16_t)((uint8_t)(in_DX >> 8) & 0x80) | (in_AX & 0xff)) + 0x3f7e;
        pcVar1 = (void (*)(uint16_t))(0x3c * 16);
        (*pcVar1)(in_AX & 0xff00);
        pcVar1 = (void (*)(uint16_t))(0x3d * 16);
        (*pcVar1)(iVar3);
        return;
    }
    pcVar1 = (void (*)(uint16_t))(0x35 * 16);
    uVar2 = (*pcVar1)();
    out(extraout_DX, uVar2);
    return;
}