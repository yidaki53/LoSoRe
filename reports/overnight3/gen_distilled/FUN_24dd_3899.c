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

void FUN_24dd_373c(int param1, uint16_t param2, uint16_t *param3, uint16_t param4, uint16_t param5, uint16_t param6) {
    // Implementation of FUN_24dd_373c function
}

void FUN_24dd_3899(void) {
    if (*(char *)(0x6410) == '\0') {
        if (*(char *)(*(uint16_t *)(0x0000) + 0x2) == -0x7b2) {
            int iVar1 = *(int *)(*(uint16_t *)(0x0000) + 0x4);
            int iVar2 = *(int *)(*(uint16_t *)(0x0000) + 0x8);
            if ((-(uint16_t)(iVar2) < iVar1) && (iVar1 < iVar2)) {
                uint16_t *base_address = (uint16_t *)((uint16_t)0x0000 | *(uint16_t *)(0x0000));
                uint16_t *dest = (uint16_t *)((uint16_t)0x0000 | (uint16_t)0x0000);
                uint16_t *src = (uint16_t *)((uint16_t)0x0000 | (uint16_t)0x0004);
                uint16_t uVar3 = iVar2 - iVar1;
                uint16_t uVar4 = 0;

                while (uVar3 != 0) {
                    *dest = *src;
                    dest++;
                    src++;
                    uVar3--;
                }

                uint16_t *ptr1 = (uint16_t *)((uint16_t)0x0000 | (uint16_t)0x0008);
                uint16_t *ptr2 = (uint16_t *)((uint16_t)0x0000 | (uint16_t)0x0004);

                while (*ptr1 != 0) {
                    *ptr2 = *ptr1;
                    ptr1++;
                    ptr2++;
                }

                FUN_24dd_373c(0, 0, (uint16_t *)0x0000, 0, 0, 0);
            }
        }
    } else {
        *(char *)(0x6410) = 0x69;
    }
}