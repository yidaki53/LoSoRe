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

void __stdcall16far FUN_202c_04d5(char param_1, uint32_t param_2, int param_3, int param_4) {
    uint32_t uVar1;
    uint8_t bVar2;
    uint32_t uVar3;
    uint32_t uVar4;
    int iVar5;
    int iVar6;
    int iVar7;
    uint16_t uVar8;
    int local_a;
    int local_8;

    iVar7 = (int)param_2;
    uVar8 = (uint16_t)(param_2 >> 16);
    if (param_1 == '\0') {
        for (local_a = 0; iVar5 = local_a + param_3, iVar5 < 0x15e; local_a = local_a + 1) {
            if (-1 < iVar5) {
                local_8 = 0;
                while (true) {
                    iVar6 = local_8 + param_4;
                    if (((-1 < iVar6) && (iVar6 < 0x1f8)) &&
                        (*(char *)(iVar7 + local_a * 7 + local_8) != '\0')) {
                        uVar1 = *(uint32_t *)((int)*(uint32_t *)0x6674 + iVar5 * 4);
                        *(uint8_t *)((int)uVar1 + iVar6) = *(uint8_t *)(iVar7 + local_a * 7 + local_8);
                    }
                    if (local_8 == 6) break;
                    local_8 = local_8 + 1;
                }
            }
            if (local_a == 6) {
                return;
            }
        }
    } else {
        for (local_a = 0; uVar3 = local_a + param_3, (int)uVar3 < 0x15e; local_a = local_a + 1) {
            if (uVar3 < 0x8000) {
                local_8 = 0;
                while (true) {
                    uVar4 = local_8 + param_4;
                    if (((uVar4 < 0x8000) && ((int)uVar4 < 0x1f8)) &&
                        (*(char *)(iVar7 + local_a * 7 + local_8) != '\0')) {
                        iVar5 = 0x20;
                        bVar2 = FUN_24dd_4161();
                        if ((*(uint8_t *)(iVar5 + 0x6644) & bVar2) == 0) {
                            uVar1 = *(uint32_t *)((int)*(uint32_t *)0x6674 + uVar3 * 4);
                            *(char *)((int)uVar1 + uVar4) = *(char *)(iVar7 + local_a * 7 + local_8) + '\x03';
                        } else {
                            uVar1 = *(uint32_t *)((int)*(uint32_t *)0x6674 + uVar3 * 4);
                            *(uint8_t *)((int)uVar1 + uVar4) = *(uint8_t *)(iVar7 + local_a * 7 + local_8);
                        }
                    }
                    if (local_8 == 6) break;
                    local_8 = local_8 + 1;
                }
            }
            if (local_a == 6) {
                return;
            }
        }
    }
    return;
}