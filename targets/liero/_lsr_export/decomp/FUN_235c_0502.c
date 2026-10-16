
undefined1 FUN_235c_0502(undefined1 *param_1,undefined1 *param_2)

{
  undefined1 *puVar1;
  undefined1 *puVar2;
  int iVar3;
  undefined1 *puVar4;
  undefined1 *puVar5;
  undefined2 unaff_SS;
  undefined1 in_ZF;
  undefined2 uVar6;
  undefined2 uVar7;
  undefined1 local_216 [256];
  undefined1 local_116 [256];
  int local_16;
  undefined1 local_14 [8];
  undefined1 local_c [9];
  undefined1 local_3;
  
  puVar5 = local_c;
  puVar4 = (undefined1 *)param_2;
  for (iVar3 = 8; iVar3 != 0; iVar3 = iVar3 + -1) {
    puVar2 = puVar5;
    puVar5 = puVar5 + 1;
    puVar1 = puVar4;
    puVar4 = puVar4 + 1;
    *puVar2 = *puVar1;
  }
  puVar5 = local_14;
  puVar4 = (undefined1 *)param_1;
  for (iVar3 = 8; iVar3 != 0; iVar3 = iVar3 + -1) {
    puVar2 = puVar5;
    puVar5 = puVar5 + 1;
    puVar1 = puVar4;
    puVar4 = puVar4 + 1;
    *puVar2 = *puVar1;
  }
  local_3 = 1;
  local_16 = 1;
  while( true ) {
    puVar5 = local_116;
    uVar7 = unaff_SS;
    FUN_24dd_3fc3(8,local_c,unaff_SS);
    puVar4 = local_216;
    uVar6 = unaff_SS;
    FUN_24dd_3fc3(8,local_14,unaff_SS);
    FUN_24dd_3f86(puVar4,uVar6,puVar5,uVar7);
    if (!(bool)in_ZF) {
      local_3 = 0;
    }
    if (local_16 == 8) break;
    local_16 = local_16 + 1;
    in_ZF = local_16 == 0;
  }
  return local_3;
}

