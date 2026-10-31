
undefined2 __cdecl16far FUN_405f_01dd(void)

{
  char cVar1;
  undefined1 extraout_AL;
  undefined1 extraout_AH;
  undefined1 extraout_AH_00;
  undefined1 uVar2;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  undefined1 local_18;
  undefined1 local_17;
  int local_12;
  undefined2 uStack_6;
  undefined2 uStack_4;
  
  uStack_4 = 0x405f;
  uStack_6 = 0x7d8;
  FUN_42b5_04df();
  cVar1 = FUN_410e_02fb();
  if (cVar1 == '\0') {
    FUN_42b5_1a42(0,0x14,&local_18,unaff_SS);
    local_17 = 2;
    local_12 = *(int *)0xaaec + -1;
    FUN_428f_000b(&local_18);
    uStack_4._1_1_ = local_18;
    uVar2 = extraout_AH_00;
  }
  else {
    FUN_410e_030d();
    uVar2 = extraout_AH;
    uStack_4._1_1_ = extraout_AL;
  }
  return CONCAT11(uVar2,uStack_4._1_1_);
}

