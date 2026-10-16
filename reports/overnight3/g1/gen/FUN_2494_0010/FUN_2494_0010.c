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

void FUN_2494_0010(void) {
    void (*func)(void);
    uint16_t bx;
    uint16_t es;

    // Assuming swi(0x2f) is a BIOS interrupt call, which is not directly translatable to C.
    // For demonstration purposes, let's assume it returns a function pointer.
    func = (void (*)(void))0x2f;

    func();
    *(uint16_t *)(0x7838) = bx;
    *(uint16_t *)(0x783a) = es;
}