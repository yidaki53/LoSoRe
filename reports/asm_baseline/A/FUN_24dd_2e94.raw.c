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