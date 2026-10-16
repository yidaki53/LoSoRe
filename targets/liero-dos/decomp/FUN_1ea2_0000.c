
undefined1 __stdcall16far FUN_1ea2_0000(uint param_1,undefined2 param_2,undefined4 *param_3)

{
  int iVar1;
  uint uVar2;
  uint uVar3;
  undefined2 *puVar4;
  undefined2 uVar5;
  undefined2 unaff_DS;
  undefined4 uVar6;
  int local_6;
  undefined1 local_3;
  
  local_3 = 0;
  if (*(char *)0x65ee < '\x03') {
    *(undefined2 *)(*(char *)0x65ee * 2 + 0x65e2) = param_2;
    *(uint *)(*(char *)0x65ee * 2 + 0x65e8) = param_1;
    uVar2 = FUN_24dd_0303();
    if ((param_1 < 0x8000) &&
       ((0 < (int)param_1 ||
        ((uint)(*(int *)(*(char *)0x65ee * 2 + 0x65e2) * *(int *)(*(char *)0x65ee * 2 + 0x65e8)) <=
         uVar2)))) {
      uVar6 = FUN_24dd_028a(*(int *)(*(char *)0x65ee * 2 + 0x65e8) << 2);
      uVar2 = (uint)((ulong)uVar6 >> 0x10);
      *(int *)param_3 = (int)uVar6;
      *(uint *)((int)(undefined4 *)param_3 + 2) = uVar2;
      iVar1 = *(int *)(*(char *)0x65ee * 2 + 0x65e8);
      local_6 = 0;
      while( true ) {
        uVar3 = FUN_24dd_0303();
        if (0x7fff < uVar2) {
          return 0;
        }
        if (((int)uVar2 < 1) && (uVar3 < *(uint *)(*(char *)0x65ee * 2 + 0x65e2))) {
          return 0;
        }
        uVar6 = FUN_24dd_028a(*(undefined2 *)(*(char *)0x65ee * 2 + 0x65e2));
        uVar2 = (uint)((ulong)uVar6 >> 0x10);
        uVar5 = (undefined2)((ulong)*param_3 >> 0x10);
        puVar4 = (undefined2 *)((int)*param_3 + local_6 * 4);
        *puVar4 = (int)uVar6;
        puVar4[1] = uVar2;
        if (local_6 == iVar1 + -1) break;
        local_6 = local_6 + 1;
      }
      *(char *)0x65ee = *(char *)0x65ee + '\x01';
      local_3 = 1;
    }
  }
  return local_3;
}

