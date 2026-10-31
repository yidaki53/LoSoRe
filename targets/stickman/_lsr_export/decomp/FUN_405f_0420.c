
undefined2 __cdecl16far FUN_405f_0420(void)

{
  undefined1 extraout_AL;
  undefined1 extraout_AH;
  undefined1 extraout_AH_00;
  undefined1 uVar1;
  undefined2 unaff_DS;
  undefined1 local_18;
  undefined1 local_17;
  undefined2 uStack_6;
  undefined2 uStack_4;
  
  uStack_4 = 0x405f;
  uStack_6 = 0xa1b;
  FUN_42b5_04df();
  if (*(int *)0xaaec == 0) {
    local_17 = 8;
    FUN_428f_0000(0x42b5,&local_18);
    uStack_4._1_1_ = local_18;
    uVar1 = extraout_AH;
  }
  else {
    FUN_405f_01dd();
    uVar1 = extraout_AH_00;
    uStack_4._1_1_ = extraout_AL;
  }
  return CONCAT11(uVar1,uStack_4._1_1_);
}

