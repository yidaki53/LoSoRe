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

extern void FUN_24dd_492c(void);
extern void FUN_24dd_00b1(void);
extern void FUN_24dd_3639(void);
extern void FUN_24dd_36b7(void);
extern void FUN_24dd_36bc(void);

void __cdecl16far FUN_24dd_0000(void) {
    uint16_t es = __CS;
    FUN_24dd_492c();
    FUN_24dd_00b1();
    uint16_t bx = es;
    uint16_t ss = __SS;
    uint16_t sp = __SP;
    uint16_t *stack_ptr = (uint16_t *)(ss * 16 + sp);

    *(uint16_t *)0x2971640c = es;
    *(uint16_t *)0x297163de = ((uint16_t)stack_ptr >> 4) + ss;
    *(uint16_t *)0x297163e2 = *(uint16_t *)0x297163de + *(uint16_t *)0x297163d8;
    *(uint16_t *)0x297163f4 = *(uint16_t *)0x2;
    *(uint16_t *)0x297163fe = 0xd6;
    *(uint16_t *)0x29716400 = 0x24dd;
    uint16_t *ptr = (uint16_t *)0x7af0;
    int count = 0x13;

    *(uint16_t *)0x297163e0 = *(uint16_t *)0x297163de;
    *(uint16_t *)0x297163ec = *(uint16_t *)0x297163e2;
    *(uint16_t *)0x297163f0 = *(uint16_t *)0x297163e2;
    *(uint16_t *)0x297163f8 = *(uint16_t *)0x297163e2;

    while (count != 0) {
        // Simulate swi(0x21) by calling a function pointer
        void (*int21_handler)(void) = (void (*)(void))(*(uint16_t *)0x21 * 16 + *(uint16_t *)0x23);
        int21_handler();
        *ptr = bx;
        ptr[1] = *(uint16_t *)0x2971640c;
        ptr += 2;
        count--;
    }

    // Simulate swi(0x21) by calling a function pointer
    int21_handler();
    int21_handler();
    int21_handler();
    int21_handler();
    int21_handler();

    FUN_24dd_3639();
    FUN_24dd_36b7();
    FUN_24dd_3639();
    FUN_24dd_36bc();
}