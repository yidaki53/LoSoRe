
void __stdcall16far FUN_4170_04c5(undefined1 *param_1,undefined2 param_2)

{
  char cVar1;
  undefined1 extraout_AH;
  undefined2 uVar2;
  undefined2 unaff_SS;
  undefined1 *puVar3;
  undefined2 uVar4;
  undefined1 *puVar5;
  undefined2 uVar6;
  undefined1 local_206 [256];
  undefined1 local_106 [256];
  int local_6;
  byte local_4;
  char local_3;
  
  local_4 = 0x70;
  local_3 = 0x41;
  local_6 = 0x1bd0;
  FUN_42b5_04df();
  *param_1 = 0;
  local_3 = '\0';
  while ((cVar1 = FUN_4170_03dd(param_2), cVar1 == '\0' && (local_3 == '\0'))) {
    local_6 = FUN_4170_024c(1,&local_4,unaff_SS,param_2);
    if ((local_4 == 10) || (local_4 == 0xd)) {
      local_3 = '\x01';
    }
    else {
      local_3 = '\0';
    }
    if ((local_3 == '\0') && (local_6 == 1)) {
      puVar5 = local_206;
      uVar2 = (undefined2)((ulong)param_1 >> 0x10);
      uVar6 = unaff_SS;
      FUN_42b5_0bc4((undefined1 *)param_1,uVar2);
      puVar3 = local_106;
      uVar4 = unaff_SS;
      FUN_42b5_0cf4(CONCAT11(extraout_AH,local_4));
      FUN_42b5_0c51(puVar3,uVar4);
      FUN_42b5_0bde(0xff,(undefined1 *)param_1,uVar2,puVar5,uVar6);
    }
  }
  FUN_4170_024c(1,&local_4,unaff_SS,param_2);
  return;
}

