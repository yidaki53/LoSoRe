
/* WARNING: Removing unreachable block (ram,0x00041b32) */

bool __stdcall16far FUN_4170_03dd(undefined2 param_1)

{
  long lVar1;
  long lVar2;
  
  FUN_42b5_04df();
  lVar1 = FUN_4170_034d(param_1);
  FUN_4170_02fc(0,0,2,param_1);
  lVar2 = FUN_4170_034d(param_1);
  FUN_4170_02fc(lVar1,(uint)lVar2 & 0xff00,param_1);
  return lVar2 <= lVar1;
}

