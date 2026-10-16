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

void __stdcall16far FUN_1ec2_0c3b(uint32_t param_1, int param_2, int param_3, int param_4, int param_5) {
    uint16_t uVar1;
    uint16_t uVar2;
    int iVar3;
    int iVar4;
    int iVar5;
    int iVar6;
    int iVar7;
    uint16_t uVar8;
    char local_11 = '>';
    int local_8;
    int local_6 = param_4;
    int local_4 = param_5;

    uVar1 = param_3 - param_5;
    uVar2 = param_2 - param_4;
    iVar3 = FUN_1ec2_0c11((void*)&local_11, uVar1);
    iVar4 = FUN_1ec2_0c11((void*)&local_11, uVar2);
    iVar5 = (uVar1 ^ (int)uVar1 >> 0xf) - ((int)uVar1 >> 0xf);
    iVar6 = (uVar2 ^ (int)uVar2 >> 0xf) - ((int)uVar2 >> 0xf);
    uVar8 = (uint16_t)(param_1 >> 0x10);

    if (iVar6 < iVar5) {
        local_8 = -(iVar5 / 2);
        while (local_4 != param_3) {
            local_8 += iVar6;
            local_4 += iVar3;
            iVar7 = local_4;
            if (0 < local_8) {
                local_6 += iVar4;
                iVar7 = local_8 - iVar5;
                local_8 = iVar7;
            }
            local_11 += '\x01';
            if (local_11 == '@') {
                local_11 = '>';
            }
            FUN_1ec2_0dc8((int)param_1, uVar8, ((uint16_t)iVar7 >> 8) | local_11, local_6, local_4);
        }
    } else {
        local_8 = -(iVar6 / 2);
        while (local_6 != param_2) {
            local_8 += iVar5;
            local_6 += iVar4;
            iVar7 = local_6;
            if (0 < local_8) {
                local_4 += iVar3;
                iVar7 = local_8 - iVar6;
                local_8 = iVar7;
            }
            local_11 += '\x01';
            if (local_11 == '@') {
                local_11 = '>';
            }
            FUN_1ec2_0dc8((int)param_1, uVar8, ((uint16_t)iVar7 >> 8) | local_11, local_6, local_4);
        }
    }
}