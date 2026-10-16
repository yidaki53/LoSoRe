
/* WARNING: Restarted to delay deadcode elimination for space: stack */

void FUN_24dd_18d9(int param_1,byte param_2)

{
  uint *puVar1;
  byte bVar2;
  int *piVar3;
  undefined2 *puVar4;
  uint *puVar5;
  uint uVar6;
  byte bVar7;
  uint in_CX;
  uint uVar8;
  int iVar9;
  uint uVar10;
  uint uVar11;
  int iVar12;
  uint in_BX;
  int iVar13;
  uint uVar14;
  int iVar15;
  uint *puVar16;
  uint *puVar17;
  undefined2 unaff_ES;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  bool bVar18;
  undefined4 uVar19;
  
  FUN_24dd_0642();
  puVar16 = (uint *)((uint)param_2 * 0xc + -0xc + param_1);
  while( true ) {
    bVar2 = param_2 - 1;
    if (bVar2 == 0 || (char)param_2 < '\x01') break;
    puVar4 = (undefined2 *)*(int *)0xd8;
    *(byte *)(puVar4 + 5) = *(byte *)(puVar4 + 5) ^ *(byte *)(puVar4 + 0xb);
    uVar19 = FUN_24dd_1190();
    *puVar4 = (int)uVar19;
    puVar4[1] = in_BX;
    puVar4[2] = in_CX;
    puVar4[3] = (int)((ulong)uVar19 >> 0x10);
    puVar17 = puVar16 + -6;
    puVar5 = (uint *)*(undefined2 *)0xd8;
    in_BX = *puVar17;
    in_CX = puVar16[-5];
    uVar8 = puVar16[-4];
    uVar11 = puVar16[-3];
    bVar7 = (byte)puVar16[-1];
    puVar16 = puVar17;
    param_2 = bVar2;
    if (bVar7 == (byte)puVar5[5]) {
      puVar1 = puVar5;
      uVar6 = *puVar1;
      *puVar1 = *puVar1 + in_BX;
      puVar1 = puVar5 + 1;
      uVar14 = *puVar1;
      uVar10 = *puVar1;
      *puVar1 = uVar10 + in_CX + (uint)CARRY2(uVar6,in_BX);
      puVar1 = puVar5 + 2;
      uVar10 = (uint)(CARRY2(uVar14,in_CX) || CARRY2(uVar10 + in_CX,(uint)CARRY2(uVar6,in_BX)));
      uVar14 = *puVar1;
      uVar6 = *puVar1;
      *puVar1 = uVar6 + uVar8 + uVar10;
      puVar5[3] = puVar5[3] + uVar11 + (uint)(CARRY2(uVar14,uVar8) || CARRY2(uVar6 + uVar8,uVar10));
    }
    else {
      bVar18 = in_BX < *puVar5;
      in_BX = in_BX - *puVar5;
      uVar6 = (uint)bVar18;
      bVar18 = in_CX < puVar5[1];
      uVar14 = in_CX - puVar5[1];
      in_CX = uVar14 - uVar6;
      uVar6 = (uint)(bVar18 || uVar14 < uVar6);
      uVar14 = uVar8 - puVar5[2];
      uVar10 = uVar14 - uVar6;
      uVar8 = (uint)(uVar8 < puVar5[2] || uVar14 < uVar6);
      uVar6 = uVar11 - puVar5[3];
      uVar14 = uVar6 - uVar8;
      if (uVar11 < puVar5[3] || uVar6 < uVar8) {
        uVar11 = ~uVar10;
        uVar8 = ~in_CX;
        bVar18 = in_BX == 0;
        in_BX = -in_BX;
        in_CX = uVar8 + bVar18;
        uVar8 = (uint)CARRY2(uVar8,(uint)bVar18);
        uVar10 = uVar11 + uVar8;
        uVar14 = ~uVar14 + (uint)CARRY2(uVar11,uVar8);
        bVar7 = bVar7 ^ 1;
      }
      *puVar5 = in_BX;
      puVar5[1] = in_CX;
      puVar5[2] = uVar10;
      puVar5[3] = uVar14;
      *(byte *)(puVar5 + 5) = bVar7;
    }
  }
  puVar16 = (uint *)*(undefined2 *)0xd8;
  uVar8 = *puVar16;
  uVar11 = puVar16[1];
  uVar6 = puVar16[2];
  uVar14 = puVar16[3];
  uVar10 = puVar16[5];
  *(int *)0xd8 = (int)(puVar16 + 6);
  bVar18 = (char)uVar10 != '\x01';
  if (bVar18) {
    uVar10 = (uint)(CONCAT12((uVar14 & 1) != 0,uVar6) >> 1);
    uVar6 = (uint)(CONCAT12((uVar6 & 1) != 0,uVar11) >> 1);
    uVar11 = (uint)(CONCAT12((uVar11 & 1) != 0,uVar8) >> 1);
    uVar8 = (uint)((uVar8 & 1) != 0);
    iVar13 = uVar11 + uVar8;
    uVar8 = (uint)CARRY2(uVar11,uVar8);
    iVar9 = uVar6 + uVar8;
    uVar8 = (uint)CARRY2(uVar6,uVar8);
    iVar12 = uVar10 + uVar8;
    iVar15 = (int)(((ulong)uVar14 | 0x10000) >> 1) + (uint)CARRY2(uVar10,uVar8);
  }
  else {
    iVar13 = -uVar8;
    iVar9 = ~uVar11 + (uint)(uVar8 == 0);
    uVar8 = (uint)CARRY2(~uVar11,(uint)(uVar8 == 0));
    iVar12 = ~uVar6 + uVar8;
    iVar15 = ~uVar14 + (uint)CARRY2(~uVar6,uVar8);
  }
  piVar3 = (int *)*(int *)0xd8;
  *piVar3 = iVar13;
  piVar3[1] = iVar9;
  piVar3[2] = iVar12;
  piVar3[3] = iVar15;
  piVar3[4] = (uint)bVar18;
  piVar3[5] = 0;
  return;
}

