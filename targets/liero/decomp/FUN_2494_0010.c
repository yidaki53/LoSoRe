
void __cdecl16far FUN_2494_0010(void)

{
  code *pcVar1;
  undefined2 in_BX;
  undefined2 unaff_ES;
  undefined2 unaff_DS;
  
  pcVar1 = (code *)swi(0x2f);
  (*pcVar1)();
  *(undefined2 *)0x7838 = in_BX;
  *(undefined2 *)0x783a = unaff_ES;
  return;
}

