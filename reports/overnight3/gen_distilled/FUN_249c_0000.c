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

void __stdcall16far FUN_249c_0000(byte param_1, byte param_2) {
    // Simulate the interrupt call
    // Assuming 0x10 is the interrupt number for the interrupt service routine
    // This is a placeholder for the actual interrupt call implementation
    // In a real scenario, you would use an external library or system call to make the interrupt
    // For the purpose of this example, we'll just simulate the call
    // Note: This is not a complete implementation and would need to be expanded with actual interrupt handling
    // Here, we're just printing the parameters to simulate the interrupt call
    printf("Simulating interrupt call with params: %d, %d\n", (int)param_1, (int)param_2);
}