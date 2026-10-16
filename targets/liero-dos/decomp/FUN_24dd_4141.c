
void __stdcall16far FUN_24dd_4141(uint param_1,undefined1 *param_2,undefined4 param_3)

{
  undefined1 *puVar1;
  undefined1 *puVar2;
  undefined1 *puVar3;
  undefined1 *puVar4;
  
  puVar4 = (undefined1 *)param_2;
  puVar3 = (undefined1 *)((int)param_3 + (param_1 >> 8));
  for (param_1 = param_1 & 0xff; param_1 != 0; param_1 = param_1 - 1) {
    puVar2 = puVar4;
    puVar4 = puVar4 + 1;
    puVar1 = puVar3;
    puVar3 = puVar3 + 1;
    *puVar2 = *puVar1;
  }
  return;
}

