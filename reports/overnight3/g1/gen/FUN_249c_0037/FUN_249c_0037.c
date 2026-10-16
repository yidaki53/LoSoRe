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

void FUN_249c_0013(void *stack_ptr);
void FUN_249c_0000(uint16_t param1, uint16_t param2);
void FUN_24dd_3930(uint16_t seg, uint16_t ds);
void FUN_24dd_04f4(void);

void __stdcall16far FUN_249c_0037(uint16_t ds, uint16_t seg, byte *param_1, byte param_2, byte param_3) {
    byte local_102[256];
    byte *pbVar1 = local_102;
    byte *pbVar5 = param_1;
    uint uVar4 = (uint)local_102[0];
    byte local_10a;
    byte local_108;
    byte local_105;
    char local_103;
    byte bVar2;

    local_102[0] = *param_1;
    for (; uVar4 != 0; uVar4--) {
        *pbVar1++ = *pbVar5++;
    }
    FUN_249c_0013((void *)0xfffe);
    local_10a = (byte)(((uint)param_2 * 0x50 + (uint)param_3) * 2);
    uint16_t uVar3 = (uint16_t)((uint)local_10a >> 8);
    FUN_249c_0000(((uint16_t)uVar3 << 8) | param_2, ((uint16_t)uVar3 << 8) | param_3);
    bVar2 = local_102[0];
    local_103 = '\0';
    if (local_102[0] != 0) {
        local_108 = 1;
        while (true) {
            if (local_103 == '\0') {
                if (local_102[local_108] == 0) {
                    local_103 = '\x01';
                } else {
                    *(byte *)(seg * 16 + local_10a) = local_102[local_108];
                    *(byte *)(seg * 16 + local_10a + 1) = local_105;
                    local_10a += 2;
                }
            } else if (local_103 == '\x01') {
                local_103 = '\x02';
                FUN_249c_0013((void *)0xfffe);
            } else if (local_103 == '\x02') {
                local_103 = '\0';
                FUN_249c_0013((void *)0xfffe);
            }
            if (local_108 == bVar2) break;
            local_108++;
        }
    }
    FUN_249c_0000(((uint16_t)((uint)param_3 + (uint)local_102[0] >> 8) << 8) | param_2, (uint16_t)param_3 + (uint16_t)local_102[0]);
    FUN_24dd_3930(0x79f0, ds);
    FUN_24dd_04f4();
}