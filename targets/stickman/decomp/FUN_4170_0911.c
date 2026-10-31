
void FUN_4170_0911(int param_1)

{
  undefined2 uVar1;
  undefined2 unaff_SS;
  undefined2 local_1e;
  undefined2 local_1c;
  uint local_c;
  undefined2 uStack_6;
  undefined2 uStack_4;
  
  uStack_4 = 0x4170;
  uStack_6 = 0x201c;
  FUN_42b5_04df();
  do {
    uVar1 = FUN_4170_024c(*(undefined2 *)(param_1 + -0x20c),*(undefined2 *)(param_1 + -0x208),
                          *(undefined2 *)(param_1 + -0x206),*(undefined2 *)(param_1 + -0x210));
    *(undefined2 *)(param_1 + -0x20a) = uVar1;
    FUN_4170_02a4(*(undefined2 *)(param_1 + -0x20a),*(undefined2 *)(param_1 + -0x208),
                  *(undefined2 *)(param_1 + -0x206),*(undefined2 *)(param_1 + -0x20e));
  } while (*(int *)(param_1 + -0x20a) == *(int *)(param_1 + -0x20c));
  local_1e = 0x5700;
  local_1c = *(undefined2 *)(param_1 + -0x210);
  FUN_428f_0000(0x42b5,&local_1e);
  if ((local_c & 1) == 0) {
    local_1e = 0x5701;
    local_1c = *(undefined2 *)(param_1 + -0x20e);
    FUN_428f_0000(0x428f,&local_1e);
  }
  return;
}

