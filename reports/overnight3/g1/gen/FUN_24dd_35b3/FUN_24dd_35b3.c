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

void FUN_24dd_35b3(void) {
    void (*func1)(void);
    uint16_t result;
    int cx;
    int bp;
    char *di;
    uint16_t es;
    uint16_t ss;

    // Assuming cx, bp, di, es, ss are set up elsewhere in the program
    // For the sake of this example, let's assume they are global variables
    extern int cx;
    extern int bp;
    extern char *di;
    extern uint16_t es;
    extern uint16_t ss;

    while (cx != 0 && (0xf5 < (uint8_t)(*di - 0x3aU))) {
        func1 = (void (*)(void))((uint16_t)es * 16 + 0x3c);
        func1();
        result = func_0x000a4d2e();
        *((uint16_t *)(bp - 4)) = result;
        func1 = (void (*)(void))((uint16_t)es * 16 + 0x3a);
        func1();
        cx--;
    }
}