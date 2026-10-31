
void __cdecl16near FUN_1000_1e1b(void)

{
  char cVar1;
  undefined1 uVar2;
  int iVar3;
  int iVar4;
  undefined2 unaff_DS;
  bool bVar5;
  undefined2 uVar6;
  
  uVar6 = 0x1000;
  FUN_42b5_04df();
  if (0x11 < *(int *)0x3b0) {
    return;
  }
  cVar1 = FUN_1000_1b9e(*(int *)0x3b0 + 3,*(int *)0x3ae + -1);
  if (((cVar1 != '\0') &&
      (cVar1 = FUN_1000_1b9e(*(int *)0x3b0 + 3,*(undefined2 *)0x3ae), cVar1 != '\0')) &&
     (cVar1 = FUN_1000_1b9e(*(int *)0x3b0 + 3,*(int *)0x3ae + 1), cVar1 != '\0')) {
    return;
  }
  if (*(char *)0x3a6 == '\0') {
    uVar6 = *(undefined2 *)0x3ae;
    cVar1 = *(char *)((*(int *)0x3b0 + 3) * 0x50 + *(int *)0x3ae + 0x1f6f);
    if (cVar1 == '\a') {
      *(int *)0x3ae = *(int *)0x3ae + 1;
    }
    else if (cVar1 != '\b') {
      if (cVar1 != '\t') {
        return;
      }
      *(int *)0x3ae = *(int *)0x3ae + -1;
    }
    *(undefined1 *)0x3a6 = 1;
    FUN_3de3_0b67(*(int *)0x3b0 + 1,uVar6);
    FUN_3de3_002d(0x1e0c,0x3de3);
    *(int *)0x3b0 = *(int *)0x3b0 + 1;
    if (*(char *)0x2 == '\0') {
      FUN_3de3_0bea(0x1def,0x3de3,*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
    }
    else {
      FUN_3de3_0bea(0x1de2,0x3de3,*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
    }
    *(bool *)2 = *(char *)0x2 == '\0';
    return;
  }
  FUN_1000_0614(uVar6);
  *(int *)0x3b0 = *(int *)0x3b0 + 1;
  iVar4 = (*(int *)0x3b0 + 2) * 0x50;
  iVar3 = iVar4 + *(int *)0x3ae;
  bVar5 = iVar3 == 0;
  FUN_42b5_0e79(0x1dc2,0x42b5,CONCAT11((char)((uint)iVar4 >> 8),*(undefined1 *)(iVar3 + 0x1f6f)));
  if (bVar5) {
    iVar4 = (*(int *)0x3b0 + 1) * 0x50;
    iVar3 = iVar4 + *(int *)0x3ae;
    bVar5 = iVar3 == 0;
    FUN_42b5_0e79(0x1dc2,0x42b5,CONCAT11((char)((uint)iVar4 >> 8),*(undefined1 *)(iVar3 + 0x1f6f)));
    if (bVar5) {
      iVar4 = *(int *)0x3b0 * 0x50 + *(int *)0x3ae;
      bVar5 = iVar4 == 0;
      FUN_42b5_0e79(0x1dc2,0x42b5,
                    CONCAT11((char)((uint)(*(int *)0x3b0 * 0x50) >> 8),
                             *(undefined1 *)(iVar4 + 0x1f6f)));
      if (bVar5) {
        uVar2 = 0;
        goto LAB_1000_1eea;
      }
    }
  }
  uVar2 = 1;
LAB_1000_1eea:
  *(undefined1 *)0x3a6 = uVar2;
  if (*(char *)0x3a6 == '\0') {
    FUN_3de3_0bea(0x1dfd,0x42b5,*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
  }
  else {
    if (*(char *)0x2 == '\0') {
      FUN_3de3_0bea(0x1def,0x42b5,*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
    }
    else {
      FUN_3de3_0bea(0x1de2,0x42b5,*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
    }
    *(bool *)2 = *(char *)0x2 == '\0';
  }
  FUN_1000_1619(10);
  return;
}

