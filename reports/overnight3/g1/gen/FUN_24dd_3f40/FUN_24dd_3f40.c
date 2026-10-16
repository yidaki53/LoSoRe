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

byte * __stdcall16far FUN_24dd_3f40(byte *param_1, byte *param_2) {
    byte *pbVar1;
    int iVar2;
    int iVar3;
    uint uVar4;
    byte *pbVar5;
    byte *pbVar6;
    byte *pbVar7;
    bool bVar10;

    if (*param_2 != 0) {
        uVar4 = (uint)*param_2;
        if (uVar4 <= *param_1) {
            iVar2 = (*param_1 - uVar4) + 1;
            pbVar7 = param_1 + 1;
            pbVar6 = pbVar7;
            do {
                pbVar5 = param_2 + 1;
                bVar10 = pbVar6 == (byte *)0x0;
                do {
                    if (iVar2 == 0) break;
                    iVar2 = iVar2 + -1;
                    pbVar1 = pbVar7;
                    pbVar7 = pbVar7 + 1;
                    bVar10 = *pbVar5 == *pbVar1;
                } while (!bVar10);
                if (!bVar10) {
                    return (byte *)0x0;
                }
                iVar3 = uVar4 - 1;
                bVar10 = iVar3 == 0;
                pbVar6 = pbVar7;
                do {
                    pbVar5 = pbVar5 + 1;
                    if (iVar3 == 0) break;
                    iVar3 = iVar3 + -1;
                    pbVar1 = pbVar6;
                    pbVar6 = pbVar6 + 1;
                    bVar10 = *pbVar5 == *pbVar1;
                } while (bVar10);
                if (bVar10) {
                    return pbVar7 + (-1 - (int)(byte *)param_1);
                }
                pbVar6 = param_2 + 1;
            } while (true);
        }
    }
    return (byte *)0x0;
}