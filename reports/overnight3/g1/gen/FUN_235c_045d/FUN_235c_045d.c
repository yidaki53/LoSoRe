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

// External function declarations
void FUN_235c_0000(uint16_t param);
void out(uint16_t port, uint8_t value);

// Global variables
extern uint8_t DAT_67cd;
extern uint16_t DAT_67de;
extern uint8_t DAT_67ee;

uint8_t FUN_235c_045d(void) {
    if (DAT_67cd == '\0') {
        FUN_235c_0000(0xffd0);
        FUN_235c_0000(0xffd3);
    } else {
        FUN_235c_0000(0xffd5);
    }
    out(DAT_67de, DAT_67ee);
    return DAT_67ee;
}