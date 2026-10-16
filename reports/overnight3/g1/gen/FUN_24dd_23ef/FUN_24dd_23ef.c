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

void FUN_24dd_23ef(void) {
    uint32_t lVar1;
    uint32_t uVar2;
    uint32_t lVar3;
    uint32_t uVar4;
    int iVar5;
    uint32_t uVar6;
    uint32_t uVar7;
    uint32_t uVar8;
    uint32_t uVar9;
    char cVar10;
    uint32_t uVar11;
    int si;
    uint32_t *di;
    uint32_t uVar12;
    uint16_t es;
    uint16_t ds;
    uint8_t bVar13;
    uint32_t uVar14;

    // Assuming si and di are passed as function parameters
    // si = unaff_SI;
    // di = unaff_DI;

    di[5] = (uint32_t)(*(char *)(si + 9) < '\0');
    iVar5 = (uint32_t)*(uint8_t *)(si + 8) << 4;
    uVar9 = (uint32_t)(uint8_t)(((uint8_t)iVar5 >> 4) + (char)((uint32_t)iVar5 >> 8) * '\n') * 10000;
    uVar14 = FUN_24dd_23c0();
    cVar10 = (char)((uint64_t)uVar14 >> 0x18);
    lVar1 = (uint64_t)((uint32_t)uVar14 + uVar9) * 10000;
    uVar6 = (uint32_t)lVar1;
    uVar8 = (uint32_t)((uint64_t)lVar1 >> 0x10) +
            (((uint16_t)cVar10 << 8) | ((char)((uint64_t)uVar14 >> 0x10) + cVar10 + ((uint32_t)uVar14 + uVar9 < uVar9))) *
            10000;
    uVar14 = FUN_24dd_23c0();
    uVar9 = (uint32_t)((uint32_t)uVar14 + uVar6 < uVar6);
    cVar10 = (char)((uint64_t)uVar14 >> 0x18);
    lVar1 = (uint64_t)((uint32_t)uVar14 + uVar6) * 10000;
    uVar6 = (uint32_t)lVar1;
    lVar3 = (uint64_t)(uVar8 + uVar9) * 10000 +
            (((uint16_t)cVar10 << 8) | ((char)((uint64_t)uVar14 >> 0x10) + cVar10 + ((uint32_t)uVar8 + uVar9 < uVar9))) *
            10000 + (uint32_t)((uint64_t)lVar1 >> 0x10);
    uVar11 = (uint32_t)lVar3;
    uVar14 = FUN_24dd_23c0();
    uVar8 = (uint32_t)((uint64_t)uVar14 >> 0x10);
    uVar9 = (uint32_t)((uint32_t)uVar14 + uVar6 < uVar6);
    lVar1 = (uint64_t)((uint32_t)uVar14 + uVar6) * 10000;
    uVar7 = (uint32_t)lVar1;
    lVar1 = (uint64_t)(uVar11 + uVar8 + uVar9) * 10000 +
            (((int)((uint64_t)lVar3 >> 0x10) + uVar8 +
              ((uint32_t)uVar11 + uVar8 < uVar11) || ((uint32_t)uVar11 + uVar8 + uVar9 < uVar11 + uVar8))) *
            10000 + (uint32_t)((uint64_t)lVar1 >> 0x10);
    uVar11 = (uint32_t)lVar1;
    uVar12 = (uint32_t)((uint64_t)lVar