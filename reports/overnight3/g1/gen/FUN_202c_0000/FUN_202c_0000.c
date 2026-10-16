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

typedef void (*code)(int);

uint16_t FUN_24dd_3d80(uint param1, int param2);
uint16_t FUN_24dd_32a9(void);
uint16_t FUN_24dd_3249(void);

uint16_t __stdcall16far
FUN_202c_0000(uint param_1, int param_2, uint param_3, int param_4, uint param_5, int param_6,
             uint param_7, int param_8)
{
  code *pcVar1;
  uint uVar2;
  uint uVar3;
  uint16_t uVar4;
  int iVar5;
  int iVar6;
  uint16_t extraout_DX;
  uint16_t uVar7;
  
  iVar5 = (param_6 - param_2) - (param_5 < param_1);
  uVar2 = FUN_24dd_3d80();
  iVar6 = (param_8 - param_4) - (param_7 < param_3);
  uVar3 = FUN_24dd_3d80(uVar2, iVar5);
  pcVar1 = (code *)0x37;
  (*pcVar1)(iVar6 + iVar5 + (uVar3 < uVar2));
  uVar7 = extraout_DX;
  FUN_24dd_32a9();
  uVar4 = FUN_24dd_3249();
  return ((uint16_t)uVar7 << 8) | uVar4;
}