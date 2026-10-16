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

void FUN_24dd_48c1(uint16_t param_1);
void FUN_24dd_4734(void);
void FUN_24dd_4628(uint16_t param_1, uint16_t param_2, uint16_t param_3, uint16_t param_4);
void FUN_24dd_4514(void);
void FUN_24dd_43e9(uint16_t param_1, uint16_t param_2);
void FUN_24dd_4284(void);
void FUN_24dd_4168(uint16_t param_1, uint16_t param_2);
void FUN_24dd_4044(void);
void FUN_24dd_3f31(uint16_t param_1);
void FUN_24dd_3e84(void);

void __stdcall16far FUN_1ec2_0018(uint16_t param_1, uint8_t *param_2) {
    uint8_t *puVar1;
    uint8_t *puVar2;
    uint8_t *puVar3;
    uint8_t *puVar4;
    uint16_t uVar5;
    uint16_t uVar6;
    uint16_t uVar7;
    uint16_t uVar8;
    uint16_t *puVar9;
    uint16_t uVar10;

    uVar10 = (uint16_t)((uintptr_t)param_2 >> 16);
    puVar4 = param_2;
    uVar8 = param_1 >> 12;
    puVar3 = puVar4;
    puVar4 = puVar4 + 0xff;
    for (uVar7 = 0xf000; uVar7 != 0; uVar7 = uVar7 - 0x10) {
        puVar2 = puVar3;
        puVar3 = puVar3 + 1;
        FUN_24dd_48c1(*puVar2);
    }
    uVar8 = uVar8 << 8;
    puVar4 = param_2;
    uVar7 = param_1 >> 8;
    puVar3 = puVar4;
    puVar4 = puVar4 + 0xff;
    for (uVar6 = 0xf00; uVar6 != 0; uVar6 = uVar6 - 0x10) {
        puVar1 = puVar3;
        puVar3 = puVar3 + 1;
        FUN_24dd_48c1(*puVar1);
    }
    uVar8 = uVar8 << 8;
    puVar4 = param_2;
    uVar7 = param_1 >> 4;
    puVar3 = puVar4;
    puVar4 = puVar4 + 0xff;
    for (uVar6 = 0xf0; uVar6 != 0; uVar6 = uVar6 - 0x10) {
        puVar1 = puVar3;
        puVar3 = puVar3 + 1;
        FUN_24dd_48c1(*puVar1);
    }
    uVar8 = uVar8 << 8;
    puVar4 = param_2;
    uVar7 = param_1 >> 0;
    puVar3 = puVar4;
    puVar4 = puVar4 + 0xff;
    for (uVar6 = 0xf; uVar6 != 0; uVar6 = uVar6 - 0x10) {
        puVar1 = puVar3;
        puVar3 = puVar3 + 1;
        FUN_24dd_48c1(*puVar1);
    }
    puVar9 = (uint16_t *)param_1;
    FUN_24dd_4628(*puVar9, 0xff, 0, 0);
    FUN_24dd_4514();
    return;
}