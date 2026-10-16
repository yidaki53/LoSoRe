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

void FUN_24dd_3eaf(uint8_t, void*, uint16_t, uint16_t, uint16_t);
void FUN_24dd_3e95(uint16_t, uint16_t);
void FUN_24dd_3639(void*, uint16_t, void*, uint16_t);
void FUN_24dd_36bc(uint16_t, void*);
void FUN_24dd_04f4(void);
void FUN_24dd_39c3(uint16_t, uint16_t, uint16_t);
void FUN_24dd_3930(void*, uint16_t);
void FUN_24dd_3711(void*, uint16_t);
void FUN_24dd_3b22(void*, uint16_t, void*, uint16_t);
void FUN_24dd_3b66(uint8_t, void*, uint16_t);
void FUN_24dd_3c4f(uint8_t, uint8_t, uint8_t, uint16_t, uint16_t, void*, uint16_t);
void FUN_24dd_3bde(void*, uint16_t);

void __stdcall16far FUN_202c_093b(uint8_t *param_1) {
    uint8_t *pbVar1;
    uint8_t *pbVar2;
    uint32_t uVar3;
    uint8_t *pbVar4;
    uint8_t local_382[246];
    uint8_t local_28c[10];
    uint8_t local_282[256];
    uint8_t local_182[128];
    uint8_t local_102;
    uint8_t abStack_101[255];

    pbVar4 = param_1;
    local_102 = *param_1;
    pbVar2 = abStack_101;
    for (uVar3 = local_102; pbVar4 = pbVar4 + 1, uVar3 != 0; uVar3 = uVar3 - 1) {
        pbVar1 = pbVar2;
        pbVar2 = pbVar2 + 1;
        *pbVar1 = *pbVar4;
    }
    if (*(char *)(0x666e) != '\0') {
        *(uint8_t *)(0x66ec) = 0;
    }
    if (*(char *)(0x666f) != '\0') {
        *(uint8_t *)(0x6701) = 0;
    }
    if (local_102 == 0) {
        FUN_24dd_3eaf(0xff, &local_102, __CS__, 0x926, 0x202c);
        FUN_24dd_3e95(0x92c, 0x24dd);
        FUN_24dd_3639(local_28c, __CS__, local_282, __CS__);
        FUN_24dd_36bc(0x24dd, local_282);
        FUN_24dd_04f4();
        if (*(char *)(0x6664) == '\0') {
            FUN_24dd_3eaf(8, (void *)(0x6664), __DS__, 0x926, 0x24dd);
        }
        FUN_24dd_39c3(0, (uint16_t)(0x6664), __DS__);
        FUN_24dd_3930(local_282, __CS__);
        FUN_24dd_04f4();
        FUN_24dd_3711(local_282, __CS__);
        FUN_24dd_04f4();
    }
    FUN_24dd_3eaf(8, (void *)(0x6664), __DS__, &local_102, __CS__);
    FUN_24dd_3e95(&local_102, __CS__);
    FUN_24dd_3f14(0x936, 0x24dd);
    FUN_24dd_3b22(local_382, __CS__, local_182, __CS__);
    FUN_24dd_3b66(1