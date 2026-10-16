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

extern char FUN_24dd_4654(int);
extern void FUN_202c_032d(int, int, int, int, int);

void FUN_202c_0bc0(void) {
    uint16_t uVar2;
    uint32_t uVar3;
    uint32_t uVar4;
    uint32_t uVar5;
    char cVar6;
    int iVar7;
    int iVar8;
    int iVar9;
    int iVar10;
    int local_e;
    int local_c;
    int local_6;
    int local_4;

    uVar2 = *(uint16_t *)(0x6602);
    *(uint16_t *)(0x6412) = *(uint16_t *)(0x6600);
    *(uint16_t *)(0x6414) = uVar2;
    cVar6 = FUN_24dd_4654(7);
    **(char **)(0x6674) = cVar6 + '\f';
    local_4 = 1;
    while (true) {
        iVar7 = FUN_24dd_4654(7);
        *(char *)(*(uint32_t *)(0x6674) + local_4 * 4) =
            (char)((uint)*(uint8_t *)(*(uint32_t *)(0x6674) + (local_4 - 1) * 4) +
                   iVar7 + 0xc >> 1);
        if (local_4 == 0x15d) break;
        local_4 = local_4 + 1;
    }
    local_4 = 1;
    while (true) {
        iVar7 = FUN_24dd_4654(7);
        *(uint8_t *)(*(uint32_t *)(*(uint32_t *)(0x6674)) + local_4) =
            (char)((uint)*(uint8_t *)(*(uint32_t *)(*(uint32_t *)(0x6674)) + local_4 - 1) + iVar7 +
                   0xc >> 1);
        if (local_4 == 0x1f7) break;
        local_4 = local_4 + 1;
    }
    local_4 = 1;
    while (true) {
        local_6 = 1;
        while (true) {
            iVar7 = FUN_24dd_4654(8);
            uVar3 = *(uint32_t *)(*(uint32_t *)(0x6674) + local_4 * 4);
            uVar4 = *(uint32_t *)(*(uint32_t *)(0x6674) + (local_4 - 1) * 4);
            uVar5 = *(uint32_t *)(*(uint32_t *)(0x6674) + local_4 * 4);
            *(uint8_t *)(uVar5 + local_6) =
                (char)((uint)*(uint8_t *)(uVar4 + local_6) +
                       (uint)*(uint8_t *)(uVar3 + local_6 - 1) + iVar7 + 0xc) / 3);
            if (local_6 == 0x1f7) break;
            local_6 = local_6 + 1;
        }
        if (local_4 == 0x15d) break;
        local_4 = local_4 + 1;
    }
    iVar7 = FUN_24dd_4654(100);
    if (0 < iVar7) {
        local_4 = 1;
        while (true) {
            iVar8 = FUN_24dd_4654(0x1f8);
            iVar8 = iVar8 + -8;
            iVar9 = FUN_24dd_4654(0x15e);
            iVar9 = iVar9 + -8;
            iVar10 = FUN_24dd_4654(4);
            iVar10 = iVar10 + 0x45;
            local_c = 0;
            while (true) {
                local_e = 0;
                while (true) {
                    if ((((*(char *)((int)*(uint32_t *)(0x6678) + iVar10 * 0x100 + local_e * 0x10 + local_c)
                           != '\0') && ((uint)(iVar8 + local_c) < 0x800