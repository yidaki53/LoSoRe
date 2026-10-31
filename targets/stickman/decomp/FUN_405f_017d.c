
void __cdecl16far FUN_405f_017d(void)

{
  code *pcVar1;
  char cVar2;
  undefined2 unaff_DS;
  
  FUN_42b5_04df();
  if (*(int *)0xaaec != 0) {
    do {
      pcVar1 = (code *)swi(0x14);
      (*pcVar1)();
      while ((*(int *)0x156 != *(int *)0x158 &&
             (cVar2 = FUN_405f_0067(CONCAT11((char)((uint)*(int *)0x156 >> 8),
                                             *(undefined1 *)(*(int *)0x158 + -0x54fe))),
             cVar2 != '\0'))) {
        *(int *)0x158 = *(int *)0x158 + 1;
        if (0x3fff < *(int *)0x158) {
          *(int *)0x158 = *(int *)0x158 + -0x4000;
        }
      }
    } while (*(int *)0x156 != *(int *)0x158);
    pcVar1 = (code *)swi(0x14);
    (*pcVar1)();
  }
  return;
}

