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

void __stdcall16far FUN_24dd_3b5d(uint16_t param_1, uint16_t *param_2) {
    uint16_t *puVar3;
    uint16_t uVar2;
    uint16_t uVar4;
    bool bVar5;
    uint16_t in_stack_00000000;

    uVar4 = (uint16_t)((uintptr_t)param_2 >> 16);
    puVar3 = (uint16_t *)param_2;
    if (puVar3[1] != 0xd7b3) {
        if (puVar3[1] != 0xd7b0) {
            *(uint16_t *)0x6410 = 0x66;
            return;
        }
        FUN_24dd_3bde(puVar3, uVar4);
    }
    uVar2 = 0;
    if (*(char *)(puVar3 + 0x18) != '\0') {
        bVar5 = false;
        // Assuming swi(0x21) is a software interrupt call, which is not directly translatable to C.
        // This part needs to be replaced with the actual system call or function call equivalent.
        // For demonstration, let's assume it's a function call.
        uVar2 = some_system_call();
        if (bVar5) {
            *(uint16_t *)0x6410 = uVar2;
            return;
        }
    }
    puVar3[1] = 0xd7b3;
    *param_2 = uVar2;
    puVar3[2] = param_1;
    return;
}