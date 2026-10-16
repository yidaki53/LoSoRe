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
void FUN_24dd_48e1(uint32_t, uint32_t, uint16_t, uint32_t, uint16_t);
void FUN_1ec2_0810(uint32_t, uint16_t, uint16_t);
void FUN_24dd_3d68(uint32_t, uint32_t, uint16_t, uint32_t, uint16_t);

void FUN_1000_05eb(uint8_t param_1) {
    uint16_t ds = 0; // Assuming DS is always 0 for simplicity, as it's not used in calculations

    FUN_24dd_0530();
    FUN_24dd_48e1(3, (uint32_t)*(uint8_t *)(param_1 + 0x68) * 3 + 0x5826, ds, (uint32_t)param_1 * 3 + 0x66d8, ds);
    FUN_1ec2_0810(*(uint8_t *)(param_1 + 0x68), 0x5826, ds);

    int16_t local_4 = -2;
    while (true) {
        *(uint8_t *)(((uint32_t)*(uint8_t *)(param_1 + 0x68) + local_4) * 3 + 0x5826) =
            (uint8_t)((uint32_t)*(uint8_t *)((uint32_t)param_1 * 3 + 0x66d8) * (uint32_t)*(uint8_t *)(local_4 + 0x1a4) >> 6);
        *(uint8_t *)(((uint32_t)*(uint8_t *)(param_1 + 0x68) + local_4) * 3 + 0x5827) =
            (uint8_t)((uint32_t)*(uint8_t *)((uint32_t)param_1 * 3 + 0x66d9) * (uint32_t)*(uint8_t *)(local_4 + 0x1a4) >> 6);
        *(uint8_t *)(((uint32_t)*(uint8_t *)(param_1 + 0x68) + local_4) * 3 + 0x5828) =
            (uint8_t)((uint32_t)*(uint8_t *)((uint32_t)param_1 * 3 + 0x66da) * (uint32_t)*(uint8_t *)(local_4 + 0x1a4) >> 6);
        FUN_1ec2_0810((uint32_t)*(uint8_t *)(param_1 + 0x68) + local_4, 0x5826, ds);
        if (local_4 == -1) break;
        local_4++;
    }

    local_4 = 1;
    while (true) {
        *(uint8_t *)(((uint32_t)*(uint8_t *)(param_1 + 0x68) + local_4) * 3 + 0x5826) =
            (uint8_t)((uint32_t)*(uint8_t *)(local_4 + 0x1a3) * 0x3f +
                       (uint32_t)*(uint8_t *)((uint32_t)param_1 * 3 + 0x66d8) *
                       (0x3f - (uint32_t)*(uint8_t *)(local_4 + 0x1a3)) >> 6);
        *(uint8_t *)(((uint32_t)*(uint8_t *)(param_1 + 0x68) + local_4) * 3 + 0x5827) =
            (uint8_t)((uint32_t)*(uint8_t *)(local_4 + 0x1a3) * 0x3f +
                       (uint32_t)*(uint8_t *)((uint32_t)param_1 * 3 + 0x66d9) *
                       (0x3f - (uint32_t)*(uint8_t *)(local_4 + 0x1a3)) >> 6);
        *(uint8_t *)(((uint32_t)*(uint8_t *)(param_1 + 0x68) + local_4) * 3 + 0x5828) =
            (