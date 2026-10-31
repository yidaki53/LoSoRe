
void __cdecl16near FUN_1000_235e(void)

{
  char cVar1;
  undefined2 unaff_DS;
  
  FUN_42b5_04df();
  if ((((1 < *(int *)0x3b0) && (*(int *)0x3ac == 0)) && (*(char *)0x3a6 == '\0')) &&
     (((cVar1 = FUN_1000_11b0(), cVar1 != '\0' &&
       (cVar1 = FUN_1000_10fa(*(int *)0x3b0 + -1,*(int *)0x3ae + -1), cVar1 == '\0')) &&
      (cVar1 = FUN_1000_10fa(*(int *)0x3b0 + -1,*(int *)0x3ae + -2), cVar1 == '\0')))) {
    FUN_3de3_0b67(*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
    FUN_3de3_002d(0x2342,0x3de3);
    *(int *)0x3ae = *(int *)0x3ae + -1;
    *(int *)0x3b0 = *(int *)0x3b0 + -1;
    FUN_3de3_0bea(0x2351,0x3de3,*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
    FUN_1000_1619(5);
    *(undefined2 *)0x3ac = 0xffff;
  }
  return;
}

