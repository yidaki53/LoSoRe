static void
set_string(char *dest, char *src)
{
	char *d = dest;
	char *s = src;

	while (d < s + sizeof(dest))
		*d++ = *s++;
}