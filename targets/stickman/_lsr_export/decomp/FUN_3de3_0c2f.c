
void __stdcall16far FUN_3de3_0c2f(int param_1)

{
  undefined2 uVar1;
  undefined2 local_4;
  
  uVar1 = 0x42b5;
  FUN_42b5_04df();
  if (0 < param_1) {
    local_4 = 1;
    while( true ) {
      FUN_3de3_002d(0xc27,uVar1);
      uVar1 = 0x410e;
      FUN_410e_029c(0x32);
      if (local_4 == param_1) break;
      local_4 = local_4 + 1;
    }
  }
  return;
}

