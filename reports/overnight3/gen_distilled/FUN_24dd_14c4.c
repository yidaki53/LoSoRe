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

void FUN_24dd_04f8(void);
void FUN_24dd_1519(void);
void FUN_24dd_1277(int, uint16_t, int);
void FUN_24dd_13e2(int, uint16_t, int);
void FUN_24dd_1551(void);
void FUN_24dd_1588(void);

void FUN_24dd_14c4(void) {
    uint16_t uVar1;
    uint16_t *base_address = (uint16_t *)0xd8;
    int *int_ptr = (int *)0x804a054;

    if (-0x3fff < *int_ptr) {
        if (0x3fff < *int_ptr) {
            if (*(char *)(int_ptr + 1) == '\0') {
                FUN_24dd_04f8();
                FUN_24dd_1519();
                uVar1 = *base_address;
                FUN_24dd_1277(0x804a054, uVar1, 0x804a058);
                FUN_24dd_13e2(0x804a054, uVar1, 0x804a05c);
                FUN_24dd_1551();
                FUN_24dd_1588();
                *int_ptr = *int_ptr - 1;
                *base_address = *base_address + 0xc;
                return;
            }
            FUN_24dd_1551();
            FUN_24dd_1588();
            *int_ptr = *int_ptr - 1;
            *base_address = *base_address + 0xc;
            return;
        }
        FUN_24dd_1551();
        FUN_24dd_1588();
        *int_ptr = *int_ptr - 1;
        *base_address = *base_address + 0xc;
        return;
    }
    FUN_24dd_1551();
    FUN_24dd_1588();
    *int_ptr = *int_ptr - 1;
    *base_address = *base_address + 0xc;
    return;
}