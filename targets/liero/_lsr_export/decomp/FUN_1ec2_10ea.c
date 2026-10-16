
void __stdcall16far FUN_1ec2_10ea(int param_1,byte *param_2)

{
  byte *pbVar1;
  byte *pbVar2;
  byte bVar3;
  int iVar4;
  byte *pbVar5;
  byte *pbVar6;
  undefined2 unaff_SS;
  uint local_30a;
  uint local_308;
  uint local_306;
  byte local_303;
  byte local_302 [768];
  
  pbVar6 = local_302;
  pbVar5 = (byte *)param_2;
  for (iVar4 = 0x300; iVar4 != 0; iVar4 = iVar4 + -1) {
    pbVar2 = pbVar6;
    pbVar6 = pbVar6 + 1;
    pbVar1 = pbVar5;
    pbVar5 = pbVar5 + 1;
    *pbVar2 = *pbVar1;
  }
  local_303 = 0;
  while( true ) {
    local_306 = (uint)local_302[(uint)local_303 * 3] * param_1 >> 5;
    local_308 = (uint)local_302[(uint)local_303 * 3 + 1] * param_1 >> 5;
    local_30a = (uint)local_302[(uint)local_303 * 3 + 2] * param_1 >> 5;
    if (0x3f < local_306) {
      local_306 = 0x3f;
    }
    if (0x3f < local_308) {
      local_308 = 0x3f;
    }
    if (0x3f < local_30a) {
      local_30a = 0x3f;
    }
    bVar3 = (byte)((uint)local_302[(uint)local_303 * 3 + 2] * param_1 >> 0xd);
    FUN_1ec2_10cf(CONCAT11(bVar3,(undefined1)local_30a),CONCAT11(bVar3,(undefined1)local_308),
                  CONCAT11(bVar3,(undefined1)local_306),CONCAT11(bVar3,local_303));
    if (local_303 == 0xff) break;
    local_303 = local_303 + 1;
  }
  return;
}

