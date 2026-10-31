
void FUN_405f_00ad(int param_1)

{
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  undefined2 local_4;
  
  FUN_42b5_04df();
  local_4 = *(int *)0x156 + 1;
  if (0x3fff < local_4) {
    local_4 = *(int *)0x156 + -0x3fff;
  }
  if (local_4 == *(int *)0x158) {
    FUN_410e_02c7(5000);
    FUN_410e_029c(1000);
    FUN_410e_02c7(500);
    FUN_410e_029c(100);
    FUN_410e_02f4();
  }
  else {
    *(undefined1 *)(*(int *)0x156 + -0x54fe) = *(undefined1 *)(param_1 + 6);
    *(int *)0x156 = local_4;
  }
  return;
}

