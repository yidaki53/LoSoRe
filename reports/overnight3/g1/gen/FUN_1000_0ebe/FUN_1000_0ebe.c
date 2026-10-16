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
int FUN_24dd_4654(int);
char FUN_1000_0c7f(int, int, uint16_t, uint16_t, int, int);
void FUN_202c_005a(int, int, int, int, uint16_t, int, int);
void FUN_202c_14b6(int, int, int, int, int, int, int, char);
byte FUN_24dd_4161(void);

void FUN_1000_0ebe(uint16_t param_1, uint16_t param_2, char param_3) {
    char *pcVar1;
    uint4 uVar2;
    char cVar3;
    byte bVar4;
    int iVar5;
    int iVar6;
    int iVar7;
    int iVar8;
    int iVar9;
    int iVar10;
    int iVar11;
    uint16_t uVar12;
    uint local_b;
    uint local_9;
    char local_3;

    local_3 = 0x10;
    FUN_24dd_0530();
    if (param_3 == '\0') {
        local_3 = 0x15;
    } else if (param_3 == '\x01') {
        local_3 = 0x16;
    }
    do {
        iVar5 = FUN_24dd_4654(0x1f2);
        iVar6 = FUN_24dd_4654(0x154);
        cVar3 = FUN_1000_0c7f(0xff60, 0xff60, param_1, param_2, iVar6 + 5, iVar5 + 3);
    } while (cVar3 == '\0');
    iVar7 = iVar5 + -4;
    iVar8 = iVar6 + -2;
    uVar12 = (uint16_t)((uint32_t)*(uint32_t *)0x6678 >> 0x10);
    iVar11 = (int)*(uint32_t *)0x6678 + (uint)*(uint8_t *)0x136a * 0x100;
    iVar9 = FUN_24dd_4654(*(uint8_t *)0x137e);
    iVar10 = ((uint)*(uint8_t *)0x1374 + iVar9) * 0x100;
    if (*(char *)0x1388 == '\x01') {
        iVar10 = iVar10 + 1;
    }
    FUN_202c_005a(iVar10, (int)*(uint32_t *)0x6678 + ((uint)*(uint8_t *)0x1374 + iVar9) * 0x100,
                (int)((uint32_t)*(uint32_t *)0x6678 >> 0x10), iVar11, uVar12, iVar8, iVar7);
    if (*(char *)0x66af != '\0') {
        local_9 = iVar5 - 7;
        if ((int)local_9 <= (int)(iVar5 + 0xdU)) {
            do {
                if ((local_9 < 0x8000) && ((int)local_9 < 0x1f8)) {
                    local_b = iVar6 - 5;
                    if ((int)local_b <= (int)(iVar6 + 0xfU)) {
                        do {
                            if ((local_b < 0x8000) && ((int)local_b < 0x15e)) {
                                iVar7 = 0x20;
                                bVar4 = FUN_24dd_4161();
                                if ((*(uint8_t *)(iVar7 + 0x14e0) & bVar4) != 0) {
                                    iVar7 = 0x20;
                                    bVar4 = FUN_24dd_4161();
                                    if ((*(uint8_t *)(iVar7 + 0x6604) & bVar4) != 0) {
                                        uVar2 = *(uint32_t *)((int)*(uint32_t *)0x6674 + local_b * 4);
                                        pcVar1 = (char *)((int)uVar2 + local_9);
                                        *pcVar1