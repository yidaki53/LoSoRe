
void __stdcall16far
FUN_202c_18c0(char param_1,uint param_2,int param_3,uint param_4,int param_5,int param_6,
             undefined2 param_7,undefined2 param_8,undefined2 param_9,undefined2 param_10,
             byte param_11)

{
  uint uVar1;
  byte bVar2;
  undefined1 uVar3;
  char cVar4;
  uint uVar5;
  uint uVar6;
  uint uVar7;
  undefined2 *puVar8;
  int iVar9;
  int iVar10;
  undefined2 uVar11;
  undefined2 unaff_DS;
  int iVar12;
  int local_6;
  int local_4;
  
  for (local_4 = 0;
      (*(char *)((int)*(undefined4 *)0x6688 + local_4 * 0x14 + 0x10) != '\0' && (local_4 < 600));
      local_4 = local_4 + 1) {
  }
  bVar2 = param_11 & 0x7f;
  *(byte *)((int)*(undefined4 *)0x6688 + local_4 * 0x14 + 0x10) = param_11;
  uVar11 = (undefined2)((ulong)*(undefined4 *)0x6688 >> 0x10);
  puVar8 = (undefined2 *)((int)*(undefined4 *)0x6688 + local_4 * 0x14);
  *puVar8 = param_9;
  puVar8[1] = param_10;
  uVar11 = (undefined2)((ulong)*(undefined4 *)0x6688 >> 0x10);
  iVar9 = (int)*(undefined4 *)0x6688 + local_4 * 0x14;
  *(undefined2 *)(iVar9 + 4) = param_7;
  *(undefined2 *)(iVar9 + 6) = param_8;
  uVar5 = FUN_24dd_4654(*(int *)((uint)bVar2 * 2 + 0xc7c) << 1);
  iVar12 = 0;
  uVar1 = *(uint *)((uint)bVar2 * 2 + 0xc7c);
  param_6 = param_6 >> 0xf;
  iVar9 = param_6;
  FUN_24dd_3d80();
  uVar6 = FUN_24dd_3dbd();
  uVar7 = (uVar6 + param_4) - uVar1;
  uVar11 = (undefined2)((ulong)*(undefined4 *)0x6688 >> 0x10);
  iVar10 = (int)*(undefined4 *)0x6688 + local_4 * 0x14;
  *(int *)(iVar10 + 8) = uVar7 + uVar5;
  *(int *)(iVar10 + 10) =
       (((iVar9 + param_5 + (uint)CARRY2(uVar6,param_4)) - ((int)uVar1 >> 0xf)) -
       (uint)(uVar6 + param_4 < uVar1)) + iVar12 + (uint)CARRY2(uVar7,uVar5);
  uVar5 = FUN_24dd_4654(*(int *)((uint)bVar2 * 2 + 0xc7c) << 1);
  iVar10 = 0;
  uVar1 = *(uint *)((uint)bVar2 * 2 + 0xc7c);
  FUN_24dd_3d80();
  uVar6 = FUN_24dd_3dbd();
  uVar7 = (uVar6 + param_2) - uVar1;
  uVar11 = (undefined2)((ulong)*(undefined4 *)0x6688 >> 0x10);
  iVar9 = (int)*(undefined4 *)0x6688 + local_4 * 0x14;
  *(int *)(iVar9 + 0xc) = uVar7 + uVar5;
  *(int *)(iVar9 + 0xe) =
       (((param_6 + param_3 + (uint)CARRY2(uVar6,param_2)) - ((int)uVar1 >> 0xf)) -
       (uint)(uVar6 + param_2 < uVar1)) + iVar10 + (uint)CARRY2(uVar7,uVar5);
  if (*(uint *)((uint)bVar2 * 2 + 0x1104) < 0x8000) {
    cVar4 = *(char *)(bVar2 + 0x11a5);
    if (cVar4 == '\0') {
      if (*(char *)(bVar2 + 0x117d) == '\x01') {
        if (*(char *)(bVar2 + 0x1155) == '\0') {
          uVar3 = FUN_24dd_4654(2);
          *(undefined1 *)((int)*(undefined4 *)0x6688 + local_4 * 0x14 + 0x11) = uVar3;
        }
        else {
          uVar3 = FUN_24dd_4654(*(byte *)(bVar2 + 0x1155) + 1);
          *(undefined1 *)((int)*(undefined4 *)0x6688 + local_4 * 0x14 + 0x11) = uVar3;
        }
      }
      else {
        *(undefined1 *)((int)*(undefined4 *)0x6688 + local_4 * 0x14 + 0x11) = 0;
      }
    }
    else if (cVar4 == '\x01') {
      if ('@' < param_1) {
        param_1 = param_1 + -1;
      }
      local_6 = (param_1 + -0xc) / 8;
      if (local_6 < 0) {
        local_6 = 0;
      }
      if (0xc < local_6) {
        local_6 = 0xc;
      }
      *(undefined1 *)((int)*(undefined4 *)0x6688 + local_4 * 0x14 + 0x11) = (undefined1)local_6;
    }
    else if ((cVar4 == '\x02') || (cVar4 == '\x03')) {
      *(char *)((int)*(undefined4 *)0x6688 + local_4 * 0x14 + 0x11) = param_1;
    }
    else {
      *(undefined1 *)((int)*(undefined4 *)0x6688 + local_4 * 0x14 + 0x11) = 0;
    }
  }
  else {
    cVar4 = FUN_24dd_4654(2);
    *(char *)((int)*(undefined4 *)0x6688 + local_4 * 0x14 + 0x11) =
         *(char *)(bVar2 + 0x11cd) - cVar4;
  }
  iVar9 = FUN_24dd_4654(*(undefined2 *)((uint)bVar2 * 2 + 0x1064));
  *(int *)((int)*(undefined4 *)0x6688 + local_4 * 0x14 + 0x12) =
       *(int *)((uint)bVar2 * 2 + 0x1014) - iVar9;
  return;
}

