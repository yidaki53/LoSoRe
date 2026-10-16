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

void FUN_1ec2_10cf(uint8_t, uint8_t, uint8_t, uint8_t);

void __stdcall16far FUN_1ec2_0810(uint8_t param_1, uint8_t *param_2) {
    uint8_t local_302[768];
    uint8_t *puVar4 = param_2;
    uint8_t *puVar5 = local_302;

    for (int iVar3 = 0x300; iVar3 != 0; iVar3--) {
        *puVar5 = *puVar4;
        puVar4++;
        puVar5++;
    }

    FUN_1ec2_10cf(local_302[(uint)param_1 * 3 + 2], local_302[(uint)param_1 * 3 + 1],
                local_302[(uint)param_1 * 3], param_1);
}