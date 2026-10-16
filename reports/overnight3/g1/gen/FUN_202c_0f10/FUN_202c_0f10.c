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

extern void FUN_24dd_3e95(uint16_t, uint16_t);
extern void FUN_24dd_3f14(uint16_t, uint16_t);
extern char FUN_202c_0b0e(void*, char*, uint16_t);
extern byte FUN_24dd_4161(void);
extern void FUN_24dd_46e9(void);
extern int FUN_24dd_4654(uint16_t);
extern void FUN_202c_005a(int, int, int, int, uint16_t, int, int);
extern char FUN_202c_0a74(uint16_t, int, int);
extern void FUN_202c_032d(int, int, int, int, int);

void __cdecl16far FUN_202c_0f10(void) {
    char local_118[250];
    uint local_1e;
    int local_1c;
    int local_1a;
    int local_10;
    int local_e;
    int local_c;
    int local_a;
    int local_8;
    int local_6;
    uint local_4;
    char *pcVar1;
    undefined4 uVar2;
    byte bVar3;
    char cVar4;
    int iVar5;
    int iVar6;
    int iVar7;
    undefined2 uVar8;
    undefined2 unaff_SS;
    undefined2 unaff_DS;
    int iVar9;
    undefined1 *puVar10;

    if (*(char *)(0x66a9) == '\0') {
        puVar10 = local_118;
        FUN_24dd_3e95(0x672e, unaff_DS);
        FUN_24dd_3f14(0xf0b, 0x24dd);
        cVar4 = FUN_202c_0b0e(&stack0xfffe, puVar10, unaff_SS);
        if (cVar4 != '\0') {
            local_e = 0;
            while (true) {
                local_10 = 3;
                while (true) {
                    if (*(char *)(0x66af) != '\0') {
                        iVar6 = 0x20;
                        bVar3 = FUN_24dd_4161();
                        if ((*(byte *)(iVar6 + 0x14e0) & bVar3) != 0) {
                            iVar6 = 0x20;
                            bVar3 = FUN_24dd_4161();
                            if ((*(byte *)(iVar6 + 0x6604) & bVar3) != 0) {
                                uVar2 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_10 * 4);
                                pcVar1 = (char *)((int)uVar2 + local_e);
                                *pcVar1 = *pcVar1 + '\x04';
                            }
                        }
                    }
                    uVar2 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_10 * 4);
                    bVar3 = *(byte *)((int)uVar2 + local_e);
                    if ((0xb < bVar3) && (bVar3 < 0x13)) {
                        iVar6 = 0x20;
                        bVar3 = FUN_24dd_4161();
                        if (((*(byte *)(iVar6 + 0x14a0) & bVar3) != 0) &&
                            (uVar2 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_10 * 4),
                             pcVar1 = (char *)((int)uVar2 + local_e), *pcVar1 = *pcVar1 + -2,
                             uVar2 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_10 * 4),
                             *(byte *)((int)uVar2 + local_e) < 0xc)) {
                            uVar2 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_10 * 4);
                            *(undefined1 *)((int)uVar2 + local_e) = 0xc;
                        }
                    }
                    if (local_10 == 0x15d) break;
                    local_10 = local_10 + 1;
                }
                if (local_e == 500