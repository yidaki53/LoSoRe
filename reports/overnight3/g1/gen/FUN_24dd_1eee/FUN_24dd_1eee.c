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

void FUN_24dd_0628(void);
void FUN_24dd_1f27(void);
void FUN_24dd_0642(void);
void FUN_24dd_10a7(int, int, int);

void __cdecl16near FUN_24dd_1eee(void) {
    int iVar1;
    uint16_t si;
    uint16_t ds;

    FUN_24dd_0628();
    FUN_24dd_1f27();
    FUN_24dd_0642();
    iVar1 = *(int *)(ds * 16 + 0xd8) + 0xc;
    FUN_24dd_10a7(iVar1, iVar1, *(int *)(ds * 16 + 0xd8));
    FUN_24dd_10a7(si, si, iVar1);
    *(int *)(ds * 16 + 0xd8) = *(int *)(ds * 16 + 0xd8) + 0x18;
    return;
}