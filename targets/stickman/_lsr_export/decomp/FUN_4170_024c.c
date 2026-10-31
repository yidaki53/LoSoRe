
undefined2 __stdcall16far FUN_4170_024c(undefined2 param_1,undefined4 param_2,undefined2 param_3)

{
  undefined2 local_18;
  undefined2 local_16;
  undefined2 local_14;
  undefined2 local_12;
  undefined2 local_a;
  uint local_6;
  undefined2 local_4;
  
  local_4 = 0x4170;
  local_6 = 0x1957;
  FUN_42b5_04df();
  local_18 = CONCAT11(0x3f,(undefined1)local_18);
  local_16 = param_3;
  local_14 = param_1;
  local_12 = (undefined2)param_2;
  local_a = (undefined2)((ulong)param_2 >> 0x10);
  FUN_428f_0000(0x42b5,&local_18);
  if ((local_6 & 1) == 0) {
    local_4 = local_18;
  }
  else {
    local_4 = 0;
  }
  return local_4;
}

