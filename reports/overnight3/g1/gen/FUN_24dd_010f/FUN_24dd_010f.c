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

extern void FUN_24dd_3711(void);
extern void FUN_24dd_01f0(void);
extern void FUN_24dd_01fe(void);
extern void FUN_24dd_0218(void);
extern void FUN_24dd_0232(void);

void __cdecl16far FUN_24dd_010f(uint16_t ax, uint32_t stack_00000000, uint32_t stack_00000002) {
    uint16_t *ptr_10 = (uint16_t *)0x10;
    uint16_t *ptr_14 = (uint16_t *)0x14;
    uint16_t *ptr_8 = (uint16_t *)0x8;
    uint16_t *ptr_2971_6406 = (uint16_t *)0x2971_6406;
    uint16_t *ptr_2971_6408 = (uint16_t *)0x2971_6408;
    uint16_t *ptr_2971_640a = (uint16_t *)0x2971_640a;
    uint16_t *ptr_2971_640c = (uint16_t *)0x2971_640c;
    uint16_t *ptr_2971_6402 = (uint16_t *)0x2971_6402;
    uint16_t *ptr_2971_6410 = (uint16_t *)0x2971_6410;

    *ptr_2971_6406 = ax;
    uint16_t uVar2 = *ptr_2971_6406;
    *ptr_2971_6408 = (uint16_t)stack_00000000;
    if (stack_00000000 != 0 || stack_00000002 != 0) {
        for (; (uVar2 != 0 &&
               ((((stack_00000002 = *ptr_10, stack_00000002 == 0 ||
                  (int16_t)(stack_00000002 - stack_00000002) != 0)) ||
                 (0xfff < (uint16_t)-(int16_t)(stack_00000002 - stack_00000002))) ||
                ((stack_00000000 = (int16_t)(stack_00000002 - stack_00000002) * -0x10 + stack_00000000,
                 (int16_t)(stack_00000002 - stack_00000002) * -0x10 + stack_00000000 < 0 ||
                 (uVar2 = uVar2, *ptr_8 <= stack_00000000)))))); uVar2 = *ptr_14) {
        }
        stack_00000002 = (uint16_t)((stack_00000002 - *ptr_2971_640c) - 0x10);
    }
    *ptr_2971_640a = (uint16_t)stack_00000002;
    char *pcVar5 = (char *)*ptr_2971_6402;
    if ((int)((uint32_t)*ptr_2971_6402 >> 0x10) == 0 && pcVar5 == (char *)0x0) {
        FUN_24dd_3711();
        FUN_24dd_3711();
        int iVar3 = 0x13;
        do {
            // Assuming swi(0x21) is a BIOS interrupt call, which is not directly translatable to C.
            // This part is left as a placeholder.
            iVar3 = iVar3 + -1;
        } while (iVar3 != 0);
        if (*ptr