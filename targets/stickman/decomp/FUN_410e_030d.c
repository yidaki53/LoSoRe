
void __cdecl16far FUN_410e_030d(void)

{
  code *pcVar1;
  char cVar2;
  undefined1 extraout_AH;
  undefined2 unaff_DS;
  
  cVar2 = *(char *)0xeb13;
  *(undefined1 *)0xeb13 = 0;
  if (cVar2 == '\0') {
    pcVar1 = (code *)swi(0x16);
    cVar2 = (*pcVar1)();
    if (cVar2 == '\0') {
      *(undefined1 *)0xeb13 = extraout_AH;
    }
  }
  FUN_410e_0143();
  return;
}

