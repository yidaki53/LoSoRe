
void __cdecl16near FUN_24dd_1519(void)

{
  undefined2 *puVar1;
  ulong uVar2;
  uint uVar3;
  uint uVar4;
  uint uVar5;
  uint uVar6;
  int iVar7;
  uint uVar8;
  uint uVar9;
  int iVar10;
  int iVar11;
  uint uVar12;
  undefined2 unaff_ES;
  undefined2 unaff_DS;
  
  puVar1 = (undefined2 *)*(undefined2 *)0xd8;
  uVar9 = puVar1[3];
  uVar6 = puVar1[2];
  uVar8 = puVar1[1];
  iVar11 = (int)puVar1[4] >> 1;
  uVar3 = uVar6;
  if ((puVar1[4] & 1) != 0) {
    iVar11 = iVar11 + 1;
    uVar3 = uVar9 & 1;
    uVar9 = uVar9 >> 1;
    uVar3 = (uint)(CONCAT12(uVar3 != 0,uVar6) >> 1);
    uVar8 = (uint)(CONCAT12((uVar6 & 1) != 0,uVar8) >> 1);
  }
  if (uVar9 < 0xfffe) {
    uVar6 = (uint)(((ulong)uVar9 | 0x10000) >> 1);
    while( true ) {
      uVar4 = (uint)(CONCAT22(uVar9,uVar3) / (ulong)uVar6);
      if (uVar6 - 1 <= uVar4) break;
      uVar6 = (uint)(CONCAT12(CARRY2(uVar6,uVar4),uVar6 + uVar4) >> 1);
    }
    uVar5 = uVar4;
    uVar12 = uVar6;
    if (uVar6 < uVar4) {
      uVar5 = uVar6;
      uVar12 = uVar4;
    }
    uVar2 = (CONCAT22(uVar9,uVar3) % (ulong)uVar6 << 0x10 | (ulong)uVar8) / (ulong)uVar12;
    uVar6 = (uint)(((ulong)((uVar12 + uVar5 & 1) != 0) << 0x10 | uVar2 & 0xffff) >> 1);
    uVar9 = (uint)((uVar2 & 1) != 0);
    iVar7 = uVar6 + uVar9;
    iVar10 = (int)(CONCAT12(CARRY2(uVar12,uVar5),uVar12 + uVar5) >> 1) + (uint)CARRY2(uVar6,uVar9);
  }
  else {
    iVar10 = (int)(((ulong)uVar9 | 0x10000) >> 1);
    iVar7 = (int)(CONCAT12((uVar9 & 1) != 0,uVar3) >> 1);
  }
  *puVar1 = 0;
  puVar1[1] = 0;
  puVar1[2] = iVar7;
  puVar1[3] = iVar10;
  puVar1[4] = iVar11;
  puVar1[5] = 0;
  return;
}

