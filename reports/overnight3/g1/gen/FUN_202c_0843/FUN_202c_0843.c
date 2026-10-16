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
void FUN_24dd_3b22(uint8_t *param_1, uint16_t param_2, uint8_t *param_3, uint16_t param_4);
void FUN_24dd_3b5d(uint8_t param_1, uint8_t *param_2, uint16_t param_3);
void FUN_24dd_3bde(uint8_t *param_1, uint16_t param_2);
int FUN_24dd_04ed(void);

// Function implementation
uint8_t FUN_202c_0843(uint8_t *param_1) {
    uint8_t local_184[128];
    uint8_t local_104;
    uint8_t abStack_103[257];
    uint8_t *pbVar1;
    uint8_t *pbVar2;
    uint8_t *pbVar6;
    uint32_t uVar5;
    int iVar4;
    uint8_t uVar3;

    pbVar6 = param_1;
    local_104 = *param_1;
    pbVar2 = abStack_103;
    for (uVar5 = local_104; pbVar6 = pbVar6 + 1, uVar5 != 0; uVar5 = uVar5 - 1) {
        pbVar1 = pbVar2;
        pbVar2 = pbVar2 + 1;
        *pbVar1 = *pbVar6;
    }
    FUN_24dd_3b22(&local_104, 0, local_184, 0);
    *(uint8_t *)0x6422 = 0;
    FUN_24dd_3b5d(0x80, local_184, 0);
    FUN_24dd_3bde(local_184, 0);
    iVar4 = FUN_24dd_04ed();
    if ((iVar4 == 0) && (local_104 != 0)) {
        uVar3 = 1;
    } else {
        uVar3 = 0;
    }
    return uVar3;
}