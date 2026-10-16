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

// External function declarations
void FUN_24dd_0530(void);
uint8_t FUN_24dd_4161(void);

// Global variable declaration
extern uint32_t DAT_6670;

uint8_t FUN_1000_0d70(int param_1, int param_2, uint8_t param_3, uint8_t param_4) {
    uint8_t bVar1;
    int iVar2;
    int iVar3;
    int iVar4;
    int iVar5;
    int local_b;
    int local_9;

    FUN_24dd_0530();
    if (*(char *)((int)DAT_6670 + (uint)param_4 * 0xaa + 0x9a) != '\0') {
        iVar2 = (param_2 - *(int *)((int)DAT_6670 + (uint)param_4 * 0xaa + 6)) + 7;
        iVar3 = (param_1 - *(int *)((int)DAT_6670 + (uint)param_4 * 0xaa + 10)) + 5;
        if (*(char *)((int)DAT_6670 + (uint)param_4 * 0xaa + 0x9b) == '\0') {
            iVar2 = 0xe - iVar2;
        }
        local_9 = iVar2 - (uint)param_3;
        if (local_9 <= (int)((uint)param_3 + iVar2)) {
            while (true) {
                iVar4 = (uint)param_3 + iVar3;
                local_b = iVar3 - (uint)param_3;
                if (local_b <= iVar4) {
                    while (true) {
                        if ((((0 < local_9) && (local_9 < 0xe)) && (-1 < local_b)) && (local_b < 10)) {
                            iVar5 = 0x20;
                            bVar1 = FUN_24dd_4161();
                            if ((*(uint8_t *)(iVar5 + 0x28) & bVar1) != 0) {
                                return 1;
                            }
                        }
                        if (local_b == iVar4) break;
                        local_b = local_b + 1;
                    }
                }
                if (local_9 == (uint)param_3 + iVar2) break;
                local_9 = local_9 + 1;
            }
        }
    }
    return 0;
}