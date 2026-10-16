
void __stdcall16far FUN_235c_08e4(undefined4 *param_1)

{
  undefined2 uVar1;
  undefined2 unaff_DS;
  
  if (*(char *)0x7688 == '\0') {
    FUN_2494_0050(*(undefined2 *)*param_1);
  }
  uVar1 = (undefined2)((ulong)param_1 >> 0x10);
  FUN_24dd_029f(10,*(undefined2 *)param_1,*(undefined2 *)((int)(undefined4 *)param_1 + 2));
  *(undefined2 *)param_1 = 0;
  *(undefined2 *)((int)(undefined4 *)param_1 + 2) = 0;
  return;
}

