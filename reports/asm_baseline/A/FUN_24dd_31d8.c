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
#define __cdecl
#define __stdcall
#define __fastcall
#define __pascal
#define __near
#define __far
#define __interrupt
#define __declspec(x)
#ifndef true
#define true 1
#define false 0
#endif

static void
set_mouse_pos(unsigned short x, unsigned short y)
{
	unsigned short regs[8];

	if (x == 0 && y == 0) {
		/* Disable mouse tracking. */
		regs[0] = 0x00;
		regs[1] = 0x00;
		__asm__ __volatile__ ("out %%dx, %%aw" : : "a" (regs[0]), "d" (0x33));
		return;
	}

	regs[0] = (y & 0x80) << 7;
	regs[1] = x;
	regs[2] = y & 0x7f;
	__asm__ __volatile__ ("out %%dx, %%aw" : : "a" (regs[0]), "d" (0x33));
	__asm__ __volatile__ ("out %%dx, %%aw" : : "a" (regs[1]), "d" (0x34));
	__asm__ __volatile__ ("out %%dx, %%aw" : : "a" (regs[2]), "d" (0x35));
}