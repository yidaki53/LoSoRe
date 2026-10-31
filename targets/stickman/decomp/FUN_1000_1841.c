
void __cdecl16near FUN_1000_1841(void)

{
  int iVar1;
  undefined2 unaff_DS;
  
  FUN_42b5_04df();
  iVar1 = *(int *)0x3b4;
  if ((*(int *)0x3b0 < 0x12) &&
     (((*(char *)((*(int *)0x3b0 + 3) * 0x50 + *(int *)0x3ae + 0x1f6e) == '\n' ||
       (*(char *)((*(int *)0x3b0 + 3) * 0x50 + *(int *)0x3ae + 0x1f6f) == '\n')) ||
      (*(char *)((*(int *)0x3b0 + 3) * 0x50 + *(int *)0x3ae + 0x1f70) == '\n')))) {
    FUN_1000_1735(1);
  }
  if (*(int *)0x3b4 != iVar1) {
    FUN_1000_06a1();
  }
  return;
}

