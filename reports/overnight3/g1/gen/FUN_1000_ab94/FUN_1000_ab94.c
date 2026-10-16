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
void FUN_1ec2_13e9(uint16_t, uint16_t, int, int, uint8_t, uint8_t*, uint16_t, uint16_t, uint16_t);
uint16_t FUN_249c_019d(void);
uint16_t FUN_24dd_4919(uint16_t);
void FUN_24dd_403d(uint8_t, uint8_t, uint8_t*, uint16_t);
void FUN_24dd_3fb1(uint8_t);
uint8_t FUN_202c_0843(uint8_t*, uint16_t);
void FUN_202c_08b2(uint8_t*, uint16_t);
void FUN_1000_05eb(uint8_t);

void FUN_1000_ab94(int param_1) {
    uint8_t bVar1;
    char cVar2;
    uint16_t uVar3;
    uint16_t uVar6;
    uint16_t uVar7;
    uint8_t local_305[256];
    uint8_t local_205[256];
    uint8_t local_105[255];
    uint8_t uStack_6;

    uStack_6 = 0x1000ab9f;
    FUN_24dd_0530();
    *((uint8_t*)(param_1 - 0x20e)) = 1;
    FUN_24ba_00c4();
    uVar3 = 0x24dd;
    FUN_24dd_3eaf(0xff, local_105, 0, 0x6664, 0);
    do {
        uint8_t* puVar4 = local_205;
        uVar6 = 0;
        FUN_24dd_3e95(0xab82, uVar3);
        FUN_24dd_3f14(local_105, 0);
        FUN_24dd_3f14(0xab8d, 0x24dd);
        uVar3 = FUN_202c_0673(puVar4, uVar6);
        uStack_6 = (uint8_t)((uVar3 << 8) | uStack_6);
        FUN_1ec2_00a5(8, 0x78, (int)*(uint32_t*)0x65d7 + 0x5021, (int)((*(uint32_t*)0x65d7 >> 16) & 0xFFFF), (int)*(uint32_t*)0x6684 + 0x5021, (int)((*(uint32_t*)0x6684 >> 16) & 0xFFFF));
        FUN_1ec2_0d88(0, 7, uStack_6, (int)*(uint32_t*)0x65d7 + 0x5021, (int)((*(uint32_t*)0x65d7 >> 16) & 0xFFFF));
        uVar7 = 0x23;
        uVar6 = 0x41;
        puVar4 = local_205;
        uVar3 = 0;
        FUN_24dd_3e95(0xab82, 0x1ec2);
        FUN_24dd_3f14(local_105, 0);
        FUN_24dd_3f14(0xab8d, 0x24dd);
        FUN