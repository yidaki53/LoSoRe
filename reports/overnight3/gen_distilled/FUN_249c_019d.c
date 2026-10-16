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

extern uint8_t __far FUN_249c_019d(uint8_t param_1) {
    uint8_t uVar1;
    uint8_t *ptr1 = (uint8_t *)(0x159c);
    uint8_t *ptr2 = (uint8_t *)(0x159c);

    uVar1 = in(0x21);
    if (*ptr1 == '\0') {
        if (param_1 == 3) {
            out(0x23);
        }
    } else if (param_1 == 4) {
        uVar1 = in(0x21);
    }

    return uVar1;
}