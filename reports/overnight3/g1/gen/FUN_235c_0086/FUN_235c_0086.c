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

extern uint FUN_235c_0036(void);
extern void FUN_235c_0000(void);
extern void FUN_235c_001a(void);
extern uint16_t FUN_24dd_462e(void);
extern void FUN_24dd_31d8(void);

uint __stdcall16far FUN_235c_0086(void) {
    uint uVar2;
    uint16_t uVar3;
    uint16_t uVar4;
    uint16_t in_BX;
    int unaff_SI;
    uint16_t unaff_SS;
    uint16_t unaff_DS;
    uint8_t uVar5;

    *(uint16_t*)(0x67d0) = in_stack_0000000a + 6;
    *(uint16_t*)(0x67d2) = in_stack_0000000a + 10;
    *(uint16_t*)(0x67d4) = in_stack_0000000a + 0xc;
    *(uint16_t*)(0x67d6) = in_stack_0000000a + 0xe;
    uVar2 = FUN_235c_0036();
    if ((char)uVar2 == '\0') {
        return uVar2 & 0xff00;
    }
    FUN_235c_0000();
    FUN_235c_001a();
    uVar4 = 0;
    uVar3 = FUN_24dd_462e();
    *(uint16_t*)(0x67c6) = uVar3;
    *(uint16_t*)(0x67c8) = in_BX;
    *(uint16_t*)(0x67ca) = uVar4;
    FUN_24dd_31d8();
    FUN_235c_001a();
    uVar5 = 0;
    // Assuming swi() calls are replaced with appropriate DOS interrupt calls
    // For example, swi(0x37) could be replaced with a call to int 0x37
    // Similarly for swi(0x3c) and swi(0x3a)
    // These would need to be implemented or replaced with appropriate DOS calls
    // For the sake of this example, we'll leave them as comments
    // asm("int $0x37");
    // asm("int $0x3c");
    // asm("int $0x3a");
    uVar2 = *(uint16_t*)(&stack0x3201 + unaff_SI);
    *(uint16_t*)(&stack0x3201 + unaff_SI) = ((uint16_t)(CONCAT12(uVar5, uVar2) >> 0xc) | uVar2 << 5);
    // WARNING: Bad instruction - Truncating control flow here
    // halt_baddata();
    return 0; // Placeholder return value
}