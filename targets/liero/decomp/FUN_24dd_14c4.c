
void __cdecl16near FUN_24dd_14c4(void)

{
  undefined2 uVar1;
  int unaff_SI;
  undefined2 unaff_DS;
  
  if (-0x3fff < *(int *)(unaff_SI + 8)) {
    if (*(int *)(unaff_SI + 8) < 0x4001) {
      if (*(char *)(unaff_SI + 10) == '\0') {
        FUN_24dd_0628();
        FUN_24dd_1519();
        uVar1 = *(undefined2 *)0xd8;
        FUN_24dd_1277(unaff_SI,uVar1,unaff_SI);
        FUN_24dd_0ee2(unaff_SI,unaff_SI,uVar1);
        *(int *)(unaff_SI + 8) = *(int *)(unaff_SI + 8) + -1;
        *(int *)0xd8 = *(int *)0xd8 + 0xc;
      }
      else {
        FUN_24dd_2361();
        FUN_24dd_05e8();
        *(undefined2 *)(unaff_SI + 8) = 0x4001;
      }
    }
    else {
      FUN_24dd_0e57();
    }
  }
  return;
}

