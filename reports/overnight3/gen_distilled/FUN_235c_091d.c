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

void FUN_235c_091d(uint8_t param_1) {
    uint16_t uVar1;
    uint16_t *ptr1;
    uint16_t *ptr2;

    uVar1 = (uint16_t)param_1 * 10;
    ptr1 = (uint16_t *)((int16_t)uVar1 + 0x67fc);
    ptr2 = (uint16_t *)((int16_t)uVar1 + 0x6804);

    *ptr1 = 0;
    *ptr2 = 0;
    *(uint16_t *)(uVar1 + 0x6808) = 0;
    *(uint16_t *)(uVar1 + 0x6809) = 0;
    *(uint16_t *)(uVar1 + 0x680b) = 0;
    *(uint16_t *)(uVar1 + 0x680d) = 0;
    *(uint16_t *)(uVar1 + 0x680f) = 0;
    *(uint16_t *)(uVar1 + 0x6811) = 0;
    *(uint16_t *)(uVar1 + 0x6813) = 0;
    *(uint16_t *)(uVar1 + 0x6815) = 0;
    *(uint16_t *)(uVar1 + 0x6817) = 0;
    *(uint16_t *)(uVar1 + 0x6819) = 0;
    *(uint16_t *)(uVar1 + 0x681b) = 0;
    *(uint16_t *)(uVar1 + 0x681d) = 0;
    *(uint16_t *)(uVar1 + 0x681f) = 0;
    *(uint16_t *)(uVar1 + 0x6821) = 0;
    *(uint16_t *)(uVar1 + 0x6823) = 0;
    *(uint16_t *)(uVar1 + 0x6825) = 0;
    *(uint16_t *)(uVar1 + 0x6827) = 0;
    *(uint16_t *)(uVar1 + 0x6829) = 0;
    *(uint16_t *)(uVar1 + 0x682b) = 0;
    *(uint16_t *)(uVar1 + 0x682d) = 0;
    *(uint16_t *)(uVar1 + 0x682f) = 0;
    *(uint16_t *)(uVar1 + 0x6831) = 0;
    *(uint16_t *)(uVar1 + 0x6833) = 0;
    *(uint16_t *)(uVar1 + 0x6835) = 0;
    *(uint16_t *)(uVar1 + 0x6837) = 0;
    *(uint16_t *)(uVar1 + 0x6839) = 0;
    *(uint16_t *)(uVar1 + 0x683b) = 0;
    *(uint16_t *)(uVar1 + 0x683d) = 0;
    *(uint16_t *)(uVar1 + 0x683f) = 0;
    *(uint16_t *)(uVar1 + 0x6841) = 0;
    *(uint16_t *)(uVar1 + 0x6843) = 0;
    *(uint16_t *)(uVar1 + 0x6845) = 0;
    *(uint16_t *)(uVar1 + 0x6847) = 0;
    *(uint16_t *)(uVar1 + 0x6849) = 0;
    *(uint16_t *)(uVar1 + 0x684b) = 0;
    *(uint16_t *)(uVar1 + 0x684d) = 0;
    *(uint16_t *)(uVar1 + 0x684f) = 0;
    *(uint16_t *)(uVar1 + 0x6851) = 0;
    *(uint16_t *)(uVar1 + 0x6