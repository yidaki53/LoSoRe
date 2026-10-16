
void __stdcall16far FUN_24dd_47d9(int param_1,undefined1 *param_2,int param_3)

{
  undefined1 *puVar1;
  int in_CX;
  undefined1 *puVar2;
  undefined1 *puVar3;
  undefined2 uVar4;
  undefined2 unaff_SS;
  
  FUN_24dd_46f6();
  uVar4 = (undefined2)((ulong)param_2 >> 0x10);
  if (param_1 < param_3) {
    param_3 = param_1;
  }
  if (param_1 < in_CX) {
    in_CX = param_1;
  }
  if (param_3 < in_CX) {
    param_3 = in_CX;
  }
  puVar3 = (undefined1 *)param_2 + 1;
  *param_2 = (char)param_3;
  param_3 = param_3 - in_CX;
  puVar2 = &stack0xfffe;
  if (param_3 != 0) {
    for (; puVar2 = &stack0xfffe, param_3 != 0; param_3 = param_3 + -1) {
      puVar1 = puVar3;
      puVar3 = puVar3 + 1;
      *puVar1 = 0x20;
    }
  }
  for (; in_CX != 0; in_CX = in_CX + -1) {
    puVar1 = puVar3;
    puVar3 = puVar3 + 1;
    *puVar1 = *puVar2;
    puVar2 = puVar2 + 1;
  }
  return;
}

