
undefined2 __stdcall16far FUN_42b5_17b1(int *param_1,byte *param_2)

{
  undefined2 uVar1;
  uint uVar2;
  int iVar3;
  byte *pbVar4;
  bool bVar5;
  
  bVar5 = false;
  uVar2 = (uint)*param_2;
  pbVar4 = (byte *)param_2;
  while ((pbVar4 = pbVar4 + 1, uVar2 != 0 && (bVar5 = *pbVar4 < 0x20, *pbVar4 == 0x20))) {
    uVar2 = uVar2 - 1;
  }
  uVar1 = FUN_42b5_1387();
  if ((bVar5) || (iVar3 = 0, uVar2 != 0)) {
    iVar3 = (int)pbVar4 - (int)(byte *)param_2;
    uVar1 = 0;
  }
  *param_1 = iVar3;
  return uVar1;
}

