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
uint16_t FUN_24dd_4824(int *param_1, uint16_t param_2, byte *param_3, uint16_t param_4);
void FUN_24dd_46e9(void);

// Function definition
uint16_t __stdcall16far FUN_202c_0706(byte *param_1) {
    byte *pbVar1;
    byte *pbVar2;
    uint uVar3;
    byte *pbVar4;
    int local_10c;
    uint16_t local_10a;
    byte local_106;
    byte abStack_105[259];

    pbVar4 = param_1;
    local_106 = *param_1;
    pbVar2 = abStack_105;
    for (uVar3 = (uint)local_106; pbVar4 = pbVar4 + 1, uVar3 != 0; uVar3 = uVar3 - 1) {
        pbVar1 = pbVar2;
        pbVar2 = pbVar2 + 1;
        *pbVar1 = *pbVar4;
    }
    local_10a = FUN_24dd_4824(&local_10c, 0, &local_106, 0);
    FUN_24dd_46e9();
    if (local_10c != 0) {
        local_10a = ((uint16_t)*(uint16_t *)0x6414 << 8) | *(uint16_t *)0x6412;
    }
    return local_10a;
}