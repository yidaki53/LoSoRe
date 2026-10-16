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

extern uint16_t DAT_640e; // Assuming this is the base address for the segment

uint16_t __cdecl16far FUN_24dd_0530(uint16_t param_1) {
    uint16_t uVar1;
    int16_t iVar2;

    if ((param_1 & 0x8000) != 0) {
        param_1 = -param_1;
    }

    iVar2 = (int16_t)(param_1 - DAT_640e);
    if (iVar2 < 0 || iVar2 >= 0x100) {
        return 0xca;
    }

    return param_1;
}