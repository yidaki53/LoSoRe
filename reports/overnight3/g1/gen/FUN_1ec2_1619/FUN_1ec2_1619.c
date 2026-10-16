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

void FUN_1ec2_152f(uint8_t *param1, uint16_t seg, uint8_t *param2, uint16_t seg2, uint8_t *param3, uint16_t seg3, uint8_t param4, uint16_t seg4);
void FUN_2971_65df(uint16_t param1, uint16_t param2, uint16_t param3, uint16_t param4, uint16_t param5);

void __stdcall16far FUN_1ec2_1619(uint8_t param_1, uint8_t param_2) {
    uint8_t bVar1;
    uint8_t bVar2;
    uint8_t extraout_AH;
    uint8_t uVar3;
    uint8_t extraout_AH_00;
    uint8_t local_9;
    uint8_t local_8;
    uint8_t local_7;
    uint8_t local_6;
    uint8_t local_5;
    uint8_t local_4;
    uint8_t local_3;

    FUN_1ec2_152f(&local_6, 0x1ec2, &local_5, 0x1ec2, &local_4, 0x1ec2, param_1, 0x1ec2);
    bVar1 = param_2;
    param_1 = param_1 - 1;
    uVar3 = extraout_AH;
    bVar2 = param_1;
    if (param_2 <= param_1) {
        while (true) {
            local_3 = bVar2;
            FUN_1ec2_152f(&local_9, 0x1ec2, &local_8, 0x1ec2, &local_7, 0x1ec2, local_3, 0x1ec2);
            uVar3 = (local_3 + 1) >> 8;
            FUN_2971_65df(0x1ec2, ((uint16_t)uVar3 << 8) | local_9, ((uint16_t)uVar3 << 8) | local_8, ((uint16_t)uVar3 << 8) | local_7, local_3 + 1);
            uVar3 = extraout_AH_00;
            if (local_3 == bVar1) break;
            bVar2 = local_3 - 1;
        }
    }
    FUN_2971_65df(0x1ec2, ((uint16_t)uVar3 << 8) | local_6, ((uint16_t)uVar3 << 8) | local_5, ((uint16_t)uVar3 << 8) | local_4, ((uint16_t)uVar3 << 8) | param_2);
    return;
}