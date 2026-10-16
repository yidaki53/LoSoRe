
void FUN_235c_0aad(byte param_1)

{
  undefined2 uVar1;
  undefined2 unaff_DS;
  
  *(byte *)0x6854 = param_1;
  uVar1 = *(undefined2 *)((uint)param_1 * 4 + 0x6e62);
  *(undefined2 *)0x6e6c = *(undefined2 *)((uint)param_1 * 4 + 0x6e60);
  *(undefined2 *)0x6e6e = uVar1;
  return;
}

