
void __stdcall16far FUN_235c_0711(byte *param_1,undefined4 *param_2)

{
  uint *puVar1;
  uint uVar2;
  byte *pbVar3;
  byte *pbVar4;
  int iVar5;
  uint uVar6;
  byte *pbVar7;
  int iVar8;
  undefined2 uVar9;
  undefined2 uVar10;
  undefined2 uVar11;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  bool bVar12;
  undefined4 uVar13;
  uint local_90a;
  int local_908;
  undefined1 local_906 [2052];
  byte local_102;
  byte abStack_101 [255];
  
  pbVar7 = (byte *)param_1;
  local_102 = *param_1;
  pbVar4 = abStack_101;
  for (uVar6 = (uint)local_102; pbVar7 = pbVar7 + 1, uVar6 != 0; uVar6 = uVar6 - 1) {
    pbVar3 = pbVar4;
    pbVar4 = pbVar4 + 1;
    *pbVar3 = *pbVar7;
  }
  FUN_235c_056f(&local_102,unaff_SS);
  uVar13 = FUN_24dd_028a(10);
  *(int *)param_2 = (int)uVar13;
  *(undefined2 *)((int)(undefined4 *)param_2 + 2) = (int)((ulong)uVar13 >> 0x10);
  uVar10 = *(undefined2 *)0x7814;
  uVar9 = (undefined2)((ulong)*param_2 >> 0x10);
  iVar8 = (int)*param_2;
  *(undefined2 *)(iVar8 + 6) = *(undefined2 *)0x7812;
  *(undefined2 *)(iVar8 + 8) = uVar10;
  if (*(char *)0x7688 == '\0') {
    uVar10 = (undefined2)((ulong)*param_2 >> 0x10);
    iVar8 = (int)*param_2;
    *(undefined2 *)(iVar8 + 2) = 0;
    *(undefined2 *)(iVar8 + 4) = 0;
    uVar11 = (undefined2)((ulong)*param_2 >> 0x10);
    uVar9 = (undefined2)*param_2;
    uVar10 = FUN_24dd_3dbd(uVar9,uVar11);
    FUN_2494_0027(uVar10,uVar9,uVar11);
  }
  else {
    uVar10 = *(undefined2 *)0x768e;
    uVar9 = (undefined2)((ulong)*param_2 >> 0x10);
    iVar8 = (int)*param_2;
    *(undefined2 *)(iVar8 + 2) = *(undefined2 *)0x768c;
    *(undefined2 *)(iVar8 + 4) = uVar10;
    *(undefined2 *)*param_2 = *(undefined2 *)0x768a;
    uVar6 = *(uint *)0x768c;
    iVar8 = *(int *)0x768e;
    uVar2 = *(uint *)0x7812;
    iVar5 = *(int *)0x7814;
    *(int *)0x768c = uVar6 + *(uint *)0x7812;
    *(int *)0x768e = iVar8 + iVar5 + (uint)CARRY2(uVar6,uVar2);
    uVar10 = *(undefined2 *)0x768a;
    uVar9 = FUN_24dd_3dbd(uVar10);
    FUN_2494_003d(uVar9,uVar10);
  }
  *(undefined2 *)0x781a = 0;
  *(int *)0x781c = (int)local_906;
  *(undefined2 *)0x781e = unaff_SS;
  *(undefined2 *)0x7820 = *(undefined2 *)*param_2;
  uVar9 = (undefined2)((ulong)*param_2 >> 0x10);
  iVar8 = (int)*param_2;
  uVar10 = *(undefined2 *)(iVar8 + 4);
  *(undefined2 *)0x7822 = *(undefined2 *)(iVar8 + 2);
  *(undefined2 *)0x7824 = uVar10;
  uVar10 = (undefined2)((ulong)*param_2 >> 0x10);
  iVar8 = (int)*param_2;
  local_90a = *(uint *)(iVar8 + 6);
  local_908 = *(int *)(iVar8 + 8);
  do {
    do {
      uVar13 = FUN_235c_06d7(0x800,0,local_90a,local_908);
      *(undefined2 *)0x7816 = (int)uVar13;
      *(undefined2 *)0x7818 = (int)((ulong)uVar13 >> 0x10);
      FUN_24dd_3c48(0,0,*(undefined2 *)0x7816,local_906,unaff_SS,0x7792,unaff_DS);
      FUN_24dd_04f4();
      iVar8 = *(int *)0x7818 + (uint)(0xfffe < *(uint *)0x7816);
      FUN_24dd_3dbd();
      uVar10 = FUN_24dd_3d80();
      *(undefined2 *)0x7816 = uVar10;
      *(int *)0x7818 = iVar8;
      FUN_2494_0060(0x7816,unaff_DS);
      uVar2 = *(uint *)0x7816;
      iVar8 = *(int *)0x7818;
      puVar1 = (uint *)0x7822;
      uVar6 = *puVar1;
      *puVar1 = *puVar1 + uVar2;
      *(int *)0x7824 = *(int *)0x7824 + iVar8 + (uint)CARRY2(uVar6,uVar2);
      bVar12 = local_90a < *(uint *)0x7816;
      local_90a = local_90a - *(uint *)0x7816;
      local_908 = (local_908 - *(int *)0x7818) - (uint)bVar12;
    } while (0 < local_908);
  } while ((-1 < local_908) && (local_90a != 0));
  FUN_24dd_3bde(0x7792,unaff_DS);
  FUN_24dd_04f4();
  return;
}

