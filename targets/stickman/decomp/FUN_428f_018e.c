
void __stdcall16far FUN_428f_018e(void)

{
  int extraout_DX;
  uint uVar1;
  int iVar2;
  byte *pbVar3;
  undefined2 uVar4;
  byte *in_stack_00000010;
  
  uVar4 = (undefined2)((ulong)in_stack_00000010 >> 0x10);
  pbVar3 = (byte *)in_stack_00000010;
  for (uVar1 = (uint)*in_stack_00000010;
      ((uVar1 != 0 && (pbVar3[uVar1] != 0x5c)) && (pbVar3[uVar1] != 0x3a)); uVar1 = uVar1 - 1) {
  }
  FUN_428f_01e0();
  iVar2 = 0;
  while ((iVar2 != extraout_DX && (pbVar3[iVar2 + 1] != 0x2e))) {
    iVar2 = iVar2 + 1;
  }
  FUN_428f_01e0();
  FUN_428f_01e0();
  return;
}

