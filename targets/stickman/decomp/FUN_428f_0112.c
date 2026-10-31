
void __stdcall16far FUN_428f_0112(int *param_1,uint param_2,uint param_3)

{
  int *piVar1;
  undefined2 uVar2;
  
  uVar2 = (undefined2)((ulong)param_1 >> 0x10);
  piVar1 = (int *)param_1;
  *param_1 = (param_3 >> 9) + 0x7bc;
  piVar1[1] = param_3 >> 5 & 0xf;
  piVar1[2] = param_3 & 0x1f;
  piVar1[3] = param_2 >> 0xb;
  piVar1[4] = param_2 >> 5 & 0x3f;
  piVar1[5] = (param_2 & 0x1f) << 1;
  return;
}

