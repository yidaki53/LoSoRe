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

void FUN_24dd_0530();
uint8_t FUN_24dd_4161();
char FUN_24dd_4654(int);

void FUN_1000_5c36(int param_1) {
    uint32_t *puVar1;
    uint32_t uVar2;
    uint32_t uVar3;
    uint32_t uVar4;
    uint8_t bVar5;
    char cVar6;
    int iVar7;
    char *pcVar8;
    uint16_t uVar9;
    uint16_t ds = *(uint16_t *)0x6690 >> 16;
    pcVar8 = (char *)((*(uint32_t *)0x6690 + param_1 * 0x11) & 0xFFFF);
    char *local_6 = (char *)(((uint32_t)ds << 16) | (uint32_t)pcVar8);
    uVar3 = *(uint32_t *)(pcVar8 + 9);
    iVar7 = *(int *)(pcVar8 + 0xb);
    puVar1 = (uint32_t *)(pcVar8 + 1);
    uVar2 = *puVar1;
    *puVar1 = *puVar1 + uVar3;
    *(uint32_t *)(pcVar8 + 3) = *(int *)(pcVar8 + 3) + iVar7 + (uVar2 + uVar3 < uVar2);
    uVar3 = *(uint32_t *)(pcVar8 + 0xd);
    iVar7 = *(int *)(pcVar8 + 0xf);
    puVar1 = (uint32_t *)(pcVar8 + 5);
    uVar2 = *puVar1;
    *puVar1 = *puVar1 + uVar3;
    *(uint32_t *)(pcVar8 + 7) = *(int *)(pcVar8 + 7) + iVar7 + (uVar2 + uVar3 < uVar2);
    if (((*(int *)(pcVar8 + 3) < 0) || (0x1f7 < *(int *)(pcVar8 + 3))) || (*(int *)(pcVar8 + 7) < 0) || (0x15d < *(int *)(pcVar8 + 7))) {
        *local_6 = '\0';
    }
    if (*local_6 != '\0') {
        iVar7 = 0x20;
        bVar5 = FUN_24dd_4161();
        if ((*(uint8_t *)(iVar7 + 0x14c0) & bVar5) != 0) {
            puVar1 = (uint32_t *)(pcVar8 + 0xd);
            uVar2 = *puVar1;
            *puVar1 = *puVar1 + 1000;
            *(uint32_t *)(pcVar8 + 0xf) = *(int *)(pcVar8 + 0xf) + (0xfc17 < uVar2);
        }
        uVar4 = *(uint32_t *)((*(uint32_t *)0x6674 + *(int *)(pcVar8 + 7) * 4) & 0xFFFF);
        bVar5 = *(uint8_t *)((uint32_t)uVar4 + *(int *)(pcVar8 + 3));
        if ((bVar5 == 0) || ((2 < bVar5 && ((bVar5 < 0x4d || (0x4f < bVar5)))))) {
            if (*(int *)(pcVar8 + 7) < 0x15e) {
                iVar7 = 0x20;
                bVar5 = FUN_24dd_4161();
                if ((*(uint8_t *)(iVar7 + 0x6624) & bVar5) == 0) {
                    iVar7 = 0x20;
                    bVar5 = FUN_24dd_4161();
                    if ((*(uint8_t *)(iVar7 + 0x14a0) & bVar5) != 0) {
                        cVar6 = FUN_24dd_4654(3);
                        uVar4 = *(uint32_t *)((*(uint32_t *)0x6674 + *(int *)(pcVar8 + 7) * 4) & 0xFFFF);
                        *(char *)((uint32_t)uVar4 + *(int *)(pcVar8 +