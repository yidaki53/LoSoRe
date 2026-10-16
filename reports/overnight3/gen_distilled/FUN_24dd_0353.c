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

void FUN_24dd_0353(void) {
    uint16_t *ptr = (uint16_t *)(0x7b3c);
    *ptr = 0;

    FUN_24dd_03de();

    uint16_t uVar1;
    uint16_t *base = (uint16_t *)(0x63f6);
    uint16_t *limit = (uint16_t *)((uint16_t)base + 0x63f0);
    uint16_t *data = (uint16_t *)((uint16_t)base + 0x63f2);
    uint16_t *extra = (uint16_t *)((uint16_t)base + 0x63f4);
    uint16_t *unaff_DS = (uint16_t *)(0x63ee);
    uint16_t *unaff_ES = (uint16_t *)(0x63f0);
    uint16_t *unaff_ESI = (uint16_t *)(0x63f3);
    uint16_t *unaff_ECX = (uint16_t *)(0x63f5);
    uint16_t *unaff_EBX = (uint16_t *)(0x63f7);
    uint16_t *unaff_EAX = (uint16_t *)(0x63f9);
    uint16_t *unaff_EDX = (uint16_t *)(0x63fb);
    uint16_t *unaff_EIP = (uint16_t *)(0x63fc);
    uint16_t *unaff_EFLAGS = (uint16_t *)(0x63fe);

    if (*unaff_EIP != 0) {
        uVar1 = (uint16_t)((uint16_t)unaff_EIP >> 16);
        if ((unaff_EAX < *limit) && (unaff_EAX >= *base)) {
            if ((unaff_EDX < *extra) && (unaff_EDX >= *unaff_ES)) {
                if ((unaff_ECX < *data) && (unaff_ECX >= *unaff_ESI)) {
                    if ((unaff_EAX < *unaff_DS) && (unaff_EAX >= *unaff_ESI)) {
                        if ((unaff_EDX < *unaff_ECX) && (unaff_EDX >= *unaff_EBX)) {
                            if ((unaff_EAX < *unaff_ECX) && (unaff_EAX >= *unaff_EBX)) {
                                if ((unaff_EDX < *unaff_ECX) && (unaff_EDX >= *unaff_EBX)) {
                                    if ((unaff_EAX < *unaff_ECX) && (unaff_EAX >= *unaff_EBX)) {
                                        if ((unaff_EDX < *unaff_ECX) && (unaff_EDX >= *unaff_EBX)) {
                                            if ((unaff_EAX < *unaff_ECX) && (unaff_EAX >= *unaff_EBX)) {
                                                if ((unaff_EDX < *unaff_ECX) && (unaff_EDX >= *unaff_EBX)) {
                                                    if ((unaff_EAX < *unaff_ECX) && (unaff_EAX >= *unaff_EBX)) {
                                                        if ((unaff_EDX < *unaff_ECX) && (unaff_EDX >= *unaff_EBX)) {
                                                            if ((unaff_EAX < *unaff_ECX) && (unaff_EAX >= *unaff_EBX)) {
                                                                if ((unaff_EDX < *unaff_ECX) && (unaff_EDX >= *unaff_EBX)) {
                                                                    if ((unaff_EAX < *unaff_ECX) && (unaff_EAX >= *unaff_EBX)) {
                                                                        if ((unaff_EDX < *unaff_ECX) && (unaff_EDX >= *unaff_EBX)) {
                                                                            if ((unaff_EAX < *unaff_ECX) && (unaff_EAX >= *unaff_EBX)) {
                                                                                if ((unaff_EDX < *unaff_ECX) && (unaff_EDX >= *unaff_EBX)) {
                                                                                    if ((unaff_EAX < *unaff_ECX) && (unaff_EAX >= *unaff_EBX)) {
                                                                                        if ((unaff_EDX < *unaff_ECX) && (unaff_EDX >= *unaff_EBX)) {
                                                                                            if ((unaff_EAX < *unaff_ECX) && (unaff_EAX >= *unaff_EBX)) {