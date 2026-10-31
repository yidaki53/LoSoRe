
void __stdcall16far
FUN_42b5_09ad(int param_1,undefined2 param_2,undefined2 param_3,undefined4 param_4)

{
  int iVar1;
  int in_CX;
  undefined2 in_BX;
  undefined1 uVar2;
  
  uVar2 = &stack0x0000 == (undefined1 *)0x22;
  FUN_42b5_130d();
  FUN_42b5_07b6();
  if ((bool)uVar2) {
    iVar1 = param_1 - in_CX;
    if (iVar1 != 0 && in_CX <= param_1) {
      do {
        FUN_42b5_07da();
        iVar1 = iVar1 + -1;
      } while (iVar1 != 0);
    }
    do {
      FUN_42b5_07da();
      in_CX = in_CX + -1;
    } while (in_CX != 0);
  }
  *(undefined2 *)((int)param_4 + 8) = in_BX;
  return;
}

