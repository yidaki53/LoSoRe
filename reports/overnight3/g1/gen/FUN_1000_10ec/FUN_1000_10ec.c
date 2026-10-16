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
int FUN_24dd_4654(uint16_t param_1);
int FUN_24dd_3dbd(void);
void out(uint16_t param_1, uint16_t param_2);
void halt_baddata(void);

// Global variables
extern uint16_t global_6670;
extern uint16_t global_6720;
extern uint16_t global_6721;
extern uint16_t global_6722;
extern uint16_t global_6723;
extern uint16_t global_6724;
extern uint16_t global_6725;

void function(uint16_t param_1, uint16_t param_2, uint16_t param_3, uint16_t param_4, uint16_t param_5, uint16_t param_6, uint16_t param_7, uint16_t param_8, uint16_t param_9, uint16_t param_10, uint16_t param_11, uint16_t param_12, uint16_t param_13, uint16_t param_14, uint16_t param_15, uint16_t param_16, uint16_t param_17, uint16_t param_18, uint16_t param_19, uint16_t param_20, uint16_t param_21, uint16_t param_22, uint16_t param_23, uint16_t param_24, uint16_t param_25, uint16_t param_26, uint16_t param_27, uint16_t param_28, uint16_t param_29, uint16_t param_30, uint16_t param_31, uint16_t param_32, uint16_t param_33, uint16_t param_34, uint16_t param_35, uint16_t param_36, uint16_t param_37, uint16_t param_38, uint16_t param_39, uint16_t param_40, uint16_t param_41, uint16_t param_42, uint16_t param_43, uint16_t param_44, uint16_t param_45, uint16_t param_46, uint16_t param_47, uint16_t param_48, uint16_t param_49, uint16_t param_50, uint16_t param_51, uint16_t param_52, uint16_t param_53, uint16_t param_54, uint16_t param_55, uint16_t param_56, uint16_t param_57, uint16_t param_58, uint16_t param_59, uint16_t param_60, uint16_t param_61, uint16_t param_62, uint16_t param_63, uint16_t param_64, uint16_t param_65, uint16_t param_66, uint16_t param_67, uint16_t param_68, uint16_t param_69, uint16_t param_70, uint16_t param_71, uint16_t param_72, uint16_t param_73, uint16_t param_74, uint16_t param_75, uint16_t param_76, uint16_t param_77, uint16_t param_78, uint16_t param_79, uint16_t param_80, uint16_t param_81, uint16_t param_82, uint16_t param_83, uint16_t param_84, uint16_t param_85, uint16_t param_86, uint16_t param_87, uint16_t param_88, uint16_t param_