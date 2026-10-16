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
char FUN_1000_0d70(uint, uint, uint, uint);
void FUN_24dd_3d80(void);
uint FUN_24dd_3dbd(void);
uint FUN_24dd_4654(uint);
void FUN_202c_165d(uint, uint, uint, uint, uint, uint, uint, uint, uint);
void FUN_202c_1b84(uint, uint, uint, uint);
void FUN_235c_0a1e(uint);
void FUN_235c_095c(uint, uint, uint, uint);
void FUN_202c_14b6(uint, uint, uint, uint, uint, uint, uint, uint);
void FUN_202c_005a(uint, uint, uint, uint, uint, uint, uint);

// Global variables
extern uint16_t *g_6520;
extern uint16_t *g_6670;
extern uint16_t *g_6674;
extern uint16_t *g_6678;
extern uint16_t *g_4b8;
extern uint16_t *g_4b6;
extern uint16_t *g_66af;

void complex_function(uint16_t *puVar20, uint16_t *bVar5) {
    bool bVar26 = false;
    char cVar7;
    int iVar17;
    uint uVar16;
    uint uVar13;
    uint uVar14;
    uint uVar23;
    uint uVar24;
    uint uVar27;
    uint uVar28;
    uint uVar29;
    uint uVar30;
    int iVar18;
    int iVar19;
    int iVar21;
    int local_8 = 0;
    int local_6 = 0;
    int local_1d;
    int local_1f;

    // Check conditions and update variables
    if (*(char *)(bVar5 + 0x117d) == '\0') {
        *(char *)((int)puVar20 + 0x11) = *(char *)((int)puVar20 + 0x11) + '\x01';
        if (*(byte *)(bVar5 + 0x1155) < *(byte *)((int)puVar20 + 0x11)) {
            *(undefined1 *)((int)puVar20 + 0x11) = 0;
        }
    } else {
        if (((int)puVar20[5] < 0) &&
            (*(char *)((int)puVar20 + 0x11) = *(char *)((int)puVar20 + 0x11) + -1,
             *(char *)((int)puVar20 + 0x11) == -1)) {
            *(undefined1 *)((int)puVar20 + 0x11) = *(undefined1 *)(bVar5 + 0x1155);
        }
        if (((0 < (int)puVar20[5]) || ((-1 < (int)puVar20[5] && (puVar20[4] != 0)))) &&
            (*(char *)((int)puVar20 + 0x11) = *(char *)((int)puVar20 + 0x11) + '\x01',
             *(byte *)(bVar5 + 0x1155) < *(byte *)((int)puVar20 + 0x11))) {
            *(undefined1 *)((int)puVar20 + 0x11) = 0;
        }
    }

    if (*(char *)(bVar5 + 0xfed) == '\0') {
        if (*(char *)(bVar5 + 0xf25) == '\x01') {
            bVar26 = true;
        } else {
            puVar20[4] = 0;
            puVar20[5] = 0;
            puVar20[6] = 0;
            puVar20[7] = 0;
        }
    }

    if ((0 <