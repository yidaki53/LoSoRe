
void FUN_1000_0be1(undefined2 param_1,undefined2 param_2,undefined2 param_3,undefined2 param_4,
                  undefined2 param_5,undefined2 param_6)

{
  char cVar1;
  int iVar2;
  undefined2 uVar3;
  undefined2 unaff_DS;
  undefined2 local_4;
  
  FUN_24dd_0530();
  for (local_4 = 0;
      (*(char *)((int)*(undefined4 *)0x6690 + local_4 * 0x11) != '\0' && (local_4 < 700));
      local_4 = local_4 + 1) {
  }
  cVar1 = FUN_24dd_4654(2);
  *(char *)((int)*(undefined4 *)0x6690 + local_4 * 0x11) = cVar1 + 'P';
  *(undefined2 *)((int)*(undefined4 *)0x6690 + local_4 * 0x11 + 3) = param_6;
  *(undefined2 *)((int)*(undefined4 *)0x6690 + local_4 * 0x11 + 7) = param_5;
  uVar3 = (undefined2)((ulong)*(undefined4 *)0x6690 >> 0x10);
  iVar2 = (int)*(undefined4 *)0x6690 + local_4 * 0x11;
  *(undefined2 *)(iVar2 + 9) = param_3;
  *(undefined2 *)(iVar2 + 0xb) = param_4;
  uVar3 = (undefined2)((ulong)*(undefined4 *)0x6690 >> 0x10);
  iVar2 = (int)*(undefined4 *)0x6690 + local_4 * 0x11;
  *(undefined2 *)(iVar2 + 0xd) = param_1;
  *(undefined2 *)(iVar2 + 0xf) = param_2;
  return;
}

