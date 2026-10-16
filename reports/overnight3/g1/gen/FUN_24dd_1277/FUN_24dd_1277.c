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

void FUN_24dd_2361();
void FUN_24dd_0e57();
void FUN_24dd_060f();
void FUN_24dd_05fd();

void FUN_24dd_1277(int *param_1, uint *param_2, uint *param_3) {
    uint local_c = param_3[3];
    uint local_e = param_3[2];
    uint local_10 = param_3[1];
    uint local_12 = *param_3;
    uint uVar6 = param_3[5];
    uint uVar7 = param_2[5];
    uint uVar23 = param_2[4];
    uint uVar18 = param_3[4];
    bool bVar26 = uVar23 < 0x4001;
    if ((int)uVar23 < 0x4001) {
        bVar26 = uVar18 < 0x4001;
        if ((int)uVar18 < 0x4001) {
            if (-0x3fff < (int)uVar23) {
                if ((int)uVar18 < -0x3ffe) goto LAB_24dd_12db;
                int local_4 = uVar18 - uVar23;
                if (local_4 < 0x4001) {
                    if (local_4 < -0x3ffe) {
                        FUN_24dd_2361();
                    } else {
                        uVar23 = param_2[3];
                        bVar26 = uVar23 < local_c;
                        uVar18 = local_c;
                        if (uVar23 <= local_c) {
                            bVar26 = local_c < uVar23;
                            uVar18 = local_c - uVar23;
                        }
                        uint uVar8 = (uint)(((uint16_t)uVar18 << 8) | local_e) / uVar23;
                        uVar18 = uVar8 + 1;
                        uint uVar9 = uVar18 + bVar26;
                        bool bVar13 = (uVar23 <= local_c) + (0xfffe < uVar8 || (uVar18 + bVar26 < uVar18));
                        uint uVar14 = (uint)bVar13;
                        uVar18 = *param_2;
                        uVar8 = param_2[1];
                        if (uVar14 != 0) {
                            do {
                                bVar26 = local_12 < uVar18;
                                local_12 = local_12 - uVar18;
                                bVar26 = local_10 < uVar8;
                                uint uVar19 = local_10 - uVar8;
                                local_10 = uVar19 - bVar26;
                                uVar19 = (uint)(bVar26 || uVar19 < bVar26);
                                bVar26 = local_e < param_2[2];
                                uint uVar15 = local_e - param_2[2];
                                local_e = uVar15 - uVar19;
                                local_c = (local_c - uVar23) - (uint)(bVar26 || uVar15 < uVar19);
                                uVar14 = uVar14 - 1;
                            } while (uVar14 != 0);
                        }
                        uint local_14 = (uint)((ulong)uVar18 * (ulong)uVar9);
                        ulong uVar2 = (ulong)uVar8 * (ulong)uVar9 + ((ulong)uVar18 * (ulong)uVar9 >> 16);
                        uVar23 = (uint)uVar2;
                        ulong lVar5 = (ulong)param_2[2] * (ulong)uVar9 + (uVar2 >> 16);
                        uVar18 = (uint)lVar5;
                        uint uVar19 = (uint)((ulong)lVar5 >> 16);
                        uVar14 = (uint)((ulong)uVar9 * (ulong)param_2[3]);
                        uVar8 = uVar14 + uVar19;
                        bVar26 = uVar23 < local_12;
                        local_12 = uVar23 - local_12;
                        uVar23 = (uint