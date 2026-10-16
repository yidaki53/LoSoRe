
void __stdcall16far
FUN_1ec2_0895(undefined4 param_1,int param_2,int param_3,int param_4,int param_5)

{
  uint uVar1;
  uint uVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  int iVar7;
  int iVar8;
  undefined2 uVar9;
  int iVar10;
  int local_8;
  int local_6;
  int local_4;
  
  local_4 = param_5;
  local_6 = param_4;
  uVar1 = param_3 - param_5;
  uVar2 = param_2 - param_4;
  iVar3 = FUN_1ec2_086b(&stack0xfffe,uVar1);
  iVar4 = FUN_1ec2_086b(&stack0xfffe,uVar2);
  iVar5 = (uVar1 ^ (int)uVar1 >> 0xf) - ((int)uVar1 >> 0xf);
  iVar6 = (uVar2 ^ (int)uVar2 >> 0xf) - ((int)uVar2 >> 0xf);
  uVar9 = (undefined2)((ulong)param_1 >> 0x10);
  if (iVar6 < iVar5) {
    local_8 = -(iVar5 / 2);
    while (local_4 != param_3) {
      local_8 = local_8 + iVar6;
      local_4 = local_4 + iVar3;
      if (0 < local_8) {
        local_6 = local_6 + iVar4;
        local_8 = local_8 - iVar5;
      }
      iVar7 = FUN_24dd_4654(5);
      if (iVar7 == 0) {
        iVar7 = local_6;
        iVar10 = local_4;
        iVar8 = FUN_24dd_4654(2);
        FUN_1ec2_0dc8((int)param_1,uVar9,iVar8 + 0x53,iVar7,iVar10);
      }
    }
  }
  else {
    local_8 = -(iVar6 / 2);
    while (local_6 != param_2) {
      local_8 = local_8 + iVar5;
      local_6 = local_6 + iVar4;
      if (0 < local_8) {
        local_4 = local_4 + iVar3;
        local_8 = local_8 - iVar6;
      }
      iVar7 = FUN_24dd_4654(5);
      if (iVar7 == 0) {
        iVar7 = local_6;
        iVar10 = local_4;
        iVar8 = FUN_24dd_4654(2);
        FUN_1ec2_0dc8((int)param_1,uVar9,iVar8 + 0x53,iVar7,iVar10);
      }
    }
  }
  return;
}

