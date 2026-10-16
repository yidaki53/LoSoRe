
void __stdcall16far
FUN_1ec2_0b0d(undefined4 param_1,undefined1 param_2,int param_3,int param_4,int param_5,int param_6)

{
  uint uVar1;
  uint uVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  int iVar7;
  undefined2 uVar8;
  int local_8;
  int local_6;
  int local_4;
  
  local_4 = param_6;
  local_6 = param_5;
  uVar1 = param_4 - param_6;
  uVar2 = param_3 - param_5;
  iVar3 = FUN_1ec2_0ae3(&stack0xfffe,uVar1);
  iVar4 = FUN_1ec2_0ae3(&stack0xfffe,uVar2);
  iVar5 = (uVar1 ^ (int)uVar1 >> 0xf) - ((int)uVar1 >> 0xf);
  iVar6 = (uVar2 ^ (int)uVar2 >> 0xf) - ((int)uVar2 >> 0xf);
  uVar8 = (undefined2)((ulong)param_1 >> 0x10);
  if (iVar6 < iVar5) {
    local_8 = -(iVar5 / 2);
    while (local_4 != param_4) {
      local_8 = local_8 + iVar6;
      local_4 = local_4 + iVar3;
      iVar7 = local_4;
      if (0 < local_8) {
        local_6 = local_6 + iVar4;
        iVar7 = local_8 - iVar5;
        local_8 = iVar7;
      }
      FUN_1ec2_0dc8((int)param_1,uVar8,CONCAT11((char)((uint)iVar7 >> 8),param_2),local_6,local_4);
    }
  }
  else {
    local_8 = -(iVar6 / 2);
    while (local_6 != param_3) {
      local_8 = local_8 + iVar5;
      local_6 = local_6 + iVar4;
      iVar7 = local_6;
      if (0 < local_8) {
        local_4 = local_4 + iVar3;
        iVar7 = local_8 - iVar6;
        local_8 = iVar7;
      }
      FUN_1ec2_0dc8((int)param_1,uVar8,CONCAT11((char)((uint)iVar7 >> 8),param_2),local_6,local_4);
    }
  }
  return;
}

