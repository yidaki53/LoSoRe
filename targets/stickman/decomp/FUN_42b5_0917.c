
void __stdcall16far FUN_42b5_0917(int param_1,byte *param_2,undefined4 param_3)

{
  int iVar1;
  uint uVar2;
  undefined2 in_BX;
  undefined1 in_ZF;
  
  FUN_42b5_07b6();
  if ((bool)in_ZF) {
    uVar2 = (uint)*param_2;
    iVar1 = param_1 - uVar2;
    if (iVar1 != 0 && (int)uVar2 <= param_1) {
      do {
        FUN_42b5_07da();
        iVar1 = iVar1 + -1;
      } while (iVar1 != 0);
      uVar2 = (uint)*param_2;
    }
    for (; uVar2 != 0; uVar2 = uVar2 - 1) {
      FUN_42b5_07da();
    }
  }
  *(undefined2 *)((int)param_3 + 8) = in_BX;
  return;
}

