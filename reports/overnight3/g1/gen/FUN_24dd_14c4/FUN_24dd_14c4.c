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
void FUN_24dd_1519(void);
void FUN_24dd_1277(uint16_t, uint16_t, uint16_t);
void FUN_24dd_0ee2(uint16_t, uint16_t, uint16_t);
void FUN_24dd_2361(void);
void FUN_24dd_05e8(void);
void FUN_24dd_0e57(void);

void FUN_24dd_14c4(uint16_t si) {
    uint16_t uVar1;
    int value = *(int *)(si + 8);

    if (-0x3fff < value && value < 0x4001) {
        if (*(char *)(si + 10) == '\0') {
            FUN_24dd_0628();
            FUN_24dd_1519();
            uVar1 = *(uint16_t *)0xd8;
            FUN_24dd_1277(si, uVar1, si);
            FUN_24dd_0ee2(si, si, uVar1);
            *(int *)(si + 8) = value - 1;
            *(int *)0xd8 = *(int *)0xd8 + 0xc;
        } else {
            FUN_24dd_2361();
            FUN_24dd_05e8();
            *(uint16_t *)(si + 8) = 0x4001;
        }
    } else {
        FUN_24dd_0e57();
    }
}