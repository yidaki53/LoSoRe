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
extern void FUN_1ec2_10ea(int, int, int);
extern void FUN_1000_5e66(void);
extern void FUN_1ec2_0d5d(int, int, int, int, int, int, int, int);
extern void FUN_1ec2_13e9(int, int, int, int, int, int, int, int);
extern void FUN_24dd_4905(int, int, int);
extern void FUN_1ec2_0000(int, int, int, int);
extern uint16_t FUN_202c_0673(int, int);
extern void FUN_1ec2_0d88(int, int, uint16_t, int);
extern void FUN_1000_bcca(void);
extern void FUN_24dd_3e95(int, int);
extern void FUN_24dd_3f14(int, int);
extern void FUN_1000_bfd7(void*);
extern void FUN_1000_a9c1(void);
extern void FUN_1000_ab94(void);
extern void FUN_1000_ccf1(void*, int);
extern void FUN_1ec2_13c5(void);
extern void FUN_1ec2_1619(int);

uint16_t* seg_65d7 = (uint16_t*)0x65d7;
uint16_t* seg_6684 = (uint16_t*)0x6684;
uint16_t* seg_6664 = (uint16_t*)0x6664;
uint16_t* seg_783c = (uint16_t*)0x783c;
uint16_t* seg_78db = (uint16_t*)0x78db;
uint16_t* seg_4b8 = (uint16_t*)0x4b8;
uint16_t* seg_67a0 = (uint16_t*)0x67a0;
uint16_t* seg_679c = (uint16_t*)0x679c;
uint16_t* seg_67a4 = (uint16_t*)0x67a4;
uint16_t* seg_7857 = (uint16_t*)0x7857;
uint16_t* seg_785a = (uint16_t*)0x785a;
uint16_t* seg_7861 = (uint16_t*)0x7861;
uint16_t* seg_78de = (uint16_t*)0x78de;
uint16_t* seg_78e0 = (uint16_t*)0x78e0;
uint16_t* seg_66aa = (uint16_t*)0x66aa;
uint16_t* seg_10dd = (uint16_t*)0x10dd;
uint16_t* seg_62d = (uint16_t*)0x62d;
uint16_t* seg_6453 = (uint16_t*)0x6453;
uint16_t* seg_643b = (uint16_t*)0x643b;
uint16_t* seg_66ec = (uint16_t*)0x66ec;
uint16_t* seg_652e = (uint16_t*)0x652e;
uint16_t* seg_6557 = (uint16_t*)0x6557;

int FUN_1000_cfb7(uint8_t param_1) {
    char cVar1;
    uint16_t uVar2;
    int iVar3;
    char local_10d[255];
    int local_e;
    int local_c;
    char local_a;
    char local_9;
    char local_8;
    uint8_t local_7;
    uint32_t local_6;
    int local_4;

    local_4 = 0x1000;
    local_6 = 0xcfc2;
    FUN_24dd_0530();
    local_a = '\0';
    FUN_1ec2_10ea(0, 0x5826, 0);
    FUN_