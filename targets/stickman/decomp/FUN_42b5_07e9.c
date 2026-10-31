
undefined4 __cdecl16near FUN_42b5_07e9(void)

{
  int iVar1;
  undefined2 in_BX;
  int unaff_DI;
  undefined2 unaff_ES;
  
  *(undefined2 *)(unaff_DI + 8) = in_BX;
  iVar1 = (*(code *)*(undefined2 *)(unaff_DI + 0x14))(0x42b5);
  if (iVar1 != 0) {
    DAT_4473_039c = iVar1;
  }
  return CONCAT22(*(undefined2 *)(unaff_DI + 4),*(undefined2 *)(unaff_DI + 10));
}

