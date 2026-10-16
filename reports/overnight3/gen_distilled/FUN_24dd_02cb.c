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

void __stdcall16far FUN_24dd_02cb(void *param_1) {
    void *unaff_ES = *(void **)0x0; // Assuming unaff_ES is initialized to some valid memory location.
    void *unaff_DS = *(void **)0x1; // Assuming unaff_DS is initialized to some valid memory location.

    *(void **)0x63ee = param_1;
    *(void **)0x63f0 = unaff_ES;
    *(void **)0x63f6 = param_1;
    *(void **)0x63f8 = unaff_DS;
}