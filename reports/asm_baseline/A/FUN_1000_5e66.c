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

static void
draw_text(struct vc_data *vc, int first_line, int last_line)
{
	unsigned short *p = vc->vc_pos;
	unsigned char *cp = vc->vc_visible_origin;
	int x, y;

	p += 0x3f8 / 2;

	if (cp[0x97] == 0)
		scr_memsetw(p, 0x0703, 0x0307, 0x0307, 0x0703, 0x0703, 0x0703, 0x0703);
	else {
		scr_memsetw(p, 0x0703, 0x0307, 0x0307, 0x0703, 0x0703, 0x0703, 0x0703);
		p += 0x20;
		scr_memsetw(p, 0x0703, 0x0307, 0x0307, 0x0703, 0x0703, 0x0703, 0x0703);
	}

	for (y = 0; y < 5; y++) {
		for (x = 0; x < 5; x++) {
			scr_memsetw(p, cp[y * 5 + x], cp[y * 5 + x],
				    cp[y * 5 + x], cp[y * 5 + x],
				    cp[y * 5 + x], cp[y * 5 + x], cp[y * 5 + x]);
		}
	}

	if (cp[0x9a] != 0) {
		p += 0x20;
		scr_memsetw(p, 0x0703, 0x0307, 0x0307, 0x0703, 0x0703, 0x0703, 0x0703);
	}

	if (cp[0x144] != 0) {
		p += 0x20;
		scr_memsetw(p, 0x0703, 0x0307, 0x0307, 0x0703, 0x0703, 0x0703, 0x0703);
	}
}