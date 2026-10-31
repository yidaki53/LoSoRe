
undefined1 __cdecl16far FUN_42b5_0896(undefined4 param_1)

{
  undefined1 uVar1;
  int in_BX;
  undefined1 in_CF;
  undefined1 in_ZF;
  
  FUN_42b5_0776();
  if ((bool)in_ZF) {
    uVar1 = FUN_42b5_079a();
    if (!(bool)in_CF) {
      in_BX = in_BX + 1;
    }
  }
  else {
    uVar1 = 0x1a;
  }
  *(int *)((int)param_1 + 8) = in_BX;
  return uVar1;
}

