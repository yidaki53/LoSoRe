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
#include <stdbool.h>
#include <math.h>

void FUN_24dd_351a(void) {
    code *pcVar1;
    uint8_t uVar2;
    uint8_t bVar3;
    int iVar4;
    uint8_t *pbVar5;
    int in_CX;
    uint8_t *puVar6;
    uint16_t uVar7;
    uint16_t in_BX;
    uint8_t *unaff_DI;
    uint16_t unaff_ES;
    uint16_t unaff_DS;
    bool bVar8;
    char cVar9;
    char cVar10;
    char cVar11;
    long double in_ST0;
    uint32_t uVar12;
    uint8_t *in_stack_00000000;
    uint16_t uStack_a;
    uint8_t uStack_8;
    char local_7;

    puVar6 = (uint8_t *)&stack0xfffe;
    cVar10 = (int)&stack0xfffe < 0;
    cVar9 = (int)&uStack_8 < 0;
    bVar8 = &stack0x0000 == (uint8_t *)0x8;
    pcVar1 = (code *)swi(0x35);
    (*pcVar1)();
    do {
    } while (bVar8 || cVar10 != cVar9);
    pcVar1 = (code *)swi(0x37);
    uVar12 = (*pcVar1)();
    if (in_CX != 1) {
        while (true) {
            uVar7 = (uint16_t)((uint32_t)uVar12 >> 16) & 0xff;
            *(int *)unaff_DI =
                ((char)((uint32_t)uVar12 % uVar7) << 8) | (char)((uint32_t)uVar12 / uVar7) + 0x3030;
            pbVar5 = unaff_DI + (2 - (int)in_stack_00000000);
            pcVar1 = (code *)swi(0x37);
            (*pcVar1)();
            if (pbVar5 == (uint8_t *)0x1) break;
            *in_stack_00000000 = 0x45;
            uVar2 = 0x2b;
            uVar7 = uStack_a;
            if ((int)uStack_a < 0) {
                uVar2 = 0x2d;
                uVar7 = -uStack_a;
            }
            in_stack_00000000[1] = uVar2;
            uVar12 = ((uint16_t)10 << 8) | (uVar7 % 100);
            uVar7 = (uint16_t)(char)(uVar7 / 100);
            unaff_DI = in_stack_00000000 + 4;
            *(int *)(in_stack_00000000 + 2) = ((char)(uVar7 % 10) << 8) | (char)(uVar7 / 10) + 0x3030;
        }
        pcVar1 = (code *)swi(0x3d);
        (*pcVar1)();
        return;
    }
    *(long *)(in_stack_00000000 +
              ((char)((uint16_t)in_BX >> 8) + (char)((uint32_t)uVar12 >> 24)) * 16 + 0x3b) =
        (long)round(in_ST0);
    *(int *)(in_stack_00000000 + 0x44) = *(int *)(in_stack_00000000 + 0x44) << 3;
    bVar3 = *unaff_DI;
code_r0x00028336:
    bVar8 = bVar3 < 0x45;
    if ((bVar3 != 0x45) && (bVar8 = bVar3 < 0x65, bVar3 != 0x65)) goto LAB_24dd_358a;
    puVar6 = puVar6 + -1;
    uVar12 = FUN_24dd_4732();
    if (bVar8) goto LAB_2