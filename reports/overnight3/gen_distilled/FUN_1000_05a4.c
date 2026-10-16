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

void __cdecl16far FUN_24dd_0530(void);
void __cdecl16far FUN_235c_0f1d(uint16_t);
void __cdecl16far FUN_235c_032e(void);
void __cdecl16far FUN_235c_08e4(uint16_t, uint16_t);
void __cdecl16far FUN_235c_04a2(void);

void __cdecl16far FUN_1000_05a4(void) {
    uint16_t uVar1;
    int local_4;

    FUN_24dd_0530();
    if (*(char *)(0x4b8) != '\0') {
        FUN_235c_0f1d(0x235c);
        FUN_235c_032e();
        local_4 = 1;
        while (true) {
            uVar1 = (uint16_t)(local_4 * 4) + 0x6734;
            FUN_235c_08e4(uVar1, 0x1000);
            if (local_4 == 0x1e) break;
            local_4++;
        }
        FUN_235c_04a2();
    }
    return;
}