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

void __stdcall16far FUN_24dd_3711(void *param_1) {
    int *piVar1;
    int iVar2;
    void (*func_ptr)(int) = (void (*)(int))0x24dd_371d;

    if (*(char *)(*(int *)param_1 + 2) == -0x7b1 || *(char *)(*(int *)param_1 + 2) == -0x7b2)) {
        *(char *)0x6410 = 0x67;
        func_ptr(0x14);
        func_ptr(0x1c);
        *(int *)(*(int *)param_1 + 2) = -0x7b0;
    } else {
        do {
            if (*(char *)0x0 == '\0') break;
            iVar2 = 0x1c;
            func_ptr(iVar2);
        } while (true);
    }
    return;
}