
void __stdcall16far FUN_410e_032f(undefined4 param_1)

{
  int iVar1;
  undefined2 uVar2;
  
  uVar2 = (undefined2)((ulong)param_1 >> 0x10);
  iVar1 = (int)param_1;
  *(undefined2 *)(iVar1 + 2) = 0xd7b0;
  *(undefined2 *)(iVar1 + 4) = 0x80;
  *(int *)(iVar1 + 0xc) = iVar1 + 0x80;
  *(undefined2 *)(iVar1 + 0xe) = uVar2;
  *(undefined2 *)(iVar1 + 0x10) = 0x35a;
  *(undefined2 *)(iVar1 + 0x12) = 0x410e;
  *(undefined1 *)(iVar1 + 0x30) = 0;
  return;
}

