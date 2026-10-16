
undefined4 __cdecl16near FUN_24dd_1190(void)

{
  uint *puVar1;
  long lVar2;
  uint uVar3;
  uint uVar4;
  uint uVar5;
  uint uVar6;
  uint uVar7;
  uint uVar8;
  uint uVar9;
  uint uVar10;
  uint uVar11;
  uint uVar12;
  uint uVar13;
  uint uVar14;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  bool bVar15;
  
  puVar1 = (uint *)*(int *)0xd8;
  uVar11 = 0;
  uVar4 = 0;
  uVar8 = 0;
  if ((*(byte *)((int)puVar1 + 0xf) & 0x80) != 0) {
    uVar4 = *puVar1;
    uVar8 = puVar1[1];
  }
  if ((*(byte *)((int)puVar1 + 3) & 0x80) != 0) {
    bVar15 = CARRY2(uVar4,puVar1[6]);
    uVar4 = uVar4 + puVar1[6];
    uVar11 = (uint)bVar15;
    bVar15 = CARRY2(uVar8,puVar1[7]);
    uVar6 = uVar8 + puVar1[7];
    uVar8 = uVar6 + uVar11;
    uVar11 = (uint)(bVar15 || CARRY2(uVar6,uVar11));
    if ((*(byte *)((int)puVar1 + 0xf) & 0x80) != 0) {
      uVar11 = uVar11 - 1;
    }
  }
  uVar7 = 0;
  uVar5 = (uint)((ulong)puVar1[6] * (ulong)puVar1[2] >> 0x10);
  uVar3 = (uint)((ulong)puVar1[6] * (ulong)puVar1[2]);
  uVar6 = (uint)CARRY2(uVar4,uVar3);
  uVar12 = uVar8 + uVar5;
  uVar9 = uVar12 + uVar6;
  uVar11 = uVar11 + (CARRY2(uVar8,uVar5) || CARRY2(uVar12,uVar6));
  if (puVar1[8] != 0) {
    lVar2 = (ulong)puVar1[8] * (ulong)*puVar1;
    uVar6 = (uint)((ulong)lVar2 >> 0x10);
    uVar4 = (uint)CARRY2(uVar4 + uVar3,(uint)lVar2);
    uVar8 = uVar9 + uVar6;
    uVar7 = uVar8 + uVar4;
    uVar12 = uVar11 + (CARRY2(uVar9,uVar6) || CARRY2(uVar8,uVar4));
    uVar6 = (uint)((ulong)puVar1[8] * (ulong)puVar1[1] >> 0x10);
    uVar4 = (uint)((ulong)puVar1[8] * (ulong)puVar1[1]);
    uVar9 = uVar7 + uVar4;
    uVar4 = (uint)CARRY2(uVar7,uVar4);
    uVar8 = uVar12 + uVar6;
    uVar11 = uVar8 + uVar4;
    uVar7 = (uint)(CARRY2(uVar12,uVar6) || CARRY2(uVar8,uVar4));
  }
  uVar5 = (uint)((ulong)puVar1[6] * (ulong)puVar1[3] >> 0x10);
  uVar4 = (uint)((ulong)puVar1[6] * (ulong)puVar1[3]);
  uVar10 = uVar9 + uVar4;
  uVar4 = (uint)CARRY2(uVar9,uVar4);
  uVar6 = uVar11 + uVar5;
  uVar13 = uVar6 + uVar4;
  uVar9 = (uint)((ulong)puVar1[7] * (ulong)puVar1[2] >> 0x10);
  uVar3 = (uint)((ulong)puVar1[7] * (ulong)puVar1[2]);
  uVar8 = (uint)CARRY2(uVar10,uVar3);
  uVar12 = uVar13 + uVar9;
  uVar14 = uVar12 + uVar8;
  uVar4 = uVar7 + (CARRY2(uVar11,uVar5) || CARRY2(uVar6,uVar4)) +
          (uint)(CARRY2(uVar13,uVar9) || CARRY2(uVar12,uVar8));
  if (puVar1[9] != 0) {
    lVar2 = (ulong)puVar1[9] * (ulong)*puVar1;
    uVar11 = (uint)((ulong)lVar2 >> 0x10);
    uVar8 = (uint)CARRY2(uVar10 + uVar3,(uint)lVar2);
    bVar15 = CARRY2(uVar14,uVar11);
    uVar11 = uVar14 + uVar11;
    uVar14 = uVar11 + uVar8;
    uVar4 = uVar4 + (bVar15 || CARRY2(uVar11,uVar8));
  }
  uVar11 = 0;
  uVar7 = (uint)((ulong)puVar1[7] * (ulong)puVar1[3] >> 0x10);
  uVar8 = (uint)((ulong)puVar1[7] * (ulong)puVar1[3]);
  uVar3 = uVar14 + uVar8;
  uVar8 = (uint)CARRY2(uVar14,uVar8);
  uVar6 = uVar4 + uVar7;
  uVar12 = uVar6 + uVar8;
  uVar4 = (uint)(CARRY2(uVar4,uVar7) || CARRY2(uVar6,uVar8));
  if (puVar1[8] != 0) {
    lVar2 = (ulong)puVar1[8] * (ulong)puVar1[2];
    uVar6 = (uint)((ulong)lVar2 >> 0x10);
    uVar8 = (uint)lVar2;
    bVar15 = CARRY2(uVar3,uVar8);
    uVar3 = uVar3 + uVar8;
    uVar8 = (uint)bVar15;
    uVar11 = uVar12 + uVar6;
    uVar5 = uVar11 + uVar8;
    uVar6 = uVar4 + (CARRY2(uVar12,uVar6) || CARRY2(uVar11,uVar8));
    uVar7 = (uint)((ulong)puVar1[8] * (ulong)puVar1[3] >> 0x10);
    uVar4 = (uint)((ulong)puVar1[8] * (ulong)puVar1[3]);
    uVar12 = uVar5 + uVar4;
    uVar8 = (uint)CARRY2(uVar5,uVar4);
    uVar11 = uVar6 + uVar7;
    uVar4 = uVar11 + uVar8;
    uVar11 = (uint)(CARRY2(uVar6,uVar7) || CARRY2(uVar11,uVar8));
  }
  if (puVar1[9] != 0) {
    lVar2 = (ulong)puVar1[9] * (ulong)puVar1[1];
    uVar6 = (uint)((ulong)lVar2 >> 0x10);
    uVar8 = (uint)lVar2;
    bVar15 = CARRY2(uVar3,uVar8);
    uVar3 = uVar3 + uVar8;
    uVar8 = (uint)bVar15;
    uVar7 = uVar12 + uVar6;
    uVar6 = (uint)(CARRY2(uVar12,uVar6) || CARRY2(uVar7,uVar8));
    uVar12 = uVar4 + uVar6;
    uVar5 = (uint)((ulong)puVar1[9] * (ulong)puVar1[2] >> 0x10);
    uVar8 = (uint)CARRY2(uVar7 + uVar8,(uint)((ulong)puVar1[9] * (ulong)puVar1[2]));
    uVar7 = uVar12 + uVar5;
    uVar11 = uVar11 + CARRY2(uVar4,uVar6) + (uint)(CARRY2(uVar12,uVar5) || CARRY2(uVar7,uVar8)) +
             (int)((ulong)puVar1[9] * (ulong)puVar1[3] >> 0x10) +
             (uint)CARRY2(uVar7 + uVar8,(uint)((ulong)puVar1[9] * (ulong)puVar1[3]));
  }
  return CONCAT22(uVar11,uVar3);
}

