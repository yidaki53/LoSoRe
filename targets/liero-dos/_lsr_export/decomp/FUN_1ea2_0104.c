
undefined2 __stdcall16far FUN_1ea2_0104(undefined4 *param_1)

{
  int iVar1;
  undefined2 in_AX;
  undefined1 uVar2;
  undefined1 extraout_AH;
  int *piVar3;
  undefined2 *puVar4;
  undefined2 uVar5;
  undefined2 unaff_DS;
  int local_6;
  undefined1 local_3;
  
  uVar2 = (undefined1)((uint)in_AX >> 8);
  local_3 = 0;
  if (-1 < *(char *)0x65ee) {
    iVar1 = *(int *)(*(char *)0x65ee * 2 + 0x65e8);
    local_6 = 0;
    while( true ) {
      uVar5 = (undefined2)((ulong)*param_1 >> 0x10);
      piVar3 = (int *)((int)*param_1 + local_6 * 4);
      if (*piVar3 != 0 || piVar3[1] != 0) {
        uVar5 = (undefined2)((ulong)*param_1 >> 0x10);
        puVar4 = (undefined2 *)((int)*param_1 + local_6 * 4);
        FUN_24dd_029f(*(undefined2 *)(*(char *)0x65ee * 2 + 0x65e2),*puVar4,puVar4[1]);
      }
      if (local_6 == iVar1 + -1) break;
      local_6 = local_6 + 1;
    }
    FUN_24dd_029f(*(int *)(*(char *)0x65ee * 2 + 0x65e8) << 2,*(undefined2 *)param_1,
                  *(undefined2 *)((int)(undefined4 *)param_1 + 2));
    *(char *)0x65ee = *(char *)0x65ee + -1;
    local_3 = 1;
    uVar2 = extraout_AH;
  }
  return CONCAT11(uVar2,local_3);
}

