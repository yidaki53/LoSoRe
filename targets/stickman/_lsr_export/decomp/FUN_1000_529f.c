
undefined2 FUN_1000_529f(undefined4 param_1)

{
  undefined2 unaff_SS;
  int local_108;
  int local_106;
  byte local_104 [254];
  undefined2 uStack_6;
  undefined2 local_4;
  
  local_4 = 0x1000;
  uStack_6 = 0x52aa;
  FUN_42b5_04df();
  FUN_42b5_0bde(0xff,local_104,unaff_SS,(int)param_1,(int)((ulong)param_1 >> 0x10));
  local_106 = 1;
  while (local_106 <= (int)(uint)local_104[0]) {
    if (local_104[local_106] < 0x21) {
      FUN_42b5_0d75(1,local_106,local_104,unaff_SS);
    }
    else {
      local_106 = local_106 + 1;
    }
  }
  local_4 = FUN_42b5_17b1(&local_108,unaff_SS,local_104,unaff_SS);
  if (local_108 != 0) {
    local_4 = 0;
  }
  return local_4;
}

