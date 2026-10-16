
void __stdcall16far FUN_249c_0037(byte *param_1,byte param_2,byte param_3)

{
  byte *pbVar1;
  byte bVar2;
  undefined1 uVar3;
  uint uVar4;
  byte *pbVar5;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  byte *local_10a;
  byte local_108;
  byte local_105;
  char local_103;
  byte local_102 [256];
  
  pbVar5 = (byte *)param_1;
  local_102[0] = *param_1;
  pbVar1 = local_102;
  for (uVar4 = (uint)local_102[0]; pbVar1 = pbVar1 + 1, pbVar5 = pbVar5 + 1, uVar4 != 0;
      uVar4 = uVar4 - 1) {
    *pbVar1 = *pbVar5;
  }
  FUN_249c_0013(&stack0xfffe);
  local_10a = (byte *)(((uint)param_2 * 0x50 + (uint)param_3) * 2);
  uVar3 = (undefined1)((uint)local_10a >> 8);
  FUN_249c_0000(CONCAT11(uVar3,param_2),CONCAT11(uVar3,param_3));
  bVar2 = local_102[0];
  local_103 = '\0';
  if (local_102[0] != 0) {
    local_108 = 1;
    while( true ) {
      if (local_103 == '\0') {
        if (local_102[local_108] == 0) {
          local_103 = '\x01';
        }
        else {
          *local_10a = local_102[local_108];
          local_10a[1] = local_105;
          local_10a = local_10a + 2;
        }
      }
      else if (local_103 == '\x01') {
        local_103 = '\x02';
        FUN_249c_0013(&stack0xfffe);
      }
      else if (local_103 == '\x02') {
        local_103 = '\0';
        FUN_249c_0013(&stack0xfffe);
      }
      if (local_108 == bVar2) break;
      local_108 = local_108 + 1;
    }
  }
  FUN_249c_0000(CONCAT11((char)((uint)param_3 + (uint)local_102[0] >> 8),param_2),
                (uint)param_3 + (uint)local_102[0]);
  FUN_24dd_3930(0x79f0,unaff_DS);
  FUN_24dd_04f4();
  return;
}

