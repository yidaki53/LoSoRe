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

static int
check_key(struct w6692_hw *card)
{
	unsigned char resp[10];

	resp[0] = 0xff;
	resp[1] = 0xff;
	resp[2] = 0xff;
	resp[3] = 0xff;
	resp[4] = 0xff;
	resp[5] = 0xff;
	resp[6] = 0xff;
	resp[7] = 0xff;
	resp[8] = 0xff;
	resp[9] = 0xff;

	W6692_fill_hdr(&card->MsgHdr, 0x182, 0x00);
	w6692_send_msg(card);

	W6692_fill_hdr(&card->MsgHdr, 0x182, 0x00);
	resp[0] = W6692_send_recv_msg(card, 0x41, 0x01, 0xff, resp);
	resp[1] = W6692_send_recv_msg(card, 0x49, 0x00, 0xff, resp);
	resp[2] = W6692_send_recv_msg(card, 0x44, 0x00, 0xff, resp);
	resp[3] = W6692_send_recv_msg(card, 0x48, 0x00, 0xff, resp);

	if (resp[0] == 0x00 || resp[1] == 0xff || resp[2] == 0xff ||
	    resp[3] == 0xff)
		return 0;

	return 1;
}