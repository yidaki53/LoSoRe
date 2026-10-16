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

extern void FUN_24dd_3711(uint16_t, uint16_t);
extern void FUN_24dd_01f0(void);
extern void FUN_24dd_01fe(void);
extern void FUN_24dd_0218(void);
extern void FUN_24dd_0232(void);

void __cdecl16far FUN_24dd_0116(void) {
    uint16_t in_AX;
    int iVar2;
    char *pcVar3;
    uint16_t uVar4;

    uVar4 = 0x2971;
    *(uint16_t *)(0x2971 * 16 + 0x6406) = in_AX;
    *(uint16_t *)(0x2971 * 16 + 0x6408) = 0;
    *(uint16_t *)(0x2971 * 16 + 0x640a) = 0;
    pcVar3 = (char *)*(uint16_t *)(0x2971 * 16 + 0x6402);
    if ((int)((*(uint32_t *)(0x2971 * 16 + 0x6402) >> 16) & 0xFFFF) == 0 && pcVar3 == (char *)0x0) {
        *(uint16_t *)(0x2971 * 16 + 0x6408) = 0;
        FUN_24dd_3711(0x78f0, 0x2971);
        FUN_24dd_3711(0x79f0, 0x2971);
        iVar2 = 0x13;
        do {
            // Assuming swi(0x21) is a BIOS interrupt call, replaced with a placeholder
            // This part is platform-specific and may need to be implemented differently
            // For example, using inline assembly or a specific library function
            // Here, we just call a placeholder function to represent the interrupt call
            FUN_24dd_01f0(); // Placeholder for interrupt call
            iVar2 = iVar2 - 1;
        } while (iVar2 != 0);
        if (*(int *)0x6408 != 0 || *(int *)0x640a != 0) {
            FUN_24dd_01f0();
            FUN_24dd_01fe();
            FUN_24dd_01f0();
            FUN_24dd_0218();
            FUN_24dd_0232();
            FUN_24dd_0218();
            pcVar3 = (char *)0x260;
            FUN_24dd_01f0();
        }
        // Placeholder for interrupt call
        FUN_24dd_01f0();
        for (; *pcVar3 != '\0'; pcVar3 = pcVar3 + 1) {
            FUN_24dd_0232();
        }
        return;
    }
    *(uint16_t *)(0x2971 * 16 + 0x6402) = (char *)0x0;
    *(uint16_t *)(0x2971 * 16 + 0x6410) = 0;
    return;
}