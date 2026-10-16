static void
draw_digit(struct vc_data *vc, unsigned int color, unsigned int bgcolor,
	    unsigned int digit)
{
	unsigned int i, j;

	for (i = 0; i < 6; i++) {
		digit = get_digit_line(vc, color, bgcolor, digit, 0x3c);
		for (j = 0; j < 16; j++)
			scr_memw((i << 4) + j, digit);
	}
}