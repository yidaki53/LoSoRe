
void __stdcall16far FUN_42b5_05bf(undefined4 param_1)

{
  int iVar1;
  undefined2 uVar2;
  undefined2 unaff_DS;
  
  uVar2 = (undefined2)((ulong)param_1 >> 0x10);
  iVar1 = (int)param_1;
  if (*(int *)(iVar1 + 2) != -0x284f) {
    if (*(int *)(iVar1 + 2) != -0x284e) {
      *(undefined2 *)0x39c = 0x67;
      return;
    }
    FUN_42b5_05fb();
  }
  FUN_42b5_05fb();
  *(undefined2 *)(iVar1 + 2) = 0xd7b0;
  return;
}

