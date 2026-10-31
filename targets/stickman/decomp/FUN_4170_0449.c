
undefined4 __stdcall16far FUN_4170_0449(undefined2 param_1)

{
  undefined4 uVar1;
  undefined4 uVar2;
  
  FUN_42b5_04df();
  uVar1 = FUN_4170_034d(param_1);
  FUN_4170_02fc(0,0,2,param_1);
  uVar2 = FUN_4170_034d(param_1);
  FUN_4170_02fc(uVar1,(uint)uVar2 & 0xff00,param_1);
  return uVar2;
}

