
void __cdecl16near FUN_1000_0ac7(void)

{
  char cVar1;
  int iVar2;
  undefined2 uVar3;
  int iVar4;
  undefined2 uVar5;
  undefined2 unaff_DS;
  undefined4 local_8;
  int local_4;
  
  FUN_24dd_0530();
  for (local_4 = 1;
      (*(char *)((int)*(undefined4 *)0x6698 + local_4 * 0xe + -2) != '\0' &&
      (local_4 <= (int)(uint)*(byte *)0x669c)); local_4 = local_4 + 1) {
  }
  if (local_4 <= (int)(uint)*(byte *)0x669c) {
    uVar5 = (undefined2)((ulong)*(undefined4 *)0x6698 >> 0x10);
    iVar4 = (int)*(undefined4 *)0x6698 + local_4 * 0xe;
    local_8 = (undefined2 *)CONCAT22(uVar5,(undefined2 *)(iVar4 + -0xe));
    cVar1 = FUN_24dd_4654(2);
    *(char *)(iVar4 + -2) = cVar1 + '\x01';
    iVar2 = FUN_24dd_4654(*(undefined2 *)((uint)*(byte *)(iVar4 + -2) * 2 + 0x1364));
    *(int *)(iVar4 + -4) = *(int *)((uint)*(byte *)(iVar4 + -2) * 2 + 0x1360) + iVar2;
    if (*(char *)(iVar4 + -2) == '\x01') {
      cVar1 = FUN_24dd_4654(0x28);
      *(char *)(iVar4 + -1) = cVar1 + '\x01';
      while (*(char *)(*(byte *)(iVar4 + -1) + 0x66af) == '\x02') {
        cVar1 = FUN_24dd_4654(0x28);
        *(char *)(iVar4 + -1) = cVar1 + '\x01';
      }
    }
    *(undefined2 *)(iVar4 + -8) = 0;
    *(undefined2 *)(iVar4 + -6) = 0;
    do {
      uVar3 = FUN_24dd_4654(0x1f8);
      *local_8 = uVar3;
      uVar3 = FUN_24dd_4654(0x15e);
      *(undefined2 *)(iVar4 + -10) = uVar3;
      cVar1 = FUN_1000_0961(local_4,*(undefined2 *)(iVar4 + -10),*local_8);
    } while (cVar1 == '\0');
    FUN_202c_1b84(0x24dd,*(undefined2 *)(iVar4 + -10),*local_8,8);
  }
  return;
}

