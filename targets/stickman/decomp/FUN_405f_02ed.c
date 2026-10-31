
undefined2 __stdcall16far FUN_405f_02ed(int param_1)

{
  undefined1 extraout_AH;
  undefined1 extraout_AH_00;
  undefined1 extraout_AH_01;
  undefined1 uVar1;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  undefined2 local_1c;
  int local_16;
  undefined2 uStack_6;
  undefined1 uStack_4;
  undefined1 local_3;
  
  uStack_4 = 0x5f;
  local_3 = 0x40;
  uStack_6 = 0x8e8;
  FUN_42b5_04df();
  local_3 = 1;
  uVar1 = extraout_AH;
  if (*(int *)0xaaec != 0) {
    local_3 = 0;
    FUN_42b5_1a42(0,0x14,&local_1c,unaff_SS);
    local_1c = CONCAT11(4,(undefined1)local_1c);
    local_16 = *(int *)0xaaec + -1;
    FUN_428f_000b(&local_1c);
    uVar1 = extraout_AH_00;
    if (local_1c == 0x1954) {
      local_16 = *(int *)0xaaec + -1;
      if (param_1 == 300) {
        local_1c = 0x43;
      }
      else if (param_1 == 600) {
        local_1c = 99;
      }
      else if (param_1 == 0x4b0) {
        local_1c = 0x83;
      }
      else if (param_1 == 0x960) {
        local_1c = 0xa3;
      }
      else if (param_1 == 0x12c0) {
        local_1c = 0xc3;
      }
      else if (param_1 == 0x2580) {
        local_1c = 0xe3;
      }
      else if ((param_1 == 0x3840) || (param_1 == 0x4b00)) {
        local_1c = 3;
      }
      else if (param_1 == -0x6a00) {
        local_1c = 0x23;
      }
      else {
        local_1c = 0x23;
      }
      FUN_428f_000b(&local_1c);
      local_3 = 1;
      uVar1 = extraout_AH_01;
    }
  }
  return CONCAT11(uVar1,local_3);
}

