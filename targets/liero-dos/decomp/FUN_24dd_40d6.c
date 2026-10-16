
void __stdcall16far FUN_24dd_40d6(undefined2 param_1,undefined2 *param_2)

{
  int iVar1;
  undefined2 *puVar2;
  
  puVar2 = (undefined2 *)param_2;
  *param_2 = param_1;
  for (iVar1 = 0xf; puVar2 = puVar2 + 1, iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0;
  }
  return;
}

