
int __cdecl16far FUN_24dd_3dbd(void)

{
  uint uVar1;
  uint uVar2;
  int iVar3;
  int iVar4;
  ulong in_EAX;
  uint in_CX;
  uint in_DX;
  uint in_BX;
  int iVar5;
  uint uVar6;
  uint uVar7;
  int iVar8;
  undefined2 unaff_DS;
  bool bVar9;
  bool bVar10;
  bool bVar11;
  
  if (1 < *(byte *)0x6420) {
    if (CONCAT22(in_BX,in_CX) != 0) {
      return (int)((long)(in_EAX & 0xffff | (ulong)in_DX << 0x10) / CONCAT22(in_BX,in_CX));
    }
LAB_24dd_3e36:
    iVar4 = FUN_24dd_010f();
    return iVar4;
  }
  bVar11 = (int)in_DX < 0;
  if (bVar11) {
    iVar4 = (int)in_EAX;
    in_EAX = (ulong)(uint)-iVar4;
    in_DX = -(in_DX + (iVar4 != 0));
  }
  uVar7 = (uint)bVar11;
  if (in_BX == 0) {
    if (in_CX == 0) goto LAB_24dd_3e36;
LAB_24dd_3e3e:
    iVar4 = (int)(((ulong)in_DX % (ulong)in_CX << 0x10 | in_EAX & 0xffff) / (ulong)in_CX);
  }
  else {
    if ((int)in_BX < 0) {
      uVar7 = uVar7 + 2;
      bVar9 = in_CX != 0;
      in_CX = -in_CX;
      in_BX = -(in_BX + bVar9);
      if (in_BX == 0) goto LAB_24dd_3e3e;
    }
    iVar5 = 0;
    iVar4 = 0;
    iVar8 = 0x10;
    do {
      bVar9 = iVar4 < 0;
      iVar3 = iVar4 * 2;
      uVar2 = in_DX << 1 | (uint)((in_EAX & 0x8000) != 0);
      uVar6 = iVar5 << 1 | (uint)((in_DX & 0x8000) != 0);
      in_DX = uVar2 - in_CX;
      uVar2 = (uint)(uVar2 < in_CX);
      uVar1 = uVar6 - in_BX;
      iVar5 = uVar1 - uVar2;
      iVar4 = iVar3 + 1;
      if (uVar6 < in_BX || uVar1 < uVar2) {
        bVar10 = CARRY2(in_DX,in_CX);
        in_DX = in_DX + in_CX;
        iVar5 = iVar5 + in_BX + (uint)bVar10;
        iVar4 = iVar3;
      }
      iVar8 = iVar8 + -1;
      in_EAX = (in_EAX & 0xffff) << 1 | (ulong)bVar9;
    } while (iVar8 != 0);
  }
  uVar7 = uVar7 >> 1;
  if (bVar11) {
    uVar7 = uVar7 + 1;
  }
  if (uVar7 == 1) {
    iVar4 = -iVar4;
  }
  return iVar4;
}

