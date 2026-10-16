
void __cdecl16near FUN_24dd_17d1(void)

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
  uint uVar15;
  uint uVar16;
  uint uVar17;
  uint uVar18;
  uint uVar19;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  
  puVar1 = (uint *)*(int *)0xd8;
  uVar4 = *puVar1;
  uVar14 = puVar1[1];
  uVar15 = puVar1[2];
  uVar16 = puVar1[3];
  uVar19 = 0;
  uVar3 = puVar1[4];
  uVar5 = uVar4;
  uVar11 = uVar15;
  uVar10 = uVar16;
  if (uVar3 != 0xc001) {
    if ((int)uVar3 < -0xf) {
      uVar10 = 0;
      uVar5 = uVar14;
      uVar11 = uVar16;
      uVar14 = uVar15;
      uVar3 = uVar3 + 0x10;
      uVar19 = uVar4;
    }
    while (uVar3 + 1 == 0 || (int)uVar3 < -1) {
      uVar4 = uVar10 & 1;
      uVar10 = uVar10 >> 1;
      uVar15 = uVar11 & 1;
      uVar19 = (uint)(CONCAT12((uVar5 & 1) != 0,uVar19) >> 1);
      uVar5 = (uint)(CONCAT12((uVar14 & 1) != 0,uVar5) >> 1);
      uVar11 = (uint)(CONCAT12(uVar4 != 0,uVar11) >> 1);
      uVar14 = (uint)(CONCAT12(uVar15 != 0,uVar14) >> 1);
      uVar3 = uVar3 + 1;
    }
  }
  uVar4 = (uint)CARRY2(uVar5,(uint)((int)uVar19 < 0));
  uVar15 = (uint)CARRY2(uVar14,uVar4);
  *puVar1 = uVar5 + ((int)uVar19 < 0);
  puVar1[1] = uVar14 + uVar4;
  puVar1[2] = uVar11 + uVar15;
  puVar1[3] = uVar10 + CARRY2(uVar11,uVar15);
  uVar14 = 0;
  uVar4 = 0;
  if ((*(byte *)((int)puVar1 + 3) & 0x80) != 0) {
    uVar14 = *puVar1 << 1;
    uVar4 = puVar1[1] << 1 | (uint)((int)*puVar1 < 0);
  }
  uVar11 = (uint)((ulong)*puVar1 * (ulong)puVar1[2] >> 0x10);
  uVar3 = (uint)((ulong)*puVar1 * (ulong)puVar1[2]);
  uVar19 = uVar4 + uVar11 + (uint)CARRY2(uVar14,uVar3);
  uVar15 = (uint)CARRY2(uVar14 + uVar3,uVar3);
  uVar16 = uVar19 + uVar11;
  uVar5 = uVar16 + uVar15;
  uVar18 = (uint)(CARRY2(uVar4,uVar11) || CARRY2(uVar4 + uVar11,(uint)CARRY2(uVar14,uVar3))) +
           (uint)(CARRY2(uVar19,uVar11) || CARRY2(uVar16,uVar15));
  uVar12 = (uint)((ulong)puVar1[1] * (ulong)puVar1[2] >> 0x10);
  uVar14 = (uint)((ulong)puVar1[1] * (ulong)puVar1[2]);
  uVar15 = uVar5 + uVar14;
  uVar4 = (uint)CARRY2(uVar5,uVar14);
  uVar19 = uVar18 + uVar12;
  uVar6 = uVar19 + uVar4;
  uVar16 = uVar15 + uVar14;
  uVar14 = (uint)CARRY2(uVar15,uVar14);
  uVar5 = uVar6 + uVar12;
  uVar7 = uVar5 + uVar14;
  uVar13 = (uint)((ulong)*puVar1 * (ulong)puVar1[3] >> 0x10);
  uVar3 = (uint)((ulong)*puVar1 * (ulong)puVar1[3]);
  uVar17 = uVar16 + uVar3;
  uVar15 = (uint)CARRY2(uVar16,uVar3);
  uVar11 = uVar7 + uVar13;
  uVar8 = uVar11 + uVar15;
  uVar16 = (uint)CARRY2(uVar17,uVar3);
  uVar10 = uVar8 + uVar13;
  uVar9 = uVar10 + uVar16;
  uVar3 = (uint)((int)(uVar17 + uVar3) < 0);
  uVar17 = uVar9 + uVar3;
  uVar12 = (uint)(CARRY2(uVar18,uVar12) || CARRY2(uVar19,uVar4)) +
           (uint)(CARRY2(uVar6,uVar12) || CARRY2(uVar5,uVar14)) +
           (uint)(CARRY2(uVar7,uVar13) || CARRY2(uVar11,uVar15)) +
           (uint)(CARRY2(uVar8,uVar13) || CARRY2(uVar10,uVar16)) + (uint)CARRY2(uVar9,uVar3);
  lVar2 = (ulong)puVar1[2] * (ulong)puVar1[2];
  uVar7 = (uint)((ulong)lVar2 >> 0x10);
  uVar4 = (uint)lVar2;
  uVar14 = uVar17 + uVar4;
  uVar4 = (uint)CARRY2(uVar17,uVar4);
  uVar16 = uVar12 + uVar7;
  uVar11 = uVar16 + uVar4;
  uVar8 = (uint)((ulong)puVar1[3] * (ulong)puVar1[1] >> 0x10);
  uVar5 = (uint)((ulong)puVar1[3] * (ulong)puVar1[1]);
  uVar9 = uVar14 + uVar5;
  uVar14 = (uint)CARRY2(uVar14,uVar5);
  uVar3 = uVar11 + uVar8;
  uVar10 = uVar3 + uVar14;
  uVar15 = (uint)CARRY2(uVar9,uVar5);
  uVar19 = uVar10 + uVar8;
  uVar6 = uVar19 + uVar15;
  uVar10 = (uint)(CARRY2(uVar12,uVar7) || CARRY2(uVar16,uVar4)) +
           (uint)(CARRY2(uVar11,uVar8) || CARRY2(uVar3,uVar14)) +
           (uint)(CARRY2(uVar10,uVar8) || CARRY2(uVar19,uVar15));
  uVar11 = (uint)((ulong)puVar1[3] * (ulong)puVar1[2] >> 0x10);
  uVar3 = (uint)((ulong)puVar1[3] * (ulong)puVar1[2]);
  uVar19 = uVar6 + uVar3;
  uVar4 = (uint)CARRY2(uVar6,uVar3);
  uVar15 = uVar10 + uVar11;
  uVar6 = uVar15 + uVar4;
  uVar14 = (uint)CARRY2(uVar19,uVar3);
  uVar16 = uVar6 + uVar11;
  lVar2 = (ulong)puVar1[3] * (ulong)puVar1[3] +
          CONCAT22((uint)(CARRY2(uVar10,uVar11) || CARRY2(uVar15,uVar4)) +
                   (uint)(CARRY2(uVar6,uVar11) || CARRY2(uVar16,uVar14)),uVar16 + uVar14);
  *puVar1 = uVar9 + uVar5;
  puVar1[1] = uVar19 + uVar3;
  puVar1[2] = (uint)lVar2;
  puVar1[3] = (uint)((ulong)lVar2 >> 0x10);
  *(undefined1 *)(puVar1 + 5) = 0;
  puVar1[4] = 0;
  return;
}

