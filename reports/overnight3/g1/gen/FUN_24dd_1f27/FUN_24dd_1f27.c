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

void FUN_24dd_0582(void);
void FUN_24dd_0ee2(int, int, int);
void FUN_24dd_1277(int, int, int);
void FUN_24dd_0673(void);
void FUN_24dd_17d1(void);
void FUN_24dd_18d9(uint16_t, uint16_t);
void FUN_24dd_10a7(int, int, uint16_t);

void FUN_24dd_1f27(void) {
    int iVar1;
    int si;
    uint16_t ds;

    // Assuming si and ds are set somewhere else in the code
    // For the sake of this example, let's assume they are set to some values
    si = 0x1234; // Example value
    ds = 0x24dd; // Example value

    if (-0x40 < *(int *)(ds * 16 + si + 8)) {
        *(int *)0xd8 = *(int *)0xd8 + -0xc;
        iVar1 = *(int *)0xd8;
        FUN_24dd_0582();
        *(int *)(iVar1 + 8) = *(int *)(iVar1 + 8) + 1;
        FUN_24dd_0ee2(iVar1, iVar1, si);
        FUN_24dd_1277(iVar1, iVar1, si);
        FUN_24dd_0673();
        *(int *)(*(int *)0xd8 + 8) = *(int *)(*(int *)0xd8 + 8) + 2;
        FUN_24dd_17d1();
        FUN_24dd_18d9(0x1dcb, uRam00021dc9);
        FUN_24dd_10a7(si, iVar1, *(uint16_t *)0xd8);
        *(int *)(si + 8) = *(int *)(si + 8) + 1;
        *(int *)0xd8 = *(int *)0xd8 + 0x18;
    }
    return;
}