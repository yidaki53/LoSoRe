
void __stdcall16far FUN_3de3_0000(char param_1)

{
  undefined1 extraout_AH;
  undefined1 extraout_AH_00;
  undefined1 uVar1;
  undefined2 unaff_DS;
  
  FUN_42b5_04df();
  uVar1 = extraout_AH;
  if (param_1 != '\a') {
    FUN_40a5_05e4(CONCAT11(extraout_AH,param_1));
    uVar1 = extraout_AH_00;
  }
  if (*(int *)0xaaec != 0) {
    FUN_405f_0121(CONCAT11(uVar1,param_1));
  }
  return;
}

