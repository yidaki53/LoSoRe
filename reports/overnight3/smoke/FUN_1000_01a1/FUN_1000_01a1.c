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

extern void FUN_24dd_0530(void);
extern void FUN_24dd_39c3(uint16_t, uint16_t, uint16_t);
extern void FUN_24dd_3930(uint16_t, uint16_t);
extern void FUN_24dd_04f4(void);
extern char FUN_1e7d_018a(uint16_t, uint16_t, uint16_t, uint16_t, uint16_t, uint16_t, uint16_t, uint16_t);
extern char FUN_235c_0086(char, char, char, uint16_t);
extern void FUN_1ec2_0018(uint16_t);
extern void FUN_24dd_3a4b(uint16_t, char, uint16_t);
extern void FUN_24dd_31d8(uint16_t);
extern void FUN_24dd_3adf(uint16_t, uint16_t);
extern void FUN_24dd_3951(uint16_t, uint16_t);
extern char FUN_235c_0340(void);
extern uint16_t FUN_235c_0361(uint16_t);
extern void FUN_235c_0482(void);
extern void FUN_235c_04bc(uint16_t, uint16_t);
extern void FUN_235c_0711(uint16_t, uint16_t, uint16_t, uint16_t);
extern void FUN_235c_04f3(void);
extern void FUN_235c_0bbc(void);
extern void FUN_24dd_0116(void);

void FUN_1000_01a1(void) {
    char cVar1;
    uint16_t uVar2;
    uint16_t uVar4;
    uint16_t uVar5;
    uint16_t uVar6;
    char local_104[254];
    uint16_t uStack_6 = 0x1ac;
    int local_4 = 0x1000;

    FUN_24dd_0530();

    if (*(char *)(0x4b8) == '\0') {
        uVar4 = 0x79f0;
        FUN_24dd_39c3(0, 0, 0x24dd);
        FUN_24dd_3930(uVar4, 0);
        FUN_24dd_04f4();
    } else {
        uVar5 = 0x79f0;
        uVar4 = 0;
        FUN_24dd_39c3(0, 0xf, 0x24dd);
        FUN_24dd_3930(uVar5, uVar4);
        FUN_24dd_04f4();
        cVar1 = FUN_1e7d_018a(0x65d6, 0, 0x65d5, 0, 0x65d4, 0, 0x65d2, 0);
        if (cVar1 == '\0') {
            uVar5 = 0x79f0;
            uVar4 = 0;
            FUN_24dd_39c3(0, 0x2c, 0x1e7d);
            FUN_24dd_3930(uVar5, uVar4);
            FUN_24dd_04f4();
            uVar5 = 0x79f0;
            uVar4 = 0;
            FUN_24dd_39c3(0, 0, 0x24dd);
            FUN_24dd_3930(uVar5, uVar4);
            FUN_24dd_04f4();
            *(char *)(0x4b8) = 0;
        } else {
            cVar1 = FUN_235c_0086(*(char *)(0x65d6), *(char *)(0x65d5), *(char *)(0x65d4), *(uint16_t *)(0x65d2));
            if (cVar1 == '\0') {
                uVar5 = 0x79f0;
                uVar4 = 0;
                FUN_24dd_39c3(0, 0x4f, 0x235c);
                FUN_24dd_3930(uVar5, uVar4);
                FUN_24dd_04f4();
                uVar5 = 0x79f0;
                uVar4 = 0;
                FUN_24dd_39c3(0, 0, 0x24dd);
                FUN_24dd_3930(uVar5, uVar4);
                FUN_24dd_04f4