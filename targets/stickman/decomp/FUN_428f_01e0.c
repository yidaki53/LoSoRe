
void __cdecl16near FUN_428f_01e0(void)

{
  undefined1 *puVar1;
  uint in_AX;
  uint in_BX;
  undefined1 *unaff_SI;
  undefined1 *unaff_DI;
  undefined2 unaff_ES;
  undefined2 unaff_DS;
  
  if (in_BX <= in_AX) {
    in_AX = in_BX;
  }
  *unaff_DI = (char)in_AX;
  for (; unaff_DI = unaff_DI + 1, in_AX != 0; in_AX = in_AX - 1) {
    puVar1 = unaff_SI;
    unaff_SI = unaff_SI + 1;
    *unaff_DI = *puVar1;
  }
  return;
}

