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
void FUN_1000_05eb(int);
void FUN_202c_0f10(void);
void FUN_24dd_4905(int, int, int, int);
void FUN_24dd_4654(int);
void FUN_1ec2_10cf(uint8_t, uint8_t, uint8_t, uint16_t);
void FUN_24dd_3f86(int, int, int, int);
void FUN_24dd_3e95(int, int);
void FUN_24dd_3f14(int, int);
void FUN_1ec2_13e9(int, int, int, int, int, void*, int, int, int);
void FUN_24dd_3eaf(int, int, int, int, int);
void FUN_24dd_3d80(void);
uint16_t FUN_24dd_3dbd(void);
void FUN_1000_9f45(int);

extern uint16_t DAT_651d;
extern uint32_t DAT_6670;
extern uint32_t DAT_6688;
extern uint32_t DAT_6690;
extern uint32_t DAT_668c;
extern uint32_t DAT_6694;
extern uint32_t DAT_6698;
extern uint32_t DAT_66a9;
extern uint32_t DAT_66ae;
extern uint32_t DAT_58b8;
extern uint32_t DAT_58b7;
extern uint32_t DAT_58b6;
extern uint32_t DAT_672e;
extern uint32_t DAT_65f2;
extern uint32_t DAT_67ba;
extern uint32_t DAT_67b0;
extern uint32_t DAT_67b4;
extern uint32_t DAT_6478;
extern uint32_t DAT_647a;
extern uint32_t DAT_dbc;
extern uint32_t DAT_66e8;

void FUN_1000_d7b5(void) {
    uint16_t uVar1;
    uint8_t bVar3;
    int iVar2;
    uint16_t uVar4;
    uint16_t uVar7;
    uint16_t uVar8;
    uint8_t local_188[252];
    int local_8c;
    uint16_t uStack_8a;
    int local_86;
    int local_4;

    local_4 = 0x1000;
    uStack_8a = 0xd7c0;
    FUN_24dd_0530();
    *(uint8_t*)0x651f = 2;
    FUN_1000_05eb(0);
    FUN_1000_05eb(1);
    FUN_202c_0f10();
    FUN_24dd_4905(0, 0x1fe, (int)DAT_6670, (int)(DAT_6670 >> 16));
    FUN_24dd_4905(0, 0x2ef4, (int)DAT_6688, (int)(DAT_6688 >> 16));
    FUN_24dd_4905(0, 0x2e8d, (int)DAT_6690, (int)(DAT_6690 >> 16));
    FUN_24dd_4905(0, 0x132b, (int)DAT_668c, (int)(DAT_668c >> 16));
    FUN_24dd_4905(0, 0x2ef4, (int)DAT_6694, (int)(DAT_6694 >> 16));
    FUN_24dd_4905(0, 0x56a, (int)DAT_6698, (int)(DAT_6698 >> 16));
    local_4 = 0;
    while (true) {
        uStack_8a = (uint16_t)(DAT_6670 >> 16);
        local_8c = (int)DAT_6670 + local