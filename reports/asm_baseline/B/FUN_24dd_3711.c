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

void FUN_24dd_3711(void) {
    uint16_t local_6;
    uint16_t local_4;
    uint16_t local_2;

    local_6 = *(uint16_t *)(BP + 0x6);
    if (*(uint16_t *)(ES + local_6 + 0x2) == 0xd7b1) {
        goto LAB_2000_8509;
    }
    if (*(uint16_t *)(ES + local_6 + 0x2) == 0xd7b2) {
        goto LAB_2000_8501;
    }
    *(uint16_t *)0x6410 = 0x67;
    goto LAB_2000_8519;

LAB_2000_8519:
    return;

LAB_2000_8509:
    // Code for LAB_2000_8509
    return;

LAB_2000_8501:
    // Code for LAB_2000_8501
    return;
}