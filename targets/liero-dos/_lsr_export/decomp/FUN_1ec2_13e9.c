
void __stdcall16far
FUN_1ec2_13e9(undefined4 param_1,undefined4 param_2,byte param_3,byte *param_4,int param_5,
             int param_6)

{
  byte bVar1;
  byte bVar2;
  byte *pbVar3;
  byte bVar4;
  int iVar5;
  uint uVar6;
  byte *pbVar7;
  int iVar8;
  undefined2 uVar9;
  undefined2 uVar10;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  byte local_105;
  uint local_104;
  byte local_102 [256];
  
  iVar5 = param_6;
  bVar4 = param_3;
  pbVar7 = (byte *)param_4;
  bVar1 = *param_4;
  pbVar3 = local_102;
  local_102[0] = bVar1;
  for (uVar6 = (uint)bVar1; pbVar3 = pbVar3 + 1, pbVar7 = pbVar7 + 1, uVar6 != 0; uVar6 = uVar6 - 1)
  {
    *pbVar3 = *pbVar7;
  }
  uVar9 = (undefined2)((ulong)param_1 >> 0x10);
  iVar8 = (int)param_1;
  *(undefined1 *)0x65f0 = *(undefined1 *)(iVar8 + 0x273f);
  if (bVar1 != 0) {
    local_104 = 1;
    while( true ) {
      local_105 = local_102[local_104];
      if (local_105 == 0) {
        param_5 = param_5 + (uint)*(byte *)0x65f0;
        param_6 = iVar5;
      }
      else {
        if (local_105 == 0xff) {
          if (bVar4 == 1) {
            param_3 = local_102[local_104 + 1];
          }
          local_105 = local_102[local_104 + 2];
          local_104 = local_104 + 2;
        }
        local_105 = local_105 - 2;
        bVar2 = *(byte *)(iVar8 + (uint)local_105 * 0x40 + 0x3f);
        uVar10 = (undefined2)((ulong)param_2 >> 0x10);
        if ((int)(0x13f - (uint)bVar2) < param_6) {
          param_5 = param_5 + (uint)*(byte *)0x65f0;
          FUN_2971_67f6(0x1ec2,CONCAT11((char)((uint)local_105 * 0x40 >> 8),param_3),
                        iVar8 + (uint)local_105 * 0x40,uVar9,(int)param_2,uVar10,param_5,iVar5);
          param_6 = iVar5;
        }
        else {
          FUN_2971_67f6(0x1ec2,CONCAT11((char)((uint)local_105 * 0x40 >> 8),param_3),
                        iVar8 + (uint)local_105 * 0x40,uVar9,(int)param_2,uVar10,param_5,param_6);
        }
        param_6 = param_6 + (uint)bVar2;
      }
      if (local_104 == bVar1) break;
      local_104 = local_104 + 1;
    }
  }
  return;
}

