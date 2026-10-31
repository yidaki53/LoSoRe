
void FUN_1000_3b3e(int param_1,undefined4 param_2)

{
  undefined2 unaff_SS;
  undefined1 local_102;
  undefined1 local_101 [251];
  undefined2 uStack_6;
  undefined2 uStack_4;
  
  uStack_4 = 0x1000;
  uStack_6 = 0x3b49;
  FUN_42b5_04df();
  FUN_42b5_0bde(0xff,&local_102,unaff_SS,(int)param_2,(int)((ulong)param_2 >> 0x10));
  if (*(int *)(param_1 + -6) != -1) {
    FUN_4170_02a4(local_102,local_101,unaff_SS,*(undefined2 *)(param_1 + -6));
  }
  return;
}

