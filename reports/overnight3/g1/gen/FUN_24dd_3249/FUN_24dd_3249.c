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

uint16_t FUN_24dd_3249(void) {
    uint16_t uVar4;
    uint16_t uVar8;
    uint16_t *in_BX;
    uint16_t in_CX;
    uint16_t in_stack_00000001;
    uint16_t uStack_3;
    uint16_t uStack_1;
    uint16_t in_stack_00000000;
    uint16_t in_AF;
    uint16_t in_CF;
    uint16_t bVar7;
    uint16_t bVar5;
    uint16_t cVar2;
    uint16_t iVar6;
    uint16_t uVar9;
    uint16_t uVar10;
    uint16_t *puVar3;
    uint16_t *pcVar1;

    // Simulate swi(0x35) and (*pcVar1)()
    pcVar1 = (uint16_t *)0x35;
    uVar8 = *pcVar1;

    puVar3 = &uStack_1;
    iVar6 = (uint16_t)(uVar8 >> 8);

    if ((__builtin_popcount((uint16_t)puVar3 & 0xff) & 1) == 0) {
        *in_BX = *in_BX >> 13;
        in_AF = 9 < ((uint8_t)uVar8 & 0xf) | in_AF;
        in_stack_00000001 = (uint16_t)((uint16_t)in_stack_00000001 | (uint16_t)0x0000);
        uVar4 = (uint16_t)(((uint8_t)(uVar8 >> 8) + in_AF) & 0xff0f) + 1;
        bVar7 = (__builtin_popcount((uint16_t)uVar4 & 0xff) & 1) == 0;
        while (true) {
            if (!bVar7) {
                uVar8 = (uint16_t)((uint16_t)iVar6 | (uint16_t)((uint8_t)uVar4 % 0));
                goto code_r0x00027ff2;
            }
            if (__builtin_popcount((uint16_t)&uStack_3 & 0xff) != 0) break;
            if ((__builtin_popcount((uint16_t)(uVar4 + 1) & 0xff) & 1) != 0) {
                pcVar1 = (uint16_t *)0x3c;
                *pcVar1 = *pcVar1;
                pcVar1 = (uint16_t *)0x3d;
                uVar4 = *pcVar1;
                return uVar4;
            }
            if ((__builtin_popcount((uint16_t)(iVar6 + 1) & 0xff) & 1) != 0) {
                return uVar4 + 1;
            }
            pcVar1 = (uint16_t *)0x37;
            uVar9 = *pcVar1;
            uVar4 = (uint16_t)uVar9 + 1;
            uVar10 = (uint16_t)((uint16_t)((uint16_t)uVar9 >> 8) | (uint16_t)uVar4);
            if ((__builtin_popcount((uint16_t)uVar4 & 0xff) & 1) != 0) {
                // halt_baddata();
                return 0; // Placeholder for halt_baddata
            }
            if ((__builtin_popcount((uint16_t)((uint16_t)uVar9 + 0xbf60) & 0xff) & 1) != 0) {
                pcVar1 = (uint16_t *)0x35;
                uVar10 = *pcVar1;
                out((uint16_t)((uint16_t)uVar10 >> 8), (uint8_t)uVar10);
                return (uint16_t)uVar10;
            }
            in_stack_00000001 = (uint16_t)((uint16_t)0x0000 | (uint16_t)in_stack_00000001);
            while (true) {
                uVar4 = (uint16_t)((uint16_t)((uint16_t)uVar10 >>