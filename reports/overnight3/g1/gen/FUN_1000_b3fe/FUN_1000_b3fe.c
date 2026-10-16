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
void FUN_24ba_00d8(void);

uint16_t FUN_1000_b3fe(void) {
    uint8_t uVar1;
    int iVar2;
    uint8_t extraout_AL;
    uint8_t extraout_AH;
    uint32_t uStack_6 = 0x10000109;

    FUN_24dd_0530();
    while (*(uint8_t *)(uStack_6 + 0x783b) = 0, (uStack_6 & 0xFFFF) != 0xab) {
        uStack_6 = ((uStack_6 >> 8) & 0xFFFF0000) | ((uStack_6 & 0xFF) + 1) << 8;
    }
    do {
        FUN_24ba_00d8();
    } while (extraout_AL == '\0');
    uStack_6 = ((uStack_6 >> 8) & 0xFFFF0000) | 0x100;
    while (true) {
        iVar2 = uStack_6 & 0xFFFF;
        if (*(uint8_t *)(iVar2 + 0x783b) != '\0') {
            uVar1 = (uStack_6 >> 16) & 0xFF;
            uStack_6 = ((uStack_6 >> 8) & 0xFFFF0000) | (uVar1 << 8) | (uStack_6 & 0xFF);
            *(uint8_t *)(iVar2 + 0x783b) = 0;
        }
        if ((uStack_6 & 0xFFFF) == 0xab) break;
        uStack_6 = ((uStack_6 >> 8) & 0xFFFF0000) | ((uStack_6 & 0xFF) + 1) << 8;
    }
    return ((uint16_t)extraout_AH << 8) | ((uStack_6 >> 8) & 0xFF);
}