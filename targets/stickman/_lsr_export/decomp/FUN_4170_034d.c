
undefined4 __stdcall16far FUN_4170_034d(undefined2 param_1)

{
  uint uVar1;
  int iVar2;
  uint local_1e;
  undefined2 local_1c;
  undefined2 local_1a;
  undefined2 local_18;
  uint local_c;
  undefined2 local_a;
  undefined2 local_8;
  int local_6;
  int local_4;
  
  local_4 = 0x4170;
  local_6 = 0x1a58;
  FUN_42b5_04df();
  local_1e = 0x4201;
  local_1c = param_1;
  local_1a = 0;
  local_18 = 0;
  FUN_428f_0000(0x42b5,&local_1e);
  if ((local_c & 1) == 0) {
    local_a = local_18;
    local_8 = 0;
    iVar2 = 0;
    uVar1 = FUN_42b5_0b14();
    local_6 = local_1e + uVar1;
    local_4 = iVar2 + (uint)CARRY2(local_1e,uVar1);
  }
  else {
    local_6 = -1;
    local_4 = -1;
  }
  return CONCAT22(local_4,local_6);
}

