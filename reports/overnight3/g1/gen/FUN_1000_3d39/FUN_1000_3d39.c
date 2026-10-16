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

extern void FUN_24dd_0530();
extern void FUN_24dd_3d80();
extern int FUN_24dd_3dbd();
extern bool FUN_24dd_4161();
extern void FUN_202c_1b84(uint16_t, uint16_t, uint16_t, uint8_t);
extern void FUN_202c_04d5(int, int, int, int, int);
extern void FUN_1000_0be1(uint16_t, uint16_t, uint16_t, uint16_t, uint16_t, uint16_t);
extern char FUN_1000_0d70(uint16_t, uint16_t, uint8_t, uint8_t);
extern int FUN_24dd_4654(int);
extern void FUN_235c_0a1e(uint8_t);
extern void FUN_235c_095c(int, uint16_t, uint16_t, uint16_t);
extern void FUN_202c_165d(uint16_t, uint16_t, uint16_t, uint16_t, uint16_t, uint16_t, uint16_t, uint16_t, uint16_t);
extern void FUN_202c_005a(int, int, int, int, uint16_t, int, int);

void FUN_1000_3d39(int param_1) {
    uint32_t *puVar1;
    uint32_t *puVar2;
    char *pcVar3;
    uint32_t uVar4;
    bool bVar5;
    uint8_t bVar6;
    uint8_t bVar7;
    char cVar8;
    uint16_t uVar9;
    uint16_t uVar10;
    uint32_t uVar11;
    int iVar12;
    int iVar13;
    uint32_t uVar14;
    uint32_t uVar15;
    uint32_t uVar16;
    int iVar17;
    int iVar18;
    uint32_t *puVar19;
    int iVar20;
    uint16_t uVar21;
    bool bVar22;
    uint16_t uVar23;
    uint16_t uVar24;
    uint16_t uVar25;
    uint16_t uVar26;
    uint32_t *local_1f;
    int local_18;
    uint32_t local_c;
    uint32_t local_a;
    uint32_t local_8;
    uint32_t local_6;

    FUN_24dd_0530();
    uVar21 = (uint16_t)((*(uint32_t *)0x6694 >> 16) & 0xFFFF);
    puVar19 = (uint32_t *)((*(uint32_t *)0x6694 & 0xFFFF) + param_1 * 0x14);
    local_1f = (uint32_t *)(((uint32_t)uVar21 << 16) | (uint32_t)puVar19);
    bVar6 = (uint8_t)(puVar19[9] & 0x7F);
    bVar22 = false;
    uVar11 = puVar19[4];
    uVar14 = puVar19[5];
    puVar1 = puVar19;
    uVar15 = *puVar1;
    *puVar1 = *puVar1 + uVar11;
    puVar19[1] = puVar19[1] + uVar14 + (uint32_t)((uVar15 + uVar11) < uVar15);
    uVar11 = puVar19[6];
    uVar14 = puVar19[7];
    puVar1 = puVar19 + 2;
    uVar15 = *puVar1;
    *puVar1 = *puVar1 + uVar11;
    puVar19[3] = puVar19[3] + uVar14 + (uint32_t)((uVar15 + uVar11) < uVar15);
    bVar5 = false;
    if (*(char *)(bVar6 + 0