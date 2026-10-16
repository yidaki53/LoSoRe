
undefined4 __cdecl16near FUN_24dd_4732(void)

{
  ulong uVar1;
  int iVar2;
  uint uVar3;
  int iVar4;
  uint uVar5;
  int in_CX;
  uint uVar6;
  uint uVar7;
  byte bVar8;
  byte bVar9;
  uint uVar10;
  char cVar11;
  uint uVar12;
  byte *unaff_DI;
  undefined2 unaff_ES;
  bool bVar13;
  
  iVar2 = 0;
  uVar6 = 0;
  uVar12 = 0;
  if (in_CX == 0) goto LAB_24dd_4797;
  if (*unaff_DI == 0x2b) {
LAB_24dd_4747:
    unaff_DI = unaff_DI + 1;
    in_CX = in_CX + -1;
    if (in_CX == 0) goto LAB_24dd_4797;
  }
  else if (*unaff_DI == 0x2d) {
    uVar12 = 0xffff;
    goto LAB_24dd_4747;
  }
  if (*unaff_DI != 0x24) {
    do {
      uVar10 = (uint)(byte)(*unaff_DI - 0x30);
      if ((byte)(*unaff_DI - 0x3a) < 0xf6) break;
      if ((uVar6 & 0xf000) != 0) goto LAB_24dd_4797;
      uVar3 = iVar2 * 2;
      uVar7 = uVar6 << 1 | (uint)(iVar2 < 0);
      iVar4 = iVar2 << 2;
      uVar5 = iVar2 * 8;
      uVar6 = iVar2 * 10;
      iVar2 = uVar6 + uVar10;
      uVar6 = ((uVar7 << 1 | (uint)((int)uVar3 < 0)) << 1 | (uint)(iVar4 < 0)) + uVar7 +
              (uint)CARRY2(uVar5,uVar3) + (uint)CARRY2(uVar6,uVar10);
      unaff_DI = unaff_DI + 1;
      in_CX = in_CX + -1;
    } while (in_CX != 0);
LAB_24dd_4781:
    if (iVar2 != 0 || uVar6 != 0) {
      if ((int)uVar12 < 0) {
        bVar13 = iVar2 != 0;
        iVar2 = -iVar2;
        uVar6 = -(uint)bVar13 - uVar6;
      }
      if ((int)(uVar12 ^ uVar6) < 0) goto LAB_24dd_4797;
    }
    return CONCAT22(uVar6,iVar2);
  }
  iVar4 = in_CX + -1;
  if (iVar4 != 0) {
    do {
      unaff_DI = unaff_DI + 1;
      bVar8 = *unaff_DI;
      if (0x60 < bVar8) {
        bVar8 = bVar8 - 0x20;
      }
      bVar9 = bVar8 - 0x30;
      if ((byte)(bVar8 - 0x3a) < 0xf6) {
        if ((byte)(bVar8 + 0xb9) < 0xfa) goto LAB_24dd_4781;
        bVar9 = bVar8 - 0x37;
      }
      cVar11 = '\x04';
      do {
        bVar13 = iVar2 < 0;
        iVar2 = iVar2 << 1;
        uVar1 = (ulong)CONCAT12(bVar13,uVar6) << 1;
        uVar6 = (uint)uVar1 | (uint)bVar13;
        if ((uVar1 & 0x10000) != 0) goto LAB_24dd_4797;
        cVar11 = cVar11 + -1;
      } while (cVar11 != '\0');
      iVar2 = CONCAT11((char)((uint)iVar2 >> 8),(byte)iVar2 | bVar9);
      iVar4 = iVar4 + -1;
      if (iVar4 == 0) {
        if ((int)uVar12 < 0) {
          bVar13 = iVar2 != 0;
          iVar2 = -iVar2;
          uVar6 = -(uint)bVar13 - uVar6;
        }
        return CONCAT22(uVar6,iVar2);
      }
    } while( true );
  }
LAB_24dd_4797:
  return CONCAT22(uVar6,iVar2);
}

