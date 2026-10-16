static void
draw_hline(u_char * p, int linesize, int x, int y, int w, int h, int color)
{
	u_char *dest = p + y * linesize + x;
	unsigned char *s = (unsigned char *)dest;
	unsigned char *ss;
	unsigned char c = color ? 0xff : 0x00;

	while (h--)
	{
		ss = &c;
		dest = s + 32;
		while (w--)
		{
			*s++ = *ss;
			*s++ = *ss;
			*s++ = *ss;
			s++;
		}
		dest += linesize - 32;
		s = (unsigned char *)dest;
	}
}