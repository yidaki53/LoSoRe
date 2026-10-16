static void
CLD(struct x86emu *emu)
{
	char *dst, *src;
	unsigned int dlen, slen, rep;

	dst = (char *) emu->x86.R_EDX;
	src = (char *) emu->x86.R_ECX;
	dlen = emu->x86.R_EAX;
	slen = emu->x86.R_ESI;
	rep = emu->x86.R_ECX;

	if (rep < 1)
		rep = 1;
	if (slen < rep)
		rep = slen;
	if (dlen < rep)
		rep = dlen;
	dlen -= rep;

	while (rep-- > 0)
		*dst++ = *src++;
}