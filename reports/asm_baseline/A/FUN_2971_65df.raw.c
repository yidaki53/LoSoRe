static void
set_default_options(void)
{
#ifdef WITH_SSL
	SetOpensslPasswordCallback(ForwardPassword);
#endif
}