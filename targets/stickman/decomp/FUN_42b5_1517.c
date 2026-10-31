
void __cdecl16near FUN_42b5_1517(void)

{
  char *pcVar1;
  ulong uVar2;
  ulong uVar3;
  uint uVar4;
  char in_AL;
  uint uVar5;
  char cVar6;
  int iVar7;
  uint uVar8;
  uint in_BX;
  uint uVar9;
  char *unaff_DI;
  undefined2 unaff_ES;
  bool bVar10;
  bool bVar11;
  undefined4 uVar12;
  
  if (in_AL != '\0') {
    uVar12 = FUN_42b5_168c();
    if ((byte)uVar12 < 0x81) {
      uVar12 = FUN_42b5_1718();
    }
    uVar8 = (uint)((ulong)uVar12 >> 0x10) | 0x8000;
    uVar5 = (uint)uVar12 & 0xff00;
    for (cVar6 = -0x7c - (char)uVar12; cVar6 != '\0'; cVar6 = cVar6 + -1) {
      uVar4 = uVar8 & 1;
      uVar8 = uVar8 >> 1;
      uVar5 = (uint)(CONCAT12((in_BX & 1) != 0,uVar5) >> 1);
      in_BX = (uint)(CONCAT12(uVar4 != 0,in_BX) >> 1);
    }
    iVar7 = 0xc;
    do {
      *unaff_DI = (byte)(uVar8 >> 0xc) + 0x30;
      uVar2 = (ulong)CONCAT12((int)uVar5 < 0,in_BX) << 1;
      uVar9 = (uint)((uVar2 & 0xffff | (ulong)((int)uVar5 < 0)) << 1) |
              (uint)((int)(uVar5 << 1) < 0);
      uVar4 = (uint)CARRY2(uVar5 * 4,uVar5);
      bVar10 = CARRY2(uVar9,in_BX);
      uVar9 = uVar9 + in_BX;
      bVar11 = (int)(uVar5 * 5) < 0;
      uVar5 = uVar5 * 10;
      uVar3 = (ulong)CONCAT12(bVar11,uVar9 + uVar4) << 1;
      in_BX = (uint)uVar3 | (uint)bVar11;
      uVar8 = ((((uVar8 & 0xfff) << 1 | (uint)((uVar2 & 0x10000) != 0)) << 1 |
               (uint)((uVar2 & 0x8000) != 0)) + (uVar8 & 0xfff) +
              (uint)(bVar10 || CARRY2(uVar9,uVar4))) * 2 | (uint)((uVar3 & 0x10000) != 0);
      unaff_DI = unaff_DI + 1;
      iVar7 = iVar7 + -1;
    } while (iVar7 != 0);
    *unaff_DI = '\0';
    return;
  }
  for (iVar7 = 6; iVar7 != 0; iVar7 = iVar7 + -1) {
    pcVar1 = unaff_DI;
    unaff_DI = unaff_DI + 2;
    pcVar1[0] = '0';
    pcVar1[1] = '0';
  }
  *unaff_DI = '\0';
  return;
}

