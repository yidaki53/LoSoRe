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

// Function prototypes for the called functions
uint32_t FUN_24dd_4161(void);
uint32_t FUN_24dd_4654(uint32_t param_1);
void FUN_202c_165d(uint32_t param_1, uint32_t param_2, uint32_t param_3, uint32_t param_4, uint32_t param_5, uint32_t param_6, uint32_t param_7, uint32_t param_8, uint32_t param_9);
void FUN_202c_005a(uint32_t param_1, uint32_t param_2, uint32_t param_3, uint32_t param_4, uint32_t param_5, uint32_t param_6, uint32_t param_7);
void FUN_202c_1b84(uint32_t param_1, uint16_t param_2, uint16_t param_3, uint32_t param_4);
uint32_t FUN_24dd_3d80(void);

// Global variables
extern uint32_t global_6674;
extern uint32_t global_6678;
extern uint32_t global_6694;
extern uint32_t global_6698;
extern uint32_t global_669c;
extern uint32_t global_66af;

void FUN_202c(uint32_t param_1, uint32_t param_2, uint32_t param_3) {
    uint32_t local_6 = 0;
    uint32_t local_8 = 0;
    uint32_t local_16 = 0;
    uint32_t local_18 = 0;
    uint32_t local_1a = 0;
    uint32_t local_1c = 0;
    uint32_t local_1e = 0;
    uint32_t local_20 = 0;
    uint32_t local_4 = 0;
    uint32_t uVar11;
    uint32_t uVar15;
    uint32_t uVar19;
    uint32_t uVar20;
    uint32_t uVar24;
    uint32_t uVar25;
    uint32_t uVar30;
    uint32_t uVar32;
    uint32_t uVar34;
    uint32_t iVar9;
    uint32_t iVar12;
    uint32_t iVar13;
    uint32_t iVar14;
    uint32_t iVar23;
    bool bVar26;
    bool bVar7;
    char *pcVar3;
    uint32_t *puVar1;
    int *piVar2;

    uVar11 = *(uint8_t *)(global_6674 + 0x1451);
    if (uVar11 != 0) {
        iVar9 = param_3 + -7;
        iVar12 = param_2 + -7;
        uVar24 = (uint16_t)(global_6678 >> 16);
        iVar23 = (int)global_6678 + (uint)*(uint8_t *)(uVar11 + 0x1369) * 0x100;
        uVar25 = 0x24dd;
        iVar13 = FUN_24dd_4654(*(uint8_t *)(uVar11 + 0x137d));
        iVar13 = (uint)*(uint8_t *)(uVar11 + 0x1373) + iVar13;
        iVar14 = iVar13 * 0x100;
        if (*(uint8_t *)(uVar11 + 4999) & 1) {
            iVar14 = iVar14 + 1;
        }
        FUN_202c_005a(iVar14, (int)global_6678 + iVar13 * 0x10