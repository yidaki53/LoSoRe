
undefined2 __cdecl16near FUN_1000_4f50(void)

{
  char cVar1;
  int iVar2;
  undefined2 uVar3;
  undefined1 extraout_AH;
  undefined1 extraout_AH_00;
  undefined1 uVar4;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  undefined1 local_84 [126];
  undefined2 uStack_6;
  char local_4;
  char local_3;
  
  local_4 = 0;
  local_3 = 0x10;
  uStack_6 = 0x4f5b;
  FUN_42b5_04df();
  FUN_42b5_17e2(0x4f43,0x42b5,local_84,unaff_SS);
  FUN_42b5_1810(0x8a,local_84,unaff_SS);
  iVar2 = FUN_42b5_04a2();
  if (iVar2 == 0) {
    local_4 = '\0';
    while (local_4 == '\0') {
      FUN_42b5_19c5(local_84,unaff_SS);
      cVar1 = FUN_42b5_04a9();
      if (cVar1 != '\0') break;
      FUN_42b5_18c5(0x4b8,unaff_DS);
      cVar1 = &stack0x0000 == (undefined1 *)0x84;
      FUN_42b5_04a9();
      FUN_42b5_0cc9(0xa7d6,unaff_DS,0x4b8,unaff_DS);
      local_4 = cVar1;
    }
    FUN_42b5_1891(local_84,unaff_SS);
    FUN_42b5_04a9();
    local_3 = local_4;
    uVar4 = extraout_AH_00;
    if (*(char *)0x541 != '\x01') {
      *(undefined1 *)0x541 = 0;
    }
  }
  else {
    uVar3 = FUN_4170_0123(0x4f43,0x42b5);
    FUN_4170_049d(uVar3);
    local_3 = '\0';
    uVar4 = extraout_AH;
  }
  return CONCAT11(uVar4,local_3);
}

