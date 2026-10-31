
void __cdecl16far FUN_42b5_1300(void)

{
  code *pcVar1;
  undefined2 in_CX;
  undefined2 extraout_DX;
  undefined2 unaff_DS;
  
  pcVar1 = (code *)swi(0x21);
  (*pcVar1)();
  *(undefined2 *)0x39e = in_CX;
  *(undefined2 *)0x3a0 = extraout_DX;
  return;
}

