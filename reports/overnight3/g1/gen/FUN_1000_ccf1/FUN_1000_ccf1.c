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
extern void FUN_235c_095c(uint16_t, uint16_t, uint16_t, uint16_t);
extern void FUN_1000_bfd7(int, uint16_t);

void FUN_1000_ccf1(int param_1, char param_2, char param_3) {
    char cVar1;
    uint8_t extraout_AH;
    uint8_t extraout_AH_00;
    uint8_t extraout_AH_01;
    uint8_t uVar2;
    uint16_t unaff_SS;
    uint16_t unaff_DS;

    FUN_24dd_0530();
    if (((((param_3 == 0x04) || (param_3 == 0x05)) || (param_3 == '\b')) ||
        ((param_3 == '\t' || (param_3 == '\n')))) || (param_3 == '\v')) {
        uVar2 = extraout_AH;
        if (*(char *)0x4b8 != '\0') {
            if (param_2 < '\x01') {
                FUN_235c_095c(0, 0, *(uint16_t *)0x679c, *(uint16_t *)0x679e);
                uVar2 = extraout_AH_01;
            } else {
                FUN_235c_095c(0, 0, *(uint16_t *)0x67a0, *(uint16_t *)0x67a2);
                uVar2 = extraout_AH_00;
            }
        }
        *(uint8_t *)0x78e0 = 0;
        *(uint8_t *)0x78de = 0;
        FUN_1000_bfd7(param_1, ((uint16_t)uVar2 << 8) | param_3);
    } else if (param_3 == '\0') {
        if (*(char *)0x4b8 != '\0') {
            if (param_2 < '\x01') {
                FUN_235c_095c(0, 0, *(uint16_t *)0x679c, *(uint16_t *)0x679e);
            } else {
                FUN_235c_095c(0, 0, *(uint16_t *)0x67a0, *(uint16_t *)0x67a2);
            }
        }
        *(uint8_t *)0x78de = 0;
        *(uint8_t *)0x78e0 = 0;
        *(char *)0x66ac = *(char *)0x66ac + param_2;
        if (*(char *)0x66ac < '\0') {
            *(uint8_t *)0x66ac = 3;
        }
        if ('\x03' < *(char *)0x66ac) {
            *(uint8_t *)0x66ac = 0;
        }
    } else if (param_3 == '\x01') {
        if (*(char *)(param_1 + -0x10d) == '\0') {
            cVar1 = *(char *)0x66ac;
            if (cVar1 == '\0') {
                if ((param_2 < '\0') && (1 < *(int *)0x669f)) {
                    *(int *)0x669f = *(int *)0x669f + (int)param_2;
                }
                if (('\0' < param_2) && (*(int *)0x669f < 999)) {
                    *(int *)0x669f = *(int *)0x669f + (int)param_2;
                }
            } else if (cVar1 == '\x01') {
                if ((param_2 < '\0') && (0x3c < *(int *)0x66a1)) {
                    *(int *)0x66a1 = *(int *)0x66a1 + param_2 * 10;
                }
                if (('\0' < param_2) && (*(int *)0x66a1 < 0xe10)) {
                    *(int *)0x66a1 = *(int *)0x66a1 + param_2 *