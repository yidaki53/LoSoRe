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
#include <stdbool.h>

extern void FUN_24dd_3b22(void *, uint16_t, uint16_t, uint16_t);
extern void FUN_24dd_3b5d(int, uint16_t, uint16_t);
extern void FUN_24dd_04f4(void);
extern void FUN_24dd_486c(uint16_t, uint16_t);
extern void FUN_24dd_3c48(int, int, int, void *, uint16_t, uint16_t, uint16_t);
extern char FUN_235c_0502(void *, uint16_t, void *, uint16_t);
extern void FUN_24dd_3cb0(uint16_t, uint16_t, uint16_t, uint16_t);
extern void FUN_24dd_0116(void);

void FUN_235c_056f(uint16_t ds, byte *param_1) {
    bool bVar1;
    byte *pbVar2;
    char cVar3;
    uint16_t uVar4;
    uint uVar5;
    uint16_t extraout_DX;
    uint16_t uVar6;
    byte *pbVar7;
    int local_120;
    int local_11e;
    byte local_11c[8];
    uint16_t local_114;
    uint16_t local_112;
    uint16_t local_110;
    uint16_t local_10e;
    byte local_10c[8];
    int local_104;
    byte local_102[256];

    pbVar7 = (byte *)param_1;
    pbVar2 = local_102;
    local_102[0] = *param_1;
    for (uVar5 = (uint)*param_1; pbVar2 = pbVar2 + 1, pbVar7 = pbVar7 + 1, uVar5 != 0; uVar5 = uVar5 - 1) {
        *pbVar2 = *pbVar7;
    }
    if (*(char *)(0x7690 + ds * 16) == '\0') {
        FUN_24dd_3b22(local_102, ds, 0x7792, ds);
        FUN_24dd_3b5d(1, 0x7792, ds);
        FUN_24dd_04f4();
        FUN_24dd_486c(0x7792, ds);
        uVar6 = extraout_DX;
        uVar4 = FUN_24dd_04f4();
        *(uint16_t *)(0x7812 + ds * 16) = uVar4;
        *(uint16_t *)(0x7814 + ds * 16) = uVar6;
    } else {
        local_120 = 1;
        while (true) {
            if ((int)(uint)local_102[0] < local_120) {
                local_10c[local_120 + -1] = 0;
            } else {
                local_10c[local_120 + -1] = local_102[local_120];
            }
            if (local_120 == 8) break;
            local_120 = local_120 + 1;
        }
        FUN_24dd_3b22((void *)(0x7692 + ds * 16), ds, 0x7792, ds);
        FUN_24dd_3b5d(1, 0x7792, ds);
        FUN_24dd_04f4();
        FUN_24dd_3c48(0, 0, 2, &local_104, ds, 0x7792, ds);
        FUN_24dd_04f4();
        bVar1 = false;
        local_11e = 0;
        while ((!bVar1 && (local_11e < local_104))) {
            local_11e = local_11e + 1;
            FUN_24dd_3c48(0, 0, 0x10, local_11c, ds,