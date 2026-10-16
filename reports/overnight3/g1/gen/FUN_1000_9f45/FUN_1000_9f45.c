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

extern void FUN_24dd_0530();
extern uint8_t FUN_24dd_4161();
extern int FUN_24dd_4654(uint8_t);
extern void FUN_1ec2_10cf(uint8_t, uint8_t, uint8_t, uint8_t);
extern void FUN_1000_0ebe(uint16_t, uint16_t, uint8_t);
extern char FUN_1000_0c7f(uint16_t, uint16_t, uint16_t, uint16_t, uint16_t, uint16_t);
extern void FUN_202c_005a(int, int, int, int, uint16_t, int, int);
extern void FUN_235c_095c(uint8_t, uint8_t, uint16_t, uint16_t);
extern void FUN_24dd_3d80();
extern uint16_t FUN_24dd_3dbd();
extern void FUN_1000_0ac7();
extern void FUN_1000_10ec();
extern void FUN_1000_8c03();
extern void FUN_1000_5e66();
extern char FUN_1000_9e7a(uint16_t);

void FUN_1000_9f45(uint8_t param_1) {
    char *pcVar1;
    uint32_t uVar4;
    uint8_t bVar5;
    char cVar6;
    int iVar7;
    int iVar8;
    uint32_t uVar9;
    int iVar10;
    int iVar11;
    int iVar12;
    uint16_t uVar13;
    uint32_t local_a;
    uint32_t local_8;
    int local_6;
    uint32_t local_4;

    FUN_24dd_0530();
    if (*(char *)0x66af == '\0') {
        local_8 = 0;
        while (true) {
            local_a = 3;
            while (true) {
                uVar4 = *(uint32_t *)((int)*(uint32_t *)0x6674 + local_a * 4);
                bVar5 = *(uint8_t *)((int)uVar4 + local_8);
                if ((0xa3 < bVar5) && (bVar5 < 0xa8)) {
                    uVar4 = *(uint32_t *)((int)*(uint32_t *)0x6674 + local_a * 4);
                    pcVar1 = (char *)((int)uVar4 + local_8);
                    *pcVar1 = *pcVar1 + -4;
                }
                if (local_a == 0x15d) break;
                local_a = local_a + 1;
            }
            if (local_8 == 500) break;
            local_8 = local_8 + 1;
        }
    } else {
        local_8 = 0;
        while (true) {
            local_a = 3;
            while (true) {
                iVar10 = 0x20;
                bVar5 = FUN_24dd_4161();
                if ((*(uint8_t *)(iVar10 + 0x14e0) & bVar5) != 0) {
                    iVar10 = 0x20;
                    bVar5 = FUN_24dd_4161();
                    if ((*(uint8_t *)(iVar10 + 0x6604) & bVar5) != 0) {
                        uVar4 = *(uint32_t *)((int)*(uint32_t *)0x6674 + local_a * 4);
                        pcVar1 = (char *)((int)uVar4 + local_8);
                        *pcVar1 = *pcVar1 + '\x04';
                    }
                }
                if (local_a == 0x15d) break;
                local_a = local_a + 1;
            }
            if (local_8 == 500) break;
            local_8 = local_8 + 1;
        }
    }
    local_4 = 0;
    while (true) {
        FUN_1ec2_10cf(0, 0, 0, local_4 & 0xff);
        if (local_4 == 0xff) break;
        local_4 = local_4 + 1;