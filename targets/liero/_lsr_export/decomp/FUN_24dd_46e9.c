
void __cdecl16far FUN_24dd_46e9(void)

{
  code *pcVar1;
  undefined2 in_CX;
  undefined2 extraout_DX;
  undefined2 unaff_DS;
  
  pcVar1 = (code *)swi(0x21);
  (*pcVar1)();
  *(undefined2 *)0x6412 = in_CX;
  *(undefined2 *)0x6414 = extraout_DX;
  return;
}

