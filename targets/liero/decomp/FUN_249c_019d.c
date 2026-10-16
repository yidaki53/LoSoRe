
char __cdecl16far FUN_249c_019d(void)

{
  code *pcVar1;
  char cVar2;
  undefined2 unaff_DS;
  
  pcVar1 = (code *)swi(0x21);
  cVar2 = (*pcVar1)();
  if ((*(char *)0x159c != '\0') && (cVar2 == '\x03')) {
    pcVar1 = (code *)swi(0x23);
    (*pcVar1)();
  }
  return cVar2;
}

