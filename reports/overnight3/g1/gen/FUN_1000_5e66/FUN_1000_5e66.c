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

// Function prototypes (assuming these are defined elsewhere)
void FUN_24dd_3eaf(int, int, int, int, int);
void FUN_1ec2_0e8f(int, int, int, int, int, int, int, int);
void FUN_24dd_3e7c(void);
void FUN_1ec2_0dc8(int, int, int, int, int);
void FUN_1ec2_0e4a(int, int, int, int);
void FUN_1000_5c36(int);
void FUN_24dd_3dbd(void);
void FUN_1ec2_13c5(void);
void FUN_1ec2_13b0(int, int, int, int);
int FUN_1ec2_1619(uint8_t, uint8_t);
void FUN_1ec2_10ea(uint16_t, int, int);
void FUN_1ec2_11b5(uint8_t, int, int);
void FUN_1ec2_155e(int, int);

// Global variables (assuming these are defined elsewhere)
extern uint16_t global_6680;
extern uint16_t global_6684;
extern uint16_t global_6690;
extern uint16_t global_6674;
extern uint16_t global_6670;
extern uint16_t global_66a3;
extern uint16_t global_66a5;
extern uint16_t global_66a6;
extern uint16_t global_66af;
extern uint16_t global_672c;
extern uint16_t global_67b0;
extern uint16_t global_67b2;
extern uint16_t global_67b4;
extern uint16_t global_67b6;
extern uint16_t global_67c0;
extern uint16_t global_6520;
extern uint16_t global_6524;
extern uint16_t global_6427;
extern uint16_t global_6429;
extern uint16_t global_642b;
extern uint16_t global_642d;
extern uint16_t global_6432;
extern uint16_t global_6434;
extern uint16_t global_6436;
extern uint16_t global_6438;
extern uint16_t global_643a;

void function_name(void) {
    int local_4;
    int local_6;
    int local_8;
    int local_a;
    int local_c;
    int local_122;
    int local_12c;
    int local_12e;
    int local_130;
    int local_132;
    int local_134;
    int local_136;
    int local_13c;
    int local_126;
    int local_128;
    int local_12a;
    int local_12b;
    int local_12d;
    int local_12f;
    int local_131;
    int local_133;
    int local_135;
    int local_137;
    int local_138;
    int local_139;
    int local_13a;
    int local_13b;
    int local_13c;
    int local_13d;
    int local_13e;
    int local_13f;
    int local_140;
    int local_141;
    int local_142;
    int local_143;
    int local_144;
    int local_145;
    int local_146;
    int local_147;
    int local_148;
    int local_149;
    int local_14a;
    int local_14b;
    int local_14c;
    int local_14d;
    int local_14e;
    int local_14f;
    int local_150;