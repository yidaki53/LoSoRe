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

void FUN_24dd_0530(void);
char FUN_202c_0843(uint16_t, uint16_t);
void FUN_24dd_3639(uint16_t, uint16_t, uint8_t*, uint16_t);
void FUN_24dd_36b7(uint16_t, uint8_t*);
void FUN_24dd_04f4(void);
void FUN_24dd_3988(uint8_t, uint8_t*, uint16_t);
void FUN_24dd_38f0(uint8_t*, uint16_t);
uint16_t FUN_24dd_4654(int);
void FUN_24dd_3711(uint8_t*, uint16_t);

void FUN_1000_a816(uint8_t param_1) {
    char cVar1;
    uint16_t uVar2;
    uint8_t local_206[256];
    uint8_t local_106[256];
    int local_4 = 0x1000;
    uint16_t local_6 = 0xa821;

    FUN_24dd_0530();
    cVar1 = FUN_202c_0843(0xa80c, 0x24dd);
    if (cVar1 != '\0') {
        FUN_24dd_3639(0xa80c, 0x202c, local_106, 0);
        FUN_24dd_36b7(0x24dd, local_106);
        FUN_24dd_04f4();
        local_4 = -1;
        do {
            FUN_24dd_3988(0xff, local_206, 0);
            FUN_24dd_38f0(local_106, 0);
            FUN_24dd_04f4();
            local_4++;
        } while (local_206[0] != '\0');
        if (-1 < local_4) {
            FUN_24dd_36b7(0x24dd, local_106);
            FUN_24dd_04f4();
            uVar2 = FUN_24dd_4654(local_4);
            if (uVar2 < 0x8000) {
                local_6 = 0;
                while (true) {
                    FUN_24dd_3988(0x14, (uint16_t)param_1 * 0x15 + 0x66ec, 0);
                    FUN_24dd_38f0(local_106, 0);
                    FUN_24dd_04f4();
                    if (local_6 == uVar2) break;
                    local_6++;
                }
            }
        }
        FUN_24dd_3711(local_106, 0);
        FUN_24dd_04f4();
    }
    return;
}