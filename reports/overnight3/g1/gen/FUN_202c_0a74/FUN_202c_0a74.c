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

uint8_t FUN_24dd_4161(void);

uint8_t FUN_202c_0a74(int param_1, int param_2, int param_3) {
    uint8_t bVar1;
    int iVar2;
    int local_8;
    int local_6;

    if (param_3 <= param_3 + param_1) {
        local_6 = param_3;
        while (true) {
            if (param_2 <= param_2 + param_1) {
                local_8 = param_2;
                while (true) {
                    iVar2 = 0x20;
                    bVar1 = FUN_24dd_4161();
                    if (((((*(uint8_t *)(iVar2 + 0x14a0) & bVar1) != 0) && (-1 < local_8)) && (local_8 < 0x15e))
                        && ((-1 < local_6 && (local_6 < 0x1f8)))) {
                        return 0;
                    }
                    if (local_8 == param_2 + param_1) break;
                    local_8 = local_8 + 1;
                }
            }
            if (local_6 == param_3 + param_1) break;
            local_6 = local_6 + 1;
        }
    }
    return 1;
}