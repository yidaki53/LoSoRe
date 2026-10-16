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

extern void FUN_24dd_0582(void);
extern void FUN_24dd_0ee2(int, uint16_t, uint16_t);
extern void FUN_24dd_1277(int, uint16_t, uint16_t);
extern void FUN_24dd_1371(void);
extern void FUN_24dd_1468(void);
extern void FUN_24dd_1563(void);
extern void FUN_24dd_1651(void);
extern void FUN_24dd_1749(void);
extern void FUN_24dd_1847(void);
extern void FUN_24dd_1935(void);
extern void FUN_24dd_1a33(void);
extern void FUN_24dd_1b30(void);
extern void FUN_24dd_1c28(void);
extern void FUN_24dd_1d26(void);
extern void FUN_24dd_1e24(void);
extern void FUN_24dd_1f27(void) {
    int *piVar1;
    uint16_t uVar2;
    uint16_t *puVar3;
    int *piVar4;
    uint16_t uVar5;
    int iVar6;
    int iVar7;
    uint16_t uVar8;
    int *piVar9;
    uint16_t uVar10;

    uVar10 = *(uint16_t *)0xd8;
    iVar6 = *(int *)(*(uint16_t *)0xd8 + 8);
    if (iVar6 < -0x40) {
        *(uint16_t *)0xd8 = uVar10 - 0xc;
        FUN_24dd_0582();
        uVar5 = *(uint16_t *)0xd8;
        puVar3 = (uint16_t *)0x0;
        while (true) {
            uVar8 = uVar10;
            uVar10 = uVar10 + 1;
            if (puVar3 != 0) break;
            puVar3 = (uint16_t *)*(uint16_t *)0x1dc9;
        }
        iVar7 = 0;
        while (true) {
            piVar9 = (int *)*(uint16_t *)0x1dc9;
            uVar2 = *(uint16_t *)0xd8;
            FUN_24dd_0ee2(iVar7, uVar2, uVar10);
            FUN_24dd_1277(iVar7, uVar2, uVar10);
            FUN_24dd_1371();
            FUN_24dd_1468();
            FUN_24dd_1563();
            FUN_24dd_1651();
            FUN_24dd_1749();
            FUN_24dd_1847();
            FUN_24dd_1935();
            FUN_24dd_1a33();
            FUN_24dd_1b30();
            FUN_24dd_1c28();
            FUN_24dd_1d26();
            FUN_24dd_1e24();
            piVar4 = piVar9;
            iVar7 = iVar7 + 1;
            if (piVar4 != 0) break;
        }
        *(int *)(*(uint16_t *)0xd8 + 8) = iVar6 + 1;
        *(uint16_t *)0xd8 = uVar10;
        return;
    }
    *(uint16_t *)0xd8 = uVar10;
    return;
}