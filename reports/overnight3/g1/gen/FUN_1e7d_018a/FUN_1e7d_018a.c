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

#include <stdbool.h>

bool __stdcall16far FUN_1e7d_018a(unsigned char *param_1, char *param_2, char *param_3, int *param_4) {
    char cVar1;
    unsigned char uVar2;
    int iVar3;
    unsigned char local_30c[256];
    unsigned char local_20c[256];
    unsigned char local_10c[8];
    char local_104[257];
    bool local_3;

    FUN_24dd_3e95(0x182, 0x1e7d);
    FUN_24cb_00a7(local_10c, (unsigned short)&local_10c);
    func_0x0001e7d0(local_20c);
    FUN_24dd_3eaf(0xff, local_104, (unsigned short)&local_104, (unsigned short)&local_104, local_30c);
    iVar3 = FUN_1e7d_0082(1, 0x41, local_104, (unsigned short)&local_104);
    *param_4 = iVar3;
    cVar1 = FUN_1e7d_0082(0, 0x49, local_104, (unsigned short)&local_104);
    *param_3 = cVar1;
    cVar1 = FUN_1e7d_0082(0, 0x44, local_104, (unsigned short)&local_104);
    *param_2 = cVar1;
    uVar2 = FUN_1e7d_0082(0, 0x48, local_104, (unsigned short)&local_104);
    *param_1 = uVar2;
    local_3 = *param_4 != 0xff && local_104[0] != '\0';
    if (*param_3 == -1) {
        local_3 = false;
    }
    if (*param_2 == -1) {
        local_3 = false;
    }
    return local_3;
}