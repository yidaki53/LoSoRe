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

void __stdcall16far FUN_1ec2_155e(uint16_t param_1) {
    uint8_t local_3 = 0;
    
    while (true) {
        uint16_t uVar2 = (uint16_t)(uint8_t)local_3;
        uint16_t uVar6 = uVar2 * 3;
        uint16_t uVar8 = uVar2 * 3 + 1;
        uint16_t uVar4 = uVar2 * 3 + 2;
        
        uint16_t *ptr1 = (uint16_t *)((int16_t)param_1 * 16 + uVar6);
        uint16_t *ptr2 = (uint16_t *)((int16_t)param_1 * 16 + uVar8);
        uint16_t *ptr3 = (uint16_t *)((int16_t)param_1 * 16 + uVar4);
        
        uint8_t *data1 = (uint8_t *)((int16_t)param_1 * 16 + uVar2 * 4);
        uint8_t *data2 = (uint8_t *)((int16_t)param_1 * 16 + uVar2 * 4 + 1);
        
        FUN_2971_65df(*data1, *data2, *ptr1, *ptr2, *ptr3, local_3);
        
        if (local_3 == 0xff) break;
        
        local_3++;
    }
}