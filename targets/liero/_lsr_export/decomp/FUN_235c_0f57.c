
void FUN_235c_0f57(char param_1,uint param_2,uint *param_3,undefined2 *param_4)

{
  uint uVar1;
  uint uVar2;
  uint uVar3;
  uint uVar4;
  int iVar5;
  uint uVar6;
  undefined2 *puVar7;
  uint *puVar8;
  undefined2 uVar9;
  undefined2 uVar10;
  undefined2 unaff_DS;
  undefined4 uVar11;
  int local_a;
  undefined2 uVar12;
  
  uVar9 = (undefined2)((ulong)param_4 >> 0x10);
  puVar7 = (undefined2 *)param_4;
  uVar1 = puVar7[3];
  uVar2 = puVar7[4];
  local_a = 0x6856;
  *(undefined2 *)0x782a = *param_4;
  *(undefined2 *)0x7830 = 0;
  uVar12 = unaff_DS;
  while (param_2 != 0) {
    uVar10 = (undefined2)((ulong)param_3 >> 0x10);
    puVar8 = (uint *)param_3;
    uVar4 = (uVar2 - puVar8[1]) - (uint)(uVar1 < *param_3);
    if (((int)uVar4 < 1) && ((0x7fff < uVar4 || (uVar1 - *param_3 <= param_2)))) {
      uVar4 = *param_3;
      uVar6 = puVar8[1];
      *(int *)0x7826 = uVar1 - *param_3;
      *(int *)0x7828 = (uVar2 - uVar6) - (uint)(uVar1 < uVar4);
    }
    else {
      *(uint *)0x7826 = param_2;
      *(undefined2 *)0x7828 = 0;
    }
    uVar4 = puVar7[1];
    iVar5 = puVar7[2];
    uVar6 = *param_3;
    uVar3 = puVar8[1];
    *(int *)0x782c = uVar4 + *param_3;
    *(int *)0x782e = iVar5 + uVar3 + (uint)CARRY2(uVar4,uVar6);
    uVar4 = *param_3;
    uVar6 = puVar8[1];
    uVar3 = *(uint *)0x7826;
    iVar5 = *(int *)0x7828;
    *param_3 = uVar4 + *(uint *)0x7826;
    puVar8[1] = uVar6 + iVar5 + (uint)CARRY2(uVar4,uVar3);
    if (param_1 != '\0') {
      uVar4 = uVar1;
      uVar6 = uVar2;
      FUN_24dd_3dbd();
      *param_3 = uVar4;
      puVar8[1] = uVar6;
    }
    *(int *)0x7832 = local_a;
    *(undefined2 *)0x7834 = uVar12;
    uVar11 = FUN_235c_0b33(local_a + *(int *)0x7826,uVar12);
    uVar12 = (undefined2)((ulong)uVar11 >> 0x10);
    local_a = (int)uVar11;
    param_2 = param_2 - *(int *)0x7826;
    iVar5 = *(int *)0x7828 + (uint)(0xfffe < *(uint *)0x7826);
    FUN_24dd_3dbd();
    uVar10 = FUN_24dd_3d80();
    *(undefined2 *)0x7826 = uVar10;
    *(int *)0x7828 = iVar5;
    FUN_2494_0060(0x7826,unaff_DS);
  }
  return;
}

