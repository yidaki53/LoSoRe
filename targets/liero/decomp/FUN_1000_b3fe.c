
undefined2 FUN_1000_b3fe(void)

{
  undefined1 uVar1;
  int iVar2;
  char extraout_AL;
  undefined1 extraout_AH;
  undefined2 unaff_DS;
  undefined4 uStack_6;
  
  FUN_24dd_0530();
  uStack_6 = 0x10000109;
  while (*(undefined1 *)(uStack_6._1_2_ + 0x783b) = 0, uStack_6._1_2_ != 0xab) {
    uStack_6 = (ulong)CONCAT12(uStack_6._3_1_,uStack_6._1_2_ + 1) << 8;
  }
  do {
    FUN_24ba_00d8();
  } while (extraout_AL == '\0');
  uStack_6 = CONCAT13(uStack_6._3_1_,0x100);
  while( true ) {
    iVar2 = uStack_6._1_2_;
    if (*(char *)(uStack_6._1_2_ + 0x783b) != '\0') {
      uVar1 = uStack_6._1_1_;
      uStack_6 = CONCAT13(uVar1,(undefined3)uStack_6);
      *(undefined1 *)(iVar2 + 0x783b) = 0;
    }
    if (uStack_6._1_2_ == 0xab) break;
    uStack_6 = (ulong)CONCAT12(uStack_6._3_1_,uStack_6._1_2_ + 1) << 8;
  }
  return CONCAT11(extraout_AH,uStack_6._3_1_);
}

