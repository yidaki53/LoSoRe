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

void FUN_24dd_0530(void);
void FUN_24ba_00c4(void);
void FUN_24dd_3eaf(uint8_t, uint8_t*, uint16_t, uint16_t, uint16_t);
void FUN_24dd_3e95(uint16_t, uint16_t);
void FUN_24dd_3f14(uint8_t*, uint16_t);
uint16_t FUN_202c_0673(uint8_t*, uint16_t);
void FUN_1ec2_00a5(uint8_t, uint8_t, int, int, int, int);
void FUN_1ec2_0d88(uint8_t, uint8_t, uint8_t, int, int);
void FUN_1ec2_13e9(uint16_t, uint16_t, int, int, uint8_t, uint8_t*, uint16_t, uint8_t, uint8_t);
uint16_t FUN_249c_019d(void);
uint8_t FUN_24dd_4919(uint16_t);
void FUN_24dd_403d(uint8_t, uint8_t, uint8_t*, uint16_t);
void FUN_24dd_3fb1(uint8_t);
void FUN_235c_095c(uint8_t, uint8_t, uint16_t, uint16_t);
void FUN_202c_093b(uint8_t*, uint16_t);

void FUN_1000_a9c1(int param_1) {
    uint8_t bVar1;
    uint16_t uVar2;
    uint8_t extraout_AH;
    uint16_t unaff_SS;
    uint16_t unaff_DS;
    uint8_t *puVar3;
    uint8_t *puVar4;
    uint16_t uVar5;
    uint16_t uVar6;
    uint8_t local_305[256];
    uint8_t local_205[256];
    uint8_t local_105[255];
    uint32_t uStack_6;

    uStack_6 = 0x1000a9cc;
    FUN_24dd_0530();
    *((uint8_t*)(param_1 - 0x20e)) = 1;
    FUN_24ba_00c4();
    FUN_24dd_3eaf(0xff, local_105, unaff_SS, 0x6664, unaff_DS);
    do {
        puVar3 = local_205;
        uVar2 = unaff_SS;
        FUN_24dd_3e95(0xa9b4, 0x24dd);
        FUN_24dd_3f14(local_105, unaff_SS);
        FUN_24dd_3f14(0xa9bf, 0x24dd);
        uVar2 = FUN_202c_0673(puVar3, uVar2);
        uStack_6 = ((uint32_t)uVar2 << 8) | (uStack_6 & 0xff);
        FUN_1ec2_00a5(8, 0x78, (int)*(uint32_t*)0x65d7 + 0x5021,
                      (int)((*(uint32_t*)0x65d7 >> 0x10) & 0xffff), (int)*(uint32_t*)0x6684 + 0x5021,
                      (int)((*(uint32_t*)0x6684 >> 0x10) & 0xffff));
        FUN_1ec2_0d88(0, 7, (uint8_t)(uStack_6 >> 8), (int)*(uint32_t*)0x65d7 + 0x5021,
                      (int)((*(uint32_t*)0x65d7 >> 0x10) & 0xffff));
        uVar6 = 0x23;
        uVar5 = 0x41;
        puVar3 = local_205;
        uVar2 = unaff_SS;
        FUN_24dd_3e95(0xa9b4, 0x1ec2