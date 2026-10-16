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

extern void FUN_24dd_0530(void);
extern void FUN_24dd_40d6(int);
extern void FUN_24dd_4141(int, uint8_t*, uint16_t, uint8_t*);
extern char FUN_24dd_4654(int);
extern uint8_t FUN_24dd_4161(void);
extern void FUN_24dd_40ac(int, uint8_t*, uint16_t);
extern void FUN_24dd_40ec(uint8_t);
extern void FUN_24dd_4181(uint8_t*, uint16_t);
extern void FUN_1000_5e66(void);
extern void FUN_1ec2_0000(int, int, int, int);
extern uint16_t FUN_202c_0673(int, int);
extern void FUN_1ec2_0d88(int, int, uint16_t, int);
extern void FUN_1ec2_13e9(int, uint16_t, int, int, int, int, int, int);
extern void FUN_24dd_3e95(int, int);
extern void FUN_24dd_3f14(int, uint16_t);
extern void FUN_1ec2_13c5(void);
extern void FUN_1ec2_10ea(int, int);
extern void FUN_1ec2_1619(int);
extern void FUN_1ec2_155e(int);
extern void FUN_235c_095c(int, int, uint16_t);

void FUN_1000_929a(void) {
    char local_72[32];
    char local_52[32];
    uint8_t local_32[32];
    char local_12[2];
    int aiStack_10[7];
    uint16_t unaff_SS = 0; // Assuming SS is 0 for simplicity
    uint16_t unaff_DS = 0; // Assuming DS is 0 for simplicity

    aiStack_10[6] = 0x1000;
    aiStack_10[5] = -0x6d5b;
    FUN_24dd_0530();
    aiStack_10[2] = 0;
    aiStack_10[6] = 1;
    while (true) {
        if (*(char*)(aiStack_10[6] + 0x66af) == '\0') {
            aiStack_10[2] = aiStack_10[2] + 1;
        }
        if (aiStack_10[6] == 0x25) break;
        aiStack_10[6] = aiStack_10[6] + 1;
    }
    aiStack_10[6] = 0;
    while (true) {
        uint8_t* puVar7 = local_52;
        uint16_t uVar4 = unaff_SS;
        FUN_24dd_40d6(1);
        FUN_24dd_4141(0x20, local_32, unaff_SS, puVar7, uVar4);
        aiStack_10[5] = 1;
        while (true) {
            if ((*(char*)(aiStack_10[6] * 5 + aiStack_10[5] + 0x66dd) == '\0') ||
                (*(char*)(aiStack_10[6] + 0x66a7) != '\0')) {
                char cVar2 = FUN_24dd_4654(0x28);
                *(char*)(aiStack_10[6] * 5 + aiStack_10[5] + 0x66dd) = cVar2 + '\x01';
            }
            if (aiStack_10[2] < 5) {
                while ('\0' < *(char*)(*(byte*)(*(byte*)(aiStack_10[6] * 5 + aiStack_10[5] + 0x66dd) + 0xa9d) + 0x66af)) {
                    char cVar2 = FUN_24dd_4654(0x28);
                    *(char*)(aiStack_10[6] * 5 + aiStack_10[5] + 0