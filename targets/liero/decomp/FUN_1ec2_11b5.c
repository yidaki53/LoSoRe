
void __stdcall16far FUN_1ec2_11b5(int param_1,byte *param_2)

{
  byte *pbVar1;
  byte *pbVar2;
  uint uVar3;
  byte bVar4;
  int iVar5;
  byte *pbVar6;
  byte *pbVar7;
  undefined2 unaff_SS;
  uint local_30a;
  uint local_308;
  uint local_306;
  byte local_303;
  byte local_302 [768];
  
  pbVar7 = local_302;
  pbVar6 = (byte *)param_2;
  for (iVar5 = 0x300; iVar5 != 0; iVar5 = iVar5 + -1) {
    pbVar2 = pbVar7;
    pbVar7 = pbVar7 + 1;
    pbVar1 = pbVar6;
    pbVar6 = pbVar6 + 1;
    *pbVar2 = *pbVar1;
  }
  local_303 = 0;
  while( true ) {
    local_306 = param_1 * 0x3f + (uint)local_302[(uint)local_303 * 3] * (0x20 - param_1) >> 5;
    local_308 = param_1 * 0x3f + (uint)local_302[(uint)local_303 * 3 + 1] * (0x20 - param_1) >> 5;
    uVar3 = param_1 * 0x3f + (uint)local_302[(uint)local_303 * 3 + 2] * (0x20 - param_1);
    local_30a = uVar3 >> 5;
    if (0x3f < local_306) {
      local_306 = 0x3f;
    }
    if (0x3f < local_308) {
      local_308 = 0x3f;
    }
    if (0x3f < local_30a) {
      local_30a = 0x3f;
    }
    bVar4 = (byte)(uVar3 >> 0xd);
    FUN_1ec2_10cf(CONCAT11(bVar4,(undefined1)local_30a),CONCAT11(bVar4,(undefined1)local_308),
                  CONCAT11(bVar4,(undefined1)local_306),CONCAT11(bVar4,local_303));
    if (local_303 == 0xff) break;
    local_303 = local_303 + 1;
  }
  return;
}

