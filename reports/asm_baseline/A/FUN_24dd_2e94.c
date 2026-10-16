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
s1450_build_eprom_checksum(const struct s1450_eprom *eprom,
			   struct s1450_eprom_checksum *checksum)
{
	u16 *eeprom_copy;
	u16 crc;
	unsigned char ch;

	if (eprom->header[15] & 2) {
		/*
		 * Checksummed image.
		 */
		eeprom_copy = (u16 *)eprom->data;
		crc = eeprom_copy[254];
		crc -= 0x34;
		if (crc > 0x08)
			crc -= 2;
		else if (crc < 0x09)
			crc = 0x9b90;
		else
			crc = 0x9b;
		eeprom_copy[254] = crc;
		checksum->data = eeprom_copy;
	} else {
		/*
		 * Unchecksummed image.
		 */
		eeprom_copy = (u16 *)eprom->data;
		crc = 0;
		for (ch = 0; ch < 254; ch++)
			crc = crc + eeprom_copy[ch];
		eeprom_copy[254] = (((crc & 0xff00) >> 8) ^ 0x88) + 0xd826;
		checksum->data = eeprom_copy;
	}
}