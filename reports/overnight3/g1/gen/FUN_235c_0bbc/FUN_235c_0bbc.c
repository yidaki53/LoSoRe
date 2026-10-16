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

// External function declarations
void FUN_235c_091d(uint8_t param_1);
void FUN_24dd_028a(uint16_t param_1);
void FUN_235c_0aff(uint16_t param_1, uint16_t param_2);
void FUN_24dd_3dbd(void);
void FUN_235c_0b33(uint16_t param_1, uint16_t param_2);
void FUN_24dd_4905(uint16_t param_1, uint16_t param_2, uint16_t param_3, uint16_t param_4);
void FUN_235c_0b7c(void);
void FUN_235c_0aad(uint16_t param_1);
void FUN_235c_03a1(void);

// Global variables
uint16_t DAT_67ce;
uint16_t DAT_67cd;
uint16_t DAT_67c2;
uint16_t DAT_67c4;
uint16_t DAT_6e58;
uint16_t DAT_6e5a;
uint16_t DAT_6e5c;
uint16_t DAT_6e5e;
uint16_t DAT_6e60;
uint16_t DAT_6e62;
uint16_t DAT_6e70;
uint16_t DAT_6e72;
uint16_t DAT_6e74;
uint16_t DAT_6e76;
uint16_t DAT_6e7f;
uint16_t DAT_6e80;
uint16_t DAT_6a58;

void FUN_235c_0bbc(void) {
    uint8_t uVar1;
    uint16_t uVar2;
    uint16_t uVar3;
    int iVar4;
    uint16_t local_4;

    for (local_4 = 0; FUN_235c_091d(local_4 & 0xff), local_4 != 7; local_4++) {
    }
    DAT_67ce = 0;
    if (*(char *)0x67cd == '\0') {
        uint32_t uVar5 = FUN_24dd_028a(0x800);
        DAT_6e58 = (uint16_t)uVar5;
        DAT_6e5a = (uint16_t)(uVar5 >> 16);
        FUN_235c_0aff(DAT_6e58, DAT_6e5a);
        uVar2 = 0;
        iVar4 = 1;
        FUN_24dd_3dbd();
        if ((int)(iVar4 + (uint)(0xfbff < uVar2)) < 1) {
            uVar3 = DAT_6e5a;
            DAT_6e5c = DAT_6e58;
            DAT_6e5e = uVar3;
        } else {
            uVar5 = FUN_235c_0b33((int)DAT_6e58 + 0x400, (int)(DAT_6e58 >> 16));
            DAT_6e5c = (uint16_t)uVar5;
            DAT_6e5e = (uint16_t)(uVar5 >> 16);
        }
        local_4 = 1;
        while (true) {
            uVar5 = FUN_235c_0b33((int)DAT_6e5c + local_4 * 0x200 - 0x200, (int)(DAT_6e5c >> 16));
            *(uint16_t *)(local_4 * 4 + 0x6e60) = (uint16_t)uVar5;
            *(uint16_t *)(local_4 * 4 + 0x6e62) = (uint16_t)(uVar5 >> 16);
            if (local_4 == 2) break;
            local_4++;
        }
        uVar5 = FUN_235c_0aff(DAT_6e5c, DAT_6e5e);
        DAT_6e70 = (uint16_t)uVar5;
        DAT_6e72 = (uint16_t)(uVar5 >> 16);
        uVar1 =