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

void FUN_249c_0180(void) {
    uint16_t bp;
    uint8_t al;
    uint8_t ah;
    uint8_t temp;

    bp = *(uint16_t *)(&bp - 1); // Simulate ENTER instruction
    bp -= 2;

    ah = 0xb;
    __asm__("int $0x21" : "=a"(al) : "a"(ah)); // Simulate INT 0x21
    *(uint8_t *)(bp + 0xfffe) = al;

    if (*(uint8_t *)(bp - 2) != 0xff) {
        al = 0x0;
        goto L4b55;
    }

    al++;
    *(uint8_t *)(bp - 1) = al;
    al = *(uint8_t *)(bp - 1);

L4b55:
    bp += 2; // Simulate LEAVE instruction
    __asm__("retf"); // Simulate RETF instruction
}