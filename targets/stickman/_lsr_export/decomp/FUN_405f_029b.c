
void __cdecl16far FUN_405f_029b(void)

{
  char cVar1;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  undefined1 local_16;
  undefined1 local_15;
  int local_10;
  undefined2 uStack_6;
  undefined2 uStack_4;
  
  uStack_4 = 0x405f;
  uStack_6 = 0x896;
  FUN_42b5_04df();
  while( true ) {
    cVar1 = FUN_410e_02fb();
    if (cVar1 == '\0') break;
    FUN_410e_030d();
  }
  if (*(int *)0xaaec != 0) {
    FUN_42b5_1a42(0,0x14,&local_16,unaff_SS);
    local_15 = 10;
    local_10 = *(int *)0xaaec + -1;
    FUN_428f_000b(&local_16);
  }
  return;
}

