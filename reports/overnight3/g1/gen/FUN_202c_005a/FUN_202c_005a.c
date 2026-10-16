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

void __stdcall16far FUN_202c_005a(char param_1, uint32_t param_2, uint32_t param_3, int param_4, int param_5) {
    char cVar1;
    uint32_t uVar2;
    uint8_t bVar3;
    uint32_t uVar4;
    uint32_t uVar5;
    int iVar6;
    uint16_t uVar7;
    uint16_t uVar8;
    int local_a;
    int local_8;
    uint16_t uVar8;

    uVar7 = (uint16_t)(param_3 >> 16);
    uVar8 = (uint16_t)(param_2 >> 16);
    if (param_1 == '\0') {
        for (local_a = 0; uVar4 = local_a + param_4, (int)uVar4 < 0x15d; local_a = local_a + 1) {
            if (uVar4 < 0x8000) {
                local_8 = 0;
                while (true) {
                    uVar5 = local_8 + param_5;
                    if ((uVar5 < 0x8000) && ((int)uVar5 < 0x1f8)) {
                        cVar1 = *(char *)((int)param_3 + local_a * 0x10 + local_8);
                        if ((cVar1 == '\n') || (cVar1 == '\x06')) {
                            iVar6 = 0x20;
                            bVar3 = FUN_24dd_4161();
                            if ((*(uint8_t *)(iVar6 + 0x14c0) & bVar3) != 0) {
                                uVar2 = *(uint32_t *)((int)*(uint32_t *)0x6674 + uVar4 * 4);
                                *(uint8_t *)((int)uVar2 + uVar5) =
                                    *(uint8_t *)((int)param_2 + (uVar4 & 0xf) * 0x10 + (uVar5 & 0xf));
                            }
                        } else if (cVar1 == '\x02') {
                            iVar6 = 0x20;
                            bVar3 = FUN_24dd_4161();
                            if ((*(uint8_t *)(iVar6 + 0x14c0) & bVar3) != 0) {
                                uVar2 = *(uint32_t *)((int)*(uint32_t *)0x6674 + uVar4 * 4);
                                *(uint8_t *)((int)uVar2 + uVar5) = 2;
                            }
                        } else if (cVar1 == '\x01') {
                            iVar6 = 0x20;
                            bVar3 = FUN_24dd_4161();
                            if ((*(uint8_t *)(iVar6 + 0x14c0) & bVar3) != 0) {
                                uVar2 = *(uint32_t *)((int)*(uint32_t *)0x6674 + uVar4 * 4);
                                *(uint8_t *)((int)uVar2 + uVar5) = 1;
                            }
                        }
                    }
                    if (local_8 == 0xf) break;
                    local_8 = local_8 + 1;
                }
            }
            if (local_a == 0xf) {
                return;
            }
        }
    } else {
        for (local_a = 0; uVar4 = local_a + param_4, (int)uVar4 < 0x15d; local_a = local_a + 1) {
            if (uVar4 < 0x8000) {
                local_8 = 0;
                while (true) {
                    uVar5 = local_8 + param_5;
                    if ((uVar5 < 0x8000) && ((int)uVar5 < 0x1f8)) {
                        cVar1 = *(char *)((int)param_3 + local_a * 0x10 + local_8);
                        if (cVar1 == '\x06') {
                            iVar6 = 0x20;
                            bVar3 = FUN_24dd_4161();
                            if ((*(uint8_t *)(iVar6 + 0x6624) & bVar3) != 0) {
                                uVar2 = *(uint3