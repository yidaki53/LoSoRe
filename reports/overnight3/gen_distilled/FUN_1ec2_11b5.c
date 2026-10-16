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

void FUN_1ec2_11b5(int param_1, uint8_t *param_2) {
    uint8_t local_302[768];
    uint8_t *pbVar1;
    uint8_t *pbVar3;
    uint32_t uVar4;
    uint32_t uVar6;
    uint32_t uVar8;
    uint32_t uVar10;
    uint32_t uVar12;
    uint32_t uVar14;
    uint32_t uVar16;
    uint32_t uVar18;
    uint32_t uVar20;
    uint32_t uVar22;
    uint32_t uVar24;
    uint32_t uVar26;
    uint32_t uVar28;
    uint32_t uVar30;
    uint32_t uVar32;
    uint32_t uVar34;
    uint32_t uVar36;
    uint32_t uVar38;
    uint32_t uVar40;
    uint32_t uVar42;
    uint32_t uVar43;
    uint32_t uVar45;
    uint32_t uVar46;
    uint32_t uVar47;
    uint32_t uVar48;
    uint32_t uVar49;
    uint32_t uVar50;
    uint32_t uVar52;
    uint32_t uVar54;
    uint32_t uVar56;
    uint32_t uVar58;
    uint32_t uVar60;
    uint32_t uVar62;
    uint32_t uVar63;
    uint32_t uVar64;
    uint32_t uVar65;
    uint32_t uVar66;
    uint32_t uVar67;
    uint32_t uVar68;
    uint32_t uVar69;
    uint32_t uVar70;
    uint32_t uVar71;
    uint32_t uVar72;
    uint32_t uVar73;
    uint32_t uVar74;
    uint32_t uVar75;
    uint32_t uVar76;
    uint32_t uVar77;
    uint32_t uVar78;
    uint32_t uVar79;
    uint32_t uVar80;
    uint32_t uVar81;
    uint32_t uVar82;
    uint32_t uVar83;
    uint32_t uVar84;
    uint32_t uVar85;
    uint32_t uVar86;
    uint32_t uVar87;
    uint32_t uVar88;
    uint32_t uVar89;
    uint32_t uVar90;
    uint32_t uVar92;
    uint32_t uVar94;
    uint32_t uVar96;
    uint32_t uVar98;
    uint32_t uVar100;
    uint32_t uVar102;
    uint32_t uVar104;
    uint32_t uVar106;
    uint32_t uVar108;
    uint32_t uVar110;
    uint32_t uVar112;
    uint32_t uVar114;
    uint32_t uVar116;
    uint32_t uVar118;
    uint32_t uVar120;
    uint32_t uVar122;
    uint32_t uVar124;
    uint32_t uVar126;
    uint32_t uVar128;
    uint32_t uVar130;
    uint32_t uVar132;
    uint32_t uVar134;
    uint32_t uVar136;
    uint32_t uVar138;
    uint32_t uVar140;
    uint32_t uVar142;
    uint32_t uVar144;
    uint32_t uVar146;
    uint32_t uVar148;
    uint32_t uVar150;
    uint32_t uVar152;
    uint32_t uVar154;
    uint32_t uVar