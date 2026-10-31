
void FUN_3de3_0493(undefined2 *param_1)

{
  undefined2 uVar1;
  undefined2 *puVar2;
  undefined2 uVar3;
  
  FUN_42b5_04df();
  *param_1 = 0x7bc;
  uVar3 = (undefined2)((ulong)param_1 >> 0x10);
  puVar2 = (undefined2 *)param_1;
  puVar2[1] = 1;
  puVar2[2] = 1;
  FUN_42b5_0b2f();
  uVar1 = FUN_42b5_0b2f();
  puVar2[3] = uVar1;
  FUN_42b5_0b2f();
  uVar1 = FUN_42b5_0b2f();
  puVar2[4] = uVar1;
  uVar1 = 0x3c;
  FUN_42b5_0b2f();
  puVar2[5] = uVar1;
  return;
}

