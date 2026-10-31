
void __stdcall16far FUN_3de3_0bea(undefined4 param_1,undefined2 param_2,undefined2 param_3)

{
  undefined2 unaff_SS;
  undefined1 local_102 [252];
  undefined2 uStack_6;
  undefined2 uStack_4;
  
  uStack_4 = 0x3de3;
  uStack_6 = 0xea25;
  FUN_42b5_04df();
  FUN_42b5_0bde(0xff,local_102,unaff_SS,(int)param_1,(int)((ulong)param_1 >> 0x10));
  FUN_3de3_0b67(param_2,param_3);
  FUN_3de3_002d(local_102,unaff_SS);
  return;
}

