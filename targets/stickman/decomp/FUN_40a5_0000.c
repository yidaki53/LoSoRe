
void FUN_40a5_0000(byte param_1)

{
  undefined1 extraout_AH;
  int iVar1;
  undefined2 unaff_DS;
  
  FUN_42b5_04df();
  iVar1 = CONCAT11(extraout_AH,param_1);
  *(byte *)0x15c = param_1;
  if (*(char *)0x15a != '\0') {
    iVar1 = param_1 + 0x80;
    param_1 = (byte)iVar1;
  }
  FUN_410e_0257(CONCAT11((char)((uint)iVar1 >> 8),param_1));
  if (*(char *)0x15b != '\0') {
    FUN_410e_028f();
  }
  return;
}

