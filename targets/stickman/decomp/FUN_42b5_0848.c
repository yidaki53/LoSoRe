
void __stdcall16far FUN_42b5_0848(undefined4 param_1)

{
  undefined2 in_BX;
  undefined1 in_ZF;
  
  FUN_42b5_07b6();
  if ((bool)in_ZF) {
    FUN_42b5_07da();
    FUN_42b5_07da();
  }
  *(undefined2 *)((int)param_1 + 8) = in_BX;
  FUN_42b5_0879();
  return;
}

