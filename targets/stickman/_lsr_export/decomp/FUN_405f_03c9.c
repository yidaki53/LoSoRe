
void __cdecl16far FUN_405f_03c9(void)

{
  code *pcVar1;
  undefined2 unaff_DS;
  
  FUN_42b5_04df();
  if (*(int *)0xaaec != 0) {
    pcVar1 = (code *)swi(0x14);
    (*pcVar1)();
    pcVar1 = (code *)swi(0x14);
    (*pcVar1)();
  }
  return;
}

