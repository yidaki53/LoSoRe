
void __stdcall16far FUN_42b5_08b5(int param_1,undefined2 param_2,undefined4 param_3)

{
  int iVar1;
  undefined2 in_BX;
  undefined1 in_ZF;
  
  FUN_42b5_07b6();
  if ((bool)in_ZF) {
    iVar1 = param_1 + -1;
    if (iVar1 != 0 && 0 < param_1) {
      do {
        FUN_42b5_07da();
        iVar1 = iVar1 + -1;
      } while (iVar1 != 0);
    }
    FUN_42b5_07da();
  }
  *(undefined2 *)((int)param_3 + 8) = in_BX;
  return;
}

