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

void FUN_24dd_46b1(void) {
    int iVar1;
    uint32_t lVar2;
    uint32_t uVar3;
    char cVar4;
    int iVar5;

    iVar1 = *(int *)(0x24dd * 16 + 0x6414);
    lVar2 = (uint32_t)*(uint *)(0x24dd * 16 + 0x6412) * (uint32_t)uRam000246e7;
    uVar3 = (uint32_t)lVar2;
    iVar5 = *(uint *)(0x24dd * 16 + 0x6412) << 3;
    cVar4 = (char)iVar5;
    iVar5 = (int)((uint32_t)lVar2 >> 0x10) + ((char)((uint32_t)iVar5 >> 8) + cVar4) + cVar4 + iVar1 * 5;
    *(int *)(0x24dd * 16 + 0x6412) = uVar3 + 1;
    *(int *)(0x24dd * 16 + 0x6414) = ((char)((uint32_t)iVar5 >> 8) + (char)iVar1 * 4 + (char)(iVar1 << 7) + (char)iVar5) + (uint32_t)(0xfffe < uVar3);
    return;
}