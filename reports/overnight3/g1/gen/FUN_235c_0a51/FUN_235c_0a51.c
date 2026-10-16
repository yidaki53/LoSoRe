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

void FUN_235c_091d(char param_1);

void FUN_235c_0a51(void) {
    int iVar1;
    uint uVar2;
    int iVar3;
    uint32_t uVar4;
    int iVar5;
    uint16_t uVar6;
    char local_3 = 0;

    while (true) {
        if (*(char *)(0x67fc + local_3) != '\0') {
            uVar4 = *(uint32_t *)(0x6804 + local_3 * 10);
            uVar6 = (uint16_t)(uVar4 >> 16);
            iVar5 = (int)uVar4;
            iVar1 = *(int *)(iVar5 + 8);
            uVar2 = *(uint *)(0x6809 + local_3 * 10);
            iVar3 = *(int *)(0x680b + local_3 * 10);
            if ((iVar1 < iVar3) || ((iVar1 <= iVar3 && (*(uint *)(iVar5 + 6) <= uVar2)))) {
                FUN_235c_091d((char)((uVar2 >> 8) | local_3));
                *(char *)0x67ce = *(char *)0x67ce - 1;
            }
        }
        if (local_3 == 7) break;
        local_3 = local_3 + 1;
    }
    return;
}