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

void FUN_24dd_24ba(void);
void FUN_24dd_2361(void);

void __cdecl16near FUN_24dd_24d8(void) {
    uint16_t *si = (uint16_t *)0x24d8;
    uint8_t *di = (uint8_t *)0x24dd;
    uint32_t uVar2;
    bool bVar3;
    char cVar4;
    char cVar5;
    uint8_t bVar6;
    int iVar7;

    uVar2 = si[4];
    if ((int)uVar2 < 0) {
        bVar6 = 0;
    } else {
        if (((int)uVar2 < 0x3c) ||
            ((uVar2 - 0x3c == 0 || (int)uVar2 < 0x3c &&
             ((si[3] < 0xde0b ||
              ((si[3] < 0xde0c &&
               ((si[2] < 0x6b3a ||
                ((si[2] < 0x6b3b &&
                 ((si[1] < 0x763f || ((si[1] < 0x7640 && (*si < 0xfff1)))))))))))))))) {
            cVar4 = (char)(uVar2 - 0x3c) + -4;
            do {
                cVar5 = cVar4;
                cVar4 = cVar5 + '\x10';
            } while (cVar4 == '\0' || cVar5 < -0x10);
            if (cVar4 < '\x10') {
                do {
                    bVar3 = cVar5 < -1;
                    cVar5 = cVar5 + '\x01';
                } while (bVar3);
            }
            FUN_24dd_24ba();
            FUN_24dd_24ba();
            FUN_24dd_24ba();
            bVar6 = FUN_24dd_24ba();
            *di = bVar6 % 10 | bVar6 / 10 << 4;
            di++;
            goto LAB_24dd_2585;
        }
        FUN_24dd_2361();
        bVar6 = 0x99;
    }
    for (iVar7 = 9; iVar7 != 0; iVar7--) {
        *di = bVar6;
        di++;
    }
LAB_24dd_2585:
    *di = (uint8_t)si[5] >> 1 | (uint8_t)si[5] << 7;
    return;
}