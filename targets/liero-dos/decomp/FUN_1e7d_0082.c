
undefined2 FUN_1e7d_0082(char param_1,undefined1 param_2,byte *param_3)

{
  byte *pbVar1;
  byte *pbVar2;
  undefined1 extraout_AH;
  int iVar3;
  undefined2 uVar4;
  uint uVar5;
  byte *pbVar6;
  undefined2 unaff_SS;
  undefined1 *puVar7;
  undefined2 uVar8;
  undefined1 *puVar9;
  undefined2 uVar10;
  undefined1 local_408 [254];
  undefined1 local_30a [2];
  undefined1 local_308 [256];
  int local_208 [2];
  undefined1 local_204 [256];
  byte local_104;
  byte abStack_103 [255];
  undefined2 local_4;
  
  pbVar6 = (byte *)param_3;
  local_104 = *param_3;
  pbVar2 = abStack_103;
  for (uVar5 = (uint)local_104; pbVar6 = pbVar6 + 1, uVar5 != 0; uVar5 = uVar5 - 1) {
    pbVar1 = pbVar2;
    pbVar2 = pbVar2 + 1;
    *pbVar1 = *pbVar6;
  }
  FUN_24dd_3eaf(0xff,local_204,unaff_SS,&local_104,unaff_SS);
  puVar9 = local_308;
  uVar4 = unaff_SS;
  FUN_24dd_3fb1(CONCAT11(extraout_AH,param_2));
  iVar3 = FUN_24dd_3f40(local_204,unaff_SS,puVar9,uVar4);
  if (iVar3 == 0) {
    local_4 = 0xff;
  }
  else {
    puVar9 = local_204;
    uVar8 = 1;
    puVar7 = local_408;
    uVar4 = unaff_SS;
    uVar10 = unaff_SS;
    FUN_24dd_3fb1(param_2);
    uVar4 = FUN_24dd_3f40(local_204,unaff_SS,puVar7,uVar4);
    FUN_24dd_403d(uVar4,uVar8,puVar9,uVar10);
    puVar9 = local_204;
    puVar7 = local_30a;
    uVar4 = unaff_SS;
    uVar10 = unaff_SS;
    FUN_24dd_3e95(0x7e,0x24dd);
    uVar4 = FUN_24dd_3f40(local_204,unaff_SS,puVar7,uVar4);
    FUN_24dd_403d(0xff,uVar4,puVar9,uVar10);
    if (param_1 != '\0') {
      puVar9 = local_30a;
      uVar4 = unaff_SS;
      FUN_24dd_3e95(0x80,0x24dd);
      FUN_24dd_3fde(1,0xff,local_204,unaff_SS,puVar9,uVar4);
    }
    local_4 = FUN_24dd_4824(local_208,unaff_SS,local_204,unaff_SS);
    if (local_208[0] != 0) {
      local_4 = 0xff;
    }
  }
  return local_4;
}

