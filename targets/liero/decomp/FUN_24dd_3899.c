
void __cdecl16near FUN_24dd_3899(void)

{
  undefined1 *puVar1;
  undefined1 *puVar2;
  undefined4 uVar3;
  uint in_AX;
  uint uVar4;
  undefined2 in_DX;
  int in_BX;
  int iVar5;
  undefined1 *unaff_SI;
  undefined1 *puVar6;
  undefined2 unaff_ES;
  undefined2 unaff_DS;
  bool bVar7;
  
  if (*(int *)0x6410 == 0) {
    if (*(int *)(in_BX + 2) != -0x284e) {
      *(undefined2 *)0x6410 = 0x69;
      return;
    }
    do {
      uVar4 = *(int *)(in_BX + 4) - *(int *)(in_BX + 8);
      bVar7 = in_AX < uVar4;
      in_AX = in_AX - uVar4;
      if (bVar7) {
        uVar4 = uVar4 + in_AX;
        in_AX = 0;
      }
      uVar3 = *(undefined4 *)(in_BX + 0xc);
      iVar5 = (int)uVar3;
      puVar6 = (undefined1 *)(*(int *)(in_BX + 8) + iVar5);
      for (; uVar4 != 0; uVar4 = uVar4 - 1) {
        puVar2 = puVar6;
        puVar6 = puVar6 + 1;
        puVar1 = unaff_SI;
        unaff_SI = unaff_SI + 1;
        *puVar2 = *puVar1;
      }
      iVar5 = (int)puVar6 - iVar5;
      *(int *)(in_BX + 8) = iVar5;
      if (iVar5 == *(int *)(in_BX + 4)) {
        FUN_24dd_396c();
      }
    } while (in_AX != 0);
  }
  return;
}

