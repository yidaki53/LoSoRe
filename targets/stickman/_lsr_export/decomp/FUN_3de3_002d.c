
void __stdcall16far FUN_3de3_002d(undefined4 param_1)

{
  uint uVar1;
  undefined2 unaff_SS;
  uint local_104;
  byte local_102 [252];
  undefined2 uStack_6;
  undefined2 uStack_4;
  
  uStack_4 = 0x3de3;
  uStack_6 = 0xde68;
  FUN_42b5_04df();
  FUN_42b5_0bde(0xff,local_102,unaff_SS,(int)param_1,(int)((ulong)param_1 >> 0x10));
  if (local_102[0] != 0) {
    if (local_102[0] != 0) {
      local_104 = 1;
      uVar1 = 0;
      while( true ) {
        FUN_3de3_0000(CONCAT11((char)(uVar1 >> 8),local_102[local_104]));
        if (local_104 == local_102[0]) break;
        uVar1 = local_104;
        local_104 = local_104 + 1;
      }
    }
  }
  return;
}

