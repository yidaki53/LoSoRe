
undefined2 __cdecl16near FUN_1000_9e7a(void)

{
  char cVar1;
  int iVar2;
  undefined1 extraout_AH;
  uint uVar3;
  int iVar4;
  undefined2 uVar5;
  undefined2 unaff_DS;
  undefined1 local_3;
  
  local_3 = 0x10;
  FUN_24dd_0530();
  cVar1 = *(char *)0x66ac;
  uVar3 = CONCAT11(extraout_AH,cVar1);
  if (cVar1 != '\0') {
    if (cVar1 != '\x01') {
      if ((cVar1 != '\x02') && (cVar1 != '\x03')) goto LAB_1000_9f40;
      uVar3 = *(uint *)0x66a3;
      uVar5 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
      iVar4 = (int)*(undefined4 *)0x6670;
      iVar2 = *(int *)(iVar4 + 0x42);
      if (((int)uVar3 >> 0xf < iVar2) ||
         (((int)uVar3 >> 0xf <= iVar2 && (uVar3 <= *(uint *)(iVar4 + 0x40))))) {
LAB_1000_9f3b:
        uVar3 = CONCAT11((char)(uVar3 >> 8),1);
      }
      else {
        uVar3 = *(uint *)0x66a3;
        uVar5 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
        iVar4 = (int)*(undefined4 *)0x6670;
        iVar2 = *(int *)(iVar4 + 0xec);
        if (((int)uVar3 >> 0xf < iVar2) ||
           (((int)uVar3 >> 0xf <= iVar2 && (uVar3 <= *(uint *)(iVar4 + 0xea))))) goto LAB_1000_9f3b;
        uVar3 = uVar3 & 0xff00;
      }
      local_3 = (undefined1)uVar3;
      goto LAB_1000_9f40;
    }
    uVar3 = *(uint *)0x66a1;
    uVar5 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
    iVar4 = (int)*(undefined4 *)0x6670;
    iVar2 = *(int *)(iVar4 + 0x46);
    if (((int)uVar3 >> 0xf < iVar2) ||
       (((int)uVar3 >> 0xf <= iVar2 && (uVar3 <= *(uint *)(iVar4 + 0x44))))) {
LAB_1000_9efa:
      uVar3 = CONCAT11((char)(uVar3 >> 8),1);
    }
    else {
      uVar3 = *(uint *)0x66a1;
      uVar5 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
      iVar4 = (int)*(undefined4 *)0x6670;
      iVar2 = *(int *)(iVar4 + 0xf0);
      if (((int)uVar3 >> 0xf < iVar2) ||
         (((int)uVar3 >> 0xf <= iVar2 && (uVar3 <= *(uint *)(iVar4 + 0xee))))) goto LAB_1000_9efa;
      uVar3 = uVar3 & 0xff00;
    }
    local_3 = (undefined1)uVar3;
    goto LAB_1000_9f40;
  }
  uVar5 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
  iVar4 = (int)*(undefined4 *)0x6670;
  iVar2 = *(int *)(iVar4 + 0x3a);
  if ((iVar2 < 0) || ((iVar2 < 1 && (*(int *)(iVar4 + 0x38) == 0)))) {
LAB_1000_9ebd:
    local_3 = 1;
  }
  else {
    uVar5 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
    iVar4 = (int)*(undefined4 *)0x6670;
    iVar2 = *(int *)(iVar4 + 0xe4);
    if ((iVar2 < 0) || ((iVar2 < 1 && (*(int *)(iVar4 + 0xe2) == 0)))) goto LAB_1000_9ebd;
    local_3 = 0;
  }
  uVar3 = CONCAT11(extraout_AH,local_3);
LAB_1000_9f40:
  return CONCAT11((char)(uVar3 >> 8),local_3);
}

