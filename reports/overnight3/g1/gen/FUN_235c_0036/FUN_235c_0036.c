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

#include <stdbool.h>

extern void out(undefined2, int);
extern void FUN_249c_01c3(int);
extern char FUN_235c_001a(void);

bool FUN_235c_0036(void) {
    char cVar1;
    char local_4;

    out(*(undefined2 *)0x67d0, 1);
    FUN_249c_01c3(1);
    out(*(undefined2 *)0x67d0, 0);
    for (local_4 = 'd'; (cVar1 = FUN_235c_001a(), cVar1 != -0x56 && (local_4 != '\0'));
         local_4 = local_4 + -1) {
    }
    return local_4 != '\0';
}