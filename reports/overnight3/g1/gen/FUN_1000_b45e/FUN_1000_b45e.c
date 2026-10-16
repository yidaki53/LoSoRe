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

extern void FUN_24dd_0530();
extern void FUN_24dd_4905(int, int, void*, uint16_t);
extern void FUN_1000_b28f(void*);
extern void FUN_1ec2_00a5(int, int, int, int, int, int);
extern void FUN_1ec2_0d88(int, int, uint16_t, int, int);
extern uint16_t FUN_202c_0673(int, uint16_t);
extern void FUN_1ec2_13e9(int, uint16_t, int, int, uint8_t, int, uint16_t, int, int);
extern void FUN_1ec2_0d5d(uint8_t, int, uint8_t, int, int);
extern void FUN_1ec2_01df(uint16_t, int, int, int, int, int, int, int);
extern void FUN_235c_095c(int, int, uint16_t, uint16_t);
extern void FUN_1000_b04a(int, int, uint16_t, int, int, int);
extern void FUN_24dd_3eaf(int, void*, uint16_t, void*, uint16_t);
extern void FUN_1000_a816(uint16_t);
extern uint16_t FUN_1000_ad8b(int, uint16_t, int, int, int, int);
extern uint16_t FUN_1000_b3fe(void*);

void FUN_1000_b45e(int param_1, uint8_t param_2) {
    uint16_t local_1cf[256];
    char local_cf[31];
    uint8_t auStack_b0[10];
    uint16_t local_a6;
    uint8_t local_a4;
    uint8_t local_a3[156];
    uint8_t local_7;
    int local_6;
    int local_4;

    local_4 = 0x1000;
    local_6 = 0xb469;
    FUN_24dd_0530();
    local_7 = 0;
    local_6 = 0;
    FUN_24dd_4905(0, 0x9c, local_a3, 0);
    do {
        *(uint8_t*)(param_1 + -0x20e) = 0;
        FUN_1000_b28f(&local_1cf);
        FUN_1ec2_00a5(0x82, 0x9d, (int)*(uint32_t*)0x65d7 + 0x19a3,
                      (int)((uint32_t)*(uint32_t*)0x65d7 >> 0x10), (int)*(uint32_t*)0x6684 + 0x19a3,
                      (int)((uint32_t)*(uint32_t*)0x6684 >> 0x10));
        uint16_t uVar5 = (uint16_t)((uint32_t)*(uint32_t*)0x65d7 >> 0x10);
        int iVar4 = (int)*(uint32_t*)0x65d7 + (local_6 * 8 + 0x14) * 0x140 + 0xb2;
        uint16_t uVar3 = FUN_202c_0673(local_6 * 0xd + 0x390, 0);
        FUN_1ec2_0d88(0, 7, uVar3, iVar4, uVar5);
        if (((uint8_t)local_6 != 0) && ((uint8_t)local_6 < 0xd)) {
            local_a4 = FUN_202c_0673(auStack_b0 + local_6 * 0xd, 0);
            FUN_1ec2_0d88(0, 7, local_a4,
                          (int)*(uint32_t*)0x65d7 + (local_6 * 8 + 0x14) * 0x140 +
                          (0x111 - (uint)(local_a4 >> 1)), (int)((uint32_t)*(uint32_t*)0x6