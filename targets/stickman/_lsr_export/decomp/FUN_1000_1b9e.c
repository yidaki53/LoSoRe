
undefined1 FUN_1000_1b9e(int param_1,int param_2)

{
  int iVar1;
  undefined2 unaff_DS;
  bool bVar2;
  undefined1 local_3;
  
  FUN_42b5_04df();
  local_3 = 0;
  iVar1 = param_1 * 0x50 + param_2;
  bVar2 = iVar1 == 0;
  FUN_42b5_0e79(0x1b7e,0x42b5,
                CONCAT11((char)((uint)(param_1 * 0x50) >> 8),*(undefined1 *)(iVar1 + 0x1f6f)));
  if (bVar2) {
    local_3 = FUN_1000_0c8f(param_1,param_2);
  }
  return local_3;
}

