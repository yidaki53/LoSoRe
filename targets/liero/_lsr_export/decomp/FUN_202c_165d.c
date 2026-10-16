
void __stdcall16far
FUN_202c_165d(undefined2 param_1,uint param_2,int param_3,uint param_4,int param_5,
             undefined2 param_6,undefined2 param_7,int param_8,byte param_9)

{
  uint *puVar1;
  int *piVar2;
  uint uVar3;
  byte bVar4;
  undefined1 uVar5;
  int iVar6;
  uint uVar7;
  uint uVar8;
  uint uVar9;
  int iVar10;
  int iVar11;
  uint *puVar12;
  undefined2 uVar13;
  undefined2 unaff_DS;
  int iVar14;
  int local_4;
  
  for (local_4 = 0;
      (*(char *)((int)*(undefined4 *)0x6694 + local_4 * 0x14 + 0x12) != '\0' && (local_4 < 600));
      local_4 = local_4 + 1) {
  }
  bVar4 = param_9 & 0x7f;
  *(byte *)((int)*(undefined4 *)0x6694 + local_4 * 0x14 + 0x12) = param_9;
  *(undefined2 *)((int)*(undefined4 *)0x6694 + local_4 * 0x14 + 2) = param_7;
  *(undefined2 *)((int)*(undefined4 *)0x6694 + local_4 * 0x14 + 6) = param_6;
  iVar6 = FUN_24dd_4654(*(undefined2 *)((uint)bVar4 * 2 + 0x53c));
  iVar11 = *(int *)((uint)bVar4 * 2 + 0x50c);
  uVar7 = FUN_24dd_4654(*(int *)((uint)bVar4 * 2 + 0x56c) << 1);
  iVar14 = 0;
  uVar3 = *(uint *)((uint)bVar4 * 2 + 0x56c);
  iVar6 = iVar11 - iVar6 >> 0xf;
  iVar11 = iVar6;
  FUN_24dd_3d80();
  uVar8 = FUN_24dd_3dbd();
  uVar9 = (uVar8 + param_4) - uVar3;
  uVar13 = (undefined2)((ulong)*(undefined4 *)0x6694 >> 0x10);
  iVar10 = (int)*(undefined4 *)0x6694 + local_4 * 0x14;
  *(int *)(iVar10 + 8) = uVar9 + uVar7;
  *(int *)(iVar10 + 10) =
       (((iVar11 + param_5 + (uint)CARRY2(uVar8,param_4)) - ((int)uVar3 >> 0xf)) -
       (uint)(uVar8 + param_4 < uVar3)) + iVar14 + (uint)CARRY2(uVar9,uVar7);
  uVar7 = FUN_24dd_4654(*(int *)((uint)bVar4 * 2 + 0x56c) << 1);
  iVar10 = 0;
  uVar3 = *(uint *)((uint)bVar4 * 2 + 0x56c);
  FUN_24dd_3d80();
  uVar8 = FUN_24dd_3dbd();
  uVar9 = (uVar8 + param_2) - uVar3;
  uVar13 = (undefined2)((ulong)*(undefined4 *)0x6694 >> 0x10);
  iVar11 = (int)*(undefined4 *)0x6694 + local_4 * 0x14;
  *(int *)(iVar11 + 0xc) = uVar9 + uVar7;
  *(int *)(iVar11 + 0xe) =
       (((iVar6 + param_3 + (uint)CARRY2(uVar8,param_2)) - ((int)uVar3 >> 0xf)) -
       (uint)(uVar8 + param_2 < uVar3)) + iVar10 + (uint)CARRY2(uVar9,uVar7);
  uVar13 = (undefined2)((ulong)*(undefined4 *)0x6694 >> 0x10);
  iVar11 = (int)*(undefined4 *)0x6694 + local_4 * 0x14;
  uVar7 = *(uint *)(iVar11 + 8);
  iVar11 = *(int *)(iVar11 + 10);
  uVar13 = (undefined2)((ulong)*(undefined4 *)0x6694 >> 0x10);
  puVar12 = (uint *)((int)*(undefined4 *)0x6694 + local_4 * 0x14);
  puVar1 = puVar12;
  uVar3 = *puVar1;
  *puVar1 = *puVar1 + uVar7;
  puVar1 = puVar12 + 1;
  *puVar1 = *puVar1 + iVar11 + (uint)CARRY2(uVar3,uVar7);
  uVar13 = (undefined2)((ulong)*(undefined4 *)0x6694 >> 0x10);
  iVar11 = (int)*(undefined4 *)0x6694 + local_4 * 0x14;
  uVar7 = *(uint *)(iVar11 + 0xc);
  iVar11 = *(int *)(iVar11 + 0xe);
  uVar13 = (undefined2)((ulong)*(undefined4 *)0x6694 >> 0x10);
  iVar6 = (int)*(undefined4 *)0x6694 + local_4 * 0x14;
  puVar1 = (uint *)(iVar6 + 4);
  uVar3 = *puVar1;
  *puVar1 = *puVar1 + uVar7;
  piVar2 = (int *)(iVar6 + 6);
  *piVar2 = *piVar2 + iVar11 + (uint)CARRY2(uVar3,uVar7);
  if (*(char *)(bVar4 + 0x645) == '\0') {
    if (param_8 < 1) {
      *(undefined1 *)((int)*(undefined4 *)0x6694 + local_4 * 0x14 + 0x13) =
           *(undefined1 *)(bVar4 + 0x68d);
    }
    else {
      *(undefined1 *)((int)*(undefined4 *)0x6694 + local_4 * 0x14 + 0x13) = (undefined1)param_8;
    }
  }
  else {
    uVar5 = FUN_24dd_4654(*(byte *)(bVar4 + 0x65d) + 1);
    *(undefined1 *)((int)*(undefined4 *)0x6694 + local_4 * 0x14 + 0x13) = uVar5;
  }
  iVar11 = FUN_24dd_4654(*(undefined2 *)((uint)bVar4 * 2 + 0x7c4));
  *(int *)((int)*(undefined4 *)0x6694 + local_4 * 0x14 + 0x10) =
       *(int *)((uint)bVar4 * 2 + 0x794) - iVar11;
  return;
}

