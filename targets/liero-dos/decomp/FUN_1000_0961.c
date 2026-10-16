
undefined1 FUN_1000_0961(uint param_1,int param_2,int param_3)

{
  uint uVar1;
  byte bVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  undefined2 unaff_DS;
  
  FUN_24dd_0530();
  iVar3 = param_3 + -2;
  if (iVar3 <= param_3 + 2) {
    while( true ) {
      iVar4 = param_2 + -2;
      if (iVar4 <= param_2 + 2) {
        while( true ) {
          iVar5 = 0x20;
          bVar2 = FUN_24dd_4161();
          if ((*(byte *)(iVar5 + 0x6604) & bVar2) != 0) {
            return 0;
          }
          if (iVar4 == param_2 + 2) break;
          iVar4 = iVar4 + 1;
        }
      }
      if (iVar3 == param_3 + 2) break;
      iVar3 = iVar3 + 1;
    }
  }
  while( true ) {
    iVar3 = 0x20;
    bVar2 = FUN_24dd_4161();
    if ((*(byte *)(iVar3 + 0x14c0) & bVar2) == 0) break;
    param_2 = param_2 + 1;
  }
  if (*(byte *)0x669c != 0) {
    uVar1 = 1;
    while( true ) {
      if ((((uVar1 != param_1) && (*(char *)((int)*(undefined4 *)0x6698 + uVar1 * 0xe + -2) != '\0')
           ) && (param_3 + -0x1e < *(int *)((int)*(undefined4 *)0x6698 + uVar1 * 0xe + -0xe))) &&
         (((*(int *)((int)*(undefined4 *)0x6698 + uVar1 * 0xe + -0xe) < param_3 + -0x1e &&
           (param_2 + -0x1e < *(int *)((int)*(undefined4 *)0x6698 + uVar1 * 0xe + -10))) &&
          (*(int *)((int)*(undefined4 *)0x6698 + uVar1 * 0xe + -10) < param_2 + -0x1e)))) {
        return 0;
      }
      if (uVar1 == *(byte *)0x669c) break;
      uVar1 = uVar1 + 1;
    }
  }
  return 1;
}

