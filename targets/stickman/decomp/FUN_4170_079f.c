
undefined4 __stdcall16far FUN_4170_079f(undefined4 param_1)

{
  undefined2 unaff_SS;
  undefined4 uVar1;
  undefined1 *puVar2;
  undefined2 uVar3;
  undefined1 local_20c [260];
  int local_108;
  undefined1 local_106 [256];
  undefined2 local_6;
  undefined2 local_4;
  
  local_4 = 0x4170;
  local_6 = 0x1eaa;
  FUN_42b5_04df();
  FUN_42b5_0bde(0xff,local_106,unaff_SS,(int)param_1,(int)((ulong)param_1 >> 0x10));
  puVar2 = local_20c;
  uVar3 = unaff_SS;
  FUN_4170_05ea(local_106,unaff_SS);
  uVar1 = FUN_42b5_17b1(&local_108,unaff_SS,puVar2,uVar3);
  if (local_108 != 0) {
    uVar1 = 0x7fffffff;
  }
  return uVar1;
}

