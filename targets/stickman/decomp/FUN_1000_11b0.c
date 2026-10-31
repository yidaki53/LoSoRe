
undefined1 __cdecl16near FUN_1000_11b0(void)

{
  char cVar1;
  undefined2 unaff_DS;
  bool bVar2;
  bool local_4;
  undefined1 local_3;
  
  FUN_42b5_04df();
  local_3 = 1;
  if ((*(int *)0x3b0 < 0x12) && (*(char *)0x3a6 == '\0')) {
    bVar2 = *(char *)((*(int *)0x3b0 + 3) * 0x50 + *(int *)0x3ae + 0x1f6e) == '\x02';
    if (bVar2) {
      *(undefined1 *)((*(int *)0x3b0 + 3) * 0x50 + *(int *)0x3ae + 0x1f6e) = 0;
      FUN_1000_04bc(*(int *)0x3b0 + 3,*(int *)0x3ae + -1);
    }
    local_4 = *(char *)((*(int *)0x3b0 + 3) * 0x50 + *(int *)0x3ae + 0x1f6f) == '\x02';
    if (local_4) {
      *(undefined1 *)((*(int *)0x3b0 + 3) * 0x50 + *(int *)0x3ae + 0x1f6f) = 0;
      FUN_1000_04bc(*(int *)0x3b0 + 3,*(undefined2 *)0x3ae);
    }
    local_3 = 1;
    local_4 = local_4 || bVar2;
    if (*(char *)((*(int *)0x3b0 + 3) * 0x50 + *(int *)0x3ae + 0x1f70) == '\x02') {
      *(undefined1 *)((*(int *)0x3b0 + 3) * 0x50 + *(int *)0x3ae + 0x1f70) = 0;
      FUN_1000_04bc(*(int *)0x3b0 + 3,*(int *)0x3ae + 1);
      local_4 = true;
    }
    cVar1 = FUN_1000_0c8f(*(int *)0x3b0 + 3,*(int *)0x3ae + -1);
    if ((((cVar1 == '\0') &&
         (cVar1 = FUN_1000_0c8f(*(int *)0x3b0 + 3,*(undefined2 *)0x3ae), cVar1 == '\0')) &&
        (cVar1 = FUN_1000_0c8f(*(int *)0x3b0 + 3,*(int *)0x3ae + 1), cVar1 == '\0')) && (!local_4))
    {
      local_3 = 0;
    }
  }
  return local_3;
}

