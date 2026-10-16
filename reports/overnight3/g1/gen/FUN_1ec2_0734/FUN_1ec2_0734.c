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

void __stdcall16far FUN_1ec2_0734(char param_1, uint32_t param_2, char *param_3, int param_4, int param_5) {
    char local_102[256];
    char *pcVar4 = param_3;
    char *pcVar5 = local_102;
    int iVar3;

    for (iVar3 = 0x100; iVar3 != 0; iVar3--) {
        *pcVar5++ = *pcVar4++;
    }

    uint16_t uVar6 = (uint16_t)(param_2 >> 16);

    if (param_1 == '\0') {
        for (int local_108 = 0; local_108 < 8; local_108++) {
            for (int local_104 = 2; local_104 < 0xc; local_104++) {
                if (local_102[local_108 * 0x10 + local_104] != '\0') {
                    FUN_1ec2_0e4a((int)param_2, uVar6, param_4 + local_108, (0xe - local_104) + param_5);
                }
            }
        }
    } else {
        for (int local_108 = 0; local_108 < 8; local_108++) {
            for (int local_104 = 2; local_104 < 0xc; local_104++) {
                if (local_102[local_108 * 0x10 + local_104] != '\0') {
                    FUN_1ec2_0e4a((int)param_2, uVar6, param_4 + local_108, param_5 + local_104);
                }
            }
        }
    }
}