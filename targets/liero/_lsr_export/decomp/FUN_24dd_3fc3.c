
void __stdcall16far FUN_24dd_3fc3(int param_1,undefined1 *param_2,undefined1 *param_3)

{
  undefined1 *puVar1;
  undefined1 *puVar2;
  undefined1 *puVar3;
  
  puVar3 = (undefined1 *)param_3;
  puVar2 = (undefined1 *)param_2;
  *param_3 = (char)param_1;
  for (; puVar3 = puVar3 + 1, param_1 != 0; param_1 = param_1 + -1) {
    puVar1 = puVar2;
    puVar2 = puVar2 + 1;
    *puVar3 = *puVar1;
  }
  return;
}

