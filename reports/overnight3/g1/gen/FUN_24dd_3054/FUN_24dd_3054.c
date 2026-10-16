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

extern uint16_t DAT_2971_6421;
extern uint16_t DAT_2971_7b58;
extern uint16_t DAT_2971_7b56;
extern uint16_t DAT_2971_7b50;
extern uint16_t DAT_2971_7b4c;
extern uint16_t DAT_2971_7b48;
extern uint16_t DAT_2971_7b44;
extern uint16_t DAT_2971_7b46;
extern uint16_t DAT_2971_6406;
extern uint16_t DAT_2971_6408;
extern uint16_t DAT_2971_640a;
extern uint16_t DAT_2971_640c;
extern uint16_t _DAT_2971_6402;
extern uint16_t DAT_2971_6410;
extern uint16_t DAT_2971_63e4;
extern uint16_t uRam000230c2;
extern uint16_t uRam000230c4;
extern uint16_t uRam0003124e;
extern uint16_t uRam0002311d;

uint16_t FUN_24dd_3054(void) {
    char *pcVar1;
    uint16_t *puVar2;
    void (*pcVar3)(void);
    uint16_t uVar4;
    uint16_t uVar5;
    uint16_t uVar6;
    int iVar7;
    int iVar8;
    uint16_t uVar9;
    char *pcVar10;
    int in_BX;
    int unaff_BP;
    int unaff_SI;
    int unaff_DI;
    uint16_t unaff_SS;
    bool bVar11;
    uint16_t in_FPUControlWord;
    uint16_t in_FPUStatusWord;
    uint8_t bVar12;
    uint16_t in_FPUTagWord;
    uint16_t in_FPULastInstructionOpcode;
    uint32_t in_FPUDataPointer;
    uint32_t in_FPUInstructionPointer;
    uint32_t uVar13;
    uint16_t in_stack_0000000a;
    uint16_t uStack_4;

    uStack_4 = 0x24dd;
    do {
        iVar7 = 10;
        do {
            pcVar3 = (void (*)(void))0x21;
            (*pcVar3)();
            iVar7 = iVar7 + -1;
            iVar8 = 0;
        } while (iVar7 != 0);
        while (true) {
            pcVar3 = (void (*)(void))0x21;
            (*pcVar3)();
            pcVar3 = (void (*)(void))0x21;
            (*pcVar3)();
            pcVar3 = (void (*)(void))0x21;
            (*pcVar3)();
            uRam000230c2 = *(uint16_t *)0x7af4;
            uRam000230c4 = *(uint16_t *)0x7af6;
            pcVar3 = (void (*)(void))0x37;
            uVar5 = (*pcVar3)();
            if (iVar8 == 0) break;
            uVar5 = uVar5 ^ 0x3e2e;
            if ((__builtin_popcount(uVar5 & 0xff) & 1U) == 0) {
                out(0xf0, 0);
                out(0xa0, 0x20);
                out(0x20, 0x20);
                goto LAB_24dd_309c;
            }
            pcVar1 = (char *)(unaff_BP + unaff_DI + -0x322a);
            *pcVar1 = *pcVar1 + (char)iVar8;
            puVar2 = (uint16_t *)(in_BX + unaff_SI + -0x1e);
            *puVar2 = *puVar2 & uVar5 & 0xab9;
        }
    } while (true);
    while (true) {
        pcVar3 = (void (*)(void))0x37;
        uVar6 = (*pcVar3