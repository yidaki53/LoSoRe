
int FUN_405f_0067(undefined1 param_1)

{
  byte extraout_AH;
  int iVar1;
  undefined2 unaff_DS;
  
  FUN_42b5_04df();
  FUN_405f_0000();
  *(undefined1 *)0xaaef = 0xb;
  *(int *)0xaaf4 = *(int *)0xaaec + -1;
  *(undefined1 *)0xaaee = param_1;
  FUN_428f_000b(0xaaee);
  iVar1 = (uint)extraout_AH * 0x100;
  if (*(int *)0xaaee != 0) {
    iVar1 = iVar1 + 1;
  }
  return iVar1;
}

