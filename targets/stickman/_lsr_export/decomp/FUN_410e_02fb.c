
undefined1 __cdecl16far FUN_410e_02fb(void)

{
  code *pcVar1;
  undefined2 unaff_DS;
  bool bVar2;
  
  bVar2 = *(char *)0xeb13 == '\0';
  if (bVar2) {
    pcVar1 = (code *)swi(0x16);
    (*pcVar1)();
    if (bVar2) {
      return 0;
    }
  }
  return 1;
}

