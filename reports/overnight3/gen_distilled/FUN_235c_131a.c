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

void FUN_24cb_0094(uint16_t, uint16_t, uint16_t, uint8_t);

void __cdecl16far FUN_235c_131a(void) {
    uint16_t *ptr1 = (uint16_t *)(0x67dc);
    uint8_t *ptr2 = (uint8_t *)(0x67eb);
    uint16_t *ptr3 = (uint16_t *)(0x67f2);
    uint16_t *ptr4 = (uint16_t *)(0x67f4);
    uint8_t *ptr5 = (uint8_t *)(0x67ec);
    uint8_t *ptr6 = (uint8_t *)(0x67fa);

    uint8_t bVar1 = *ptr1;
    *ptr1 = bVar1 | *ptr2;
    FUN_24cb_0094(*ptr3, *ptr4, *ptr5, *ptr6);
    *ptr6 = 0;
}