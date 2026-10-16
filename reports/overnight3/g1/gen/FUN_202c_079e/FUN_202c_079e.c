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
extern char FUN_202c_0843(byte *param_1, undefined2 unaff_SS);
extern void FUN_24dd_3b22(byte *param_1, undefined2 unaff_SS, undefined1 *param_3, undefined2 unaff_SS2);
extern void FUN_24dd_3b5d(int param_1, undefined1 *param_2, undefined2 unaff_SS);
extern void FUN_24dd_04f4(void);
extern void FUN_24dd_3cb0(undefined2 param_1, int param_2, undefined1 *param_3, int param_4, int param_5, undefined1 *param_6, undefined2 unaff_SS);
extern void FUN_24dd_3bde(undefined1 *param_1, undefined2 unaff_SS);

// Function definition
uint16_t __stdcall16far FUN_202c_079e(uint16_t param_1, uint16_t param_2, uint32_t param_3, byte *param_4) {
    byte *pbVar1;
    byte *pbVar2;
    char cVar3;
    uint32_t uVar4;
    byte *pbVar5;
    uint16_t local_186;
    undefined1 local_184[128];
    byte local_104;
    byte abStack_103[257];

    pbVar5 = param_4;
    local_104 = *param_4;
    pbVar2 = abStack_103;
    for (uVar4 = local_104; pbVar5 = pbVar5 + 1, uVar4 != 0; uVar4 = uVar4 - 1) {
        pbVar1 = pbVar2;
        pbVar2 = pbVar2 + 1;
        *pbVar1 = *pbVar5;
    }
    local_186 = 0;
    cVar3 = FUN_202c_0843(&local_104, unaff_SS);
    if (cVar3 != '\0') {
        FUN_24dd_3b22(&local_104, unaff_SS, local_184, unaff_SS);
        FUN_24dd_3b5d(1, local_184, unaff_SS);
        FUN_24dd_04f4();
        FUN_24dd_3cb0(param_2, 0, local_184, unaff_SS);
        FUN_24dd_04f4();
        FUN_24dd_3c48(&local_186, unaff_SS, param_1, (int)param_3, (int)((uint32_t)param_3 >> 16), local_184, unaff_SS);
        FUN_24dd_04f4();
        FUN_24dd_3bde(local_184, unaff_SS);
        FUN_24dd_04f4();
    }
    return local_186;
}