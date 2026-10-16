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

extern void FUN_24dd_0530(void);
extern uint16_t FUN_1000_0d70(uint16_t, uint16_t, int, int);
extern uint16_t FUN_24dd_4161(void);
extern void FUN_24dd_3e7c(void);
extern int FUN_24dd_3dbd(void);
extern uint32_t FUN_202c_0000(int, int, int, int, int, int, int, int);
extern void FUN_202c_165d(uint32_t, uint16_t, uint16_t, uint16_t, uint16_t, uint16_t, uint16_t, uint8_t, uint16_t);
extern uint32_t FUN_24dd_4654(uint16_t);

void __cdecl16near FUN_1000_8c03(void) {
    uint32_t base = *(uint32_t *)0x6670;
    uint16_t local_4 = 0x1000;
    uint16_t local_6 = 0;

    FUN_24dd_0530();

    while (true) {
        if (*(char *)(base + local_6 * 0xaa + 0x9c) != '\0') {
            uint32_t uVar22 = ((uint16_t)(base >> 16) << 16) | (base + local_6 * 0xaa);
            uint32_t uVar3 = *(uint32_t *)(base + local_6 * 0xaa + 0x16);
            int iVar10 = *(int *)(base + local_6 * 0xaa + 0x18);
            uint32_t *puVar1 = (uint32_t *)(base + local_6 * 0xaa + 0xe);
            uint32_t uVar7 = *puVar1;
            *puVar1 = *puVar1 + uVar3;
            *(int *)(base + local_6 * 0xaa + 0x10) = *(int *)(base + local_6 * 0xaa + 0x10) + iVar10 + (uint)(uVar7 + uVar3 > 0xffff);
            uVar3 = *(uint32_t *)(base + local_6 * 0xaa + 0x1a);
            iVar10 = *(int *)(base + local_6 * 0xaa + 0x1c);
            puVar1 = (uint32_t *)(base + local_6 * 0xaa + 0x12);
            uVar7 = *puVar1;
            *puVar1 = *puVar1 + uVar3;
            *(int *)(base + local_6 * 0xaa + 0x14) = *(int *)(base + local_6 * 0xaa + 0x14) + iVar10 + (uint)(uVar7 + uVar3 > 0xffff);
            uint8_t uVar5 = FUN_1000_0d70(*(uint16_t *)(base + local_6 * 0xaa + 0x14), *(uint16_t *)(base + local_6 * 0xaa + 0x10), 1, local_6 ^ 1);
            *(uint8_t *)(uVar22 + 0xd) = uVar5;

            int iVar10 = 0x20;
            uint8_t bVar6 = FUN_24dd_4161();
            int iVar11 = uVar22;
            uint16_t uVar13 = (uint16_t)(uVar22 >> 16);

            if (((((*(uint8_t *)(iVar10 + 0x6604) & bVar6) == 0) && (0 < *(int *)(iVar11 + 0x10))) &&
                 (*(int *)(iVar11 + 0x10) < 0x1f7)) &&
                ((0 < *(int *)(iVar11 + 0x14) && (*(int *)(iVar11 + 0x14) < 0x15d)))) {
                if (*(char *)(iVar11 + 0xd) == '\0') {
                    *(uint8_t *)(iVar11 + 0xc) = 0;
                } else {
                    local_4 = local_6 ^ 1;
                    uint16_t u