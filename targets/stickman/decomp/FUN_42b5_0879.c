
void __cdecl16near FUN_42b5_0879(void)

{
  int iVar1;
  int unaff_DI;
  undefined2 unaff_ES;
  undefined2 unaff_DS;
  
  if (*(int *)(unaff_DI + 0x1a) == 0) {
    return;
  }
  if (*(int *)0x39c == 0) {
    iVar1 = (*(code *)*(undefined2 *)(unaff_DI + 0x18))(0x42b5);
    if (iVar1 != 0) {
      *(int *)0x39c = iVar1;
    }
  }
  return;
}

