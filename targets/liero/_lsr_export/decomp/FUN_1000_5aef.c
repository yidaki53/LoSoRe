
void FUN_1000_5aef(int param_1)

{
  uint *puVar1;
  byte bVar2;
  uint uVar3;
  int iVar4;
  uint uVar5;
  int iVar6;
  undefined2 *puVar7;
  undefined2 uVar8;
  undefined2 unaff_DS;
  bool bVar9;
  undefined2 *puVar10;
  undefined2 uVar11;
  undefined2 uVar12;
  
  uVar12 = 0x1000;
  uVar11 = 0x5afa;
  FUN_24dd_0530();
  uVar8 = (undefined2)((ulong)*(undefined4 *)0x6698 >> 0x10);
  iVar6 = (int)*(undefined4 *)0x6698 + param_1 * 0xe;
  puVar10 = (undefined2 *)CONCAT22(uVar8,(undefined2 *)(iVar6 + -0xe));
  uVar5 = *(uint *)(iVar6 + -8);
  iVar4 = *(int *)(iVar6 + -6);
  puVar1 = (uint *)(iVar6 + -0xc);
  uVar3 = *puVar1;
  *puVar1 = *puVar1 + uVar5;
  *(int *)(iVar6 + -10) = *(int *)(iVar6 + -10) + iVar4 + (uint)CARRY2(uVar3,uVar5);
  iVar4 = 0x20;
  bVar2 = FUN_24dd_4161();
  puVar7 = (undefined2 *)puVar10;
  uVar8 = (undefined2)((ulong)puVar10 >> 0x10);
  if ((*(byte *)(iVar4 + 0x14c0) & bVar2) != 0) {
    puVar1 = puVar7 + 3;
    uVar3 = *puVar1;
    *puVar1 = *puVar1 + 0x5dc;
    puVar7[4] = puVar7[4] + (uint)(0xfa23 < uVar3);
  }
  iVar4 = puVar7[2] + puVar7[4] + (uint)CARRY2(puVar7[1],puVar7[3]);
  iVar6 = 0x20;
  bVar2 = FUN_24dd_4161(puVar10,puVar7[1] + puVar7[3],iVar4,uVar11,uVar12);
  if (((*(byte *)(iVar6 + 0x6604) & bVar2) != 0) || (0x15c < iVar4)) {
    uVar3 = ((undefined2 *)puVar10)[4];
    FUN_24dd_3d80();
    iVar4 = FUN_24dd_3dbd();
    uVar8 = (undefined2)((ulong)puVar10 >> 0x10);
    puVar7 = (undefined2 *)puVar10;
    puVar7[3] = -iVar4;
    puVar7[4] = (~uVar3 + 1) - (uint)(iVar4 != 0);
    uVar3 = puVar7[3];
    uVar5 = puVar7[4];
    if ((int)uVar5 < 0) {
      bVar9 = uVar3 != 0;
      uVar3 = -uVar3;
      uVar5 = (~uVar5 + 1) - (uint)bVar9;
    }
    if (((int)uVar5 < 0) || (((int)uVar5 < 1 && (uVar3 < 100)))) {
      puVar7[3] = 0;
      puVar7[4] = 0;
    }
  }
  uVar8 = (undefined2)((ulong)puVar10 >> 0x10);
  puVar7 = (undefined2 *)puVar10;
  puVar7[5] = puVar7[5] + -1;
  if (puVar7[5] == 0) {
    FUN_202c_1b84(0x24dd,puVar7[2],*puVar10,*(undefined1 *)(*(byte *)(puVar7 + 6) + 0x135f));
    *(undefined1 *)((undefined2 *)puVar10 + 6) = 0;
  }
  return;
}

