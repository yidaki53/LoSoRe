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

void FUN_1ec2_01df(char param_1, char param_2, uint32_t param_3, uint8_t *param_4, int param_5, int param_6) {
    uint8_t local_102[256];
    int local_108;
    int local_104;
    uint16_t uVar6 = (uint16_t)param_3;
    uint16_t uVar7 = (uint16_t)(param_3 >> 16);

    for (int i = 0; i < 256; i++) {
        local_102[i] = param_4[i];
    }

    if (param_1 == '\0') {
        if (param_2 == '\0') {
            local_108 = 0;
            while (true) {
                for (local_104 = 2; local_104 != 0xb; local_104++) {
                    FUN_1ec2_0dc8(uVar6, uVar7, ((uint16_t)((uint8_t)(local_104 >> 8)) << 8) | local_102[local_108 * 0x10 + local_104], param_5 + local_108, (0xe - local_104) + param_6);
                }
                if (local_108 == 8) break;
                local_108++;
            }
        } else {
            local_108 = 0;
            while (true) {
                for (local_104 = 2; local_104 != 0xb; local_104++) {
                    FUN_1ec2_0dc8(uVar6, uVar7, ((uint16_t)((uint8_t)(local_104 >> 8)) << 8) | local_102[local_108 * 0x10 + local_104], param_5 + local_108, param_6 + local_104);
                }
                if (local_108 == 8) break;
                local_108++;
            }
        }
    } else if (param_1 == '\x01') {
        if (param_2 == '\0') {
            local_108 = 0;
            while (true) {
                for (local_104 = 2; local_104 != 0xb; local_104++) {
                    FUN_1ec2_0e06(uVar6, uVar7, ((uint16_t)((uint8_t)(local_104 >> 8)) << 8) | local_102[local_108 * 0x10 + local_104], param_5 + local_108, (0xe - local_104) + param_6);
                }
                if (local_108 == 8) break;
                local_108++;
            }
        } else {
            local_108 = 0;
            while (true) {
                for (local_104 = 2; local_104 != 0xb; local_104++) {
                    FUN_1ec2_0e06(uVar6, uVar7, ((uint16_t)((uint8_t)(local_104 >> 8)) << 8) | local_102[local_108 * 0x10 + local_104], param_5 + local_108, param_6 + local_104);
                }
                if (local_108 == 8) break;
                local_108++;
            }
        }
    }
}