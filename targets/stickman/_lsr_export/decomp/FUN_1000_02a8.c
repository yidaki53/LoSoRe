
void FUN_1000_02a8(undefined4 param_1,undefined1 param_2,undefined4 param_3,undefined4 param_4,
                  char param_5)

{
  undefined1 extraout_AH;
  undefined1 extraout_AH_00;
  undefined1 extraout_AH_01;
  undefined1 uVar1;
  undefined2 unaff_SS;
  undefined1 *puVar2;
  undefined2 uVar3;
  undefined1 local_456 [256];
  undefined1 local_356 [256];
  int local_256;
  undefined2 local_254;
  undefined1 local_252 [80];
  undefined1 local_202 [256];
  undefined1 local_102 [252];
  undefined2 uStack_6;
  undefined2 uStack_4;
  
  uStack_4 = 0x1000;
  uStack_6 = 0x2b3;
  FUN_42b5_04df();
  FUN_42b5_0bde(0xff,local_102,unaff_SS,(int)param_4,(int)((ulong)param_4 >> 0x10));
  FUN_42b5_0bde(0xff,local_202,unaff_SS,(int)param_3,(int)((ulong)param_3 >> 0x10));
  FUN_42b5_0af8(0x50,local_252,unaff_SS,(int)param_1,(int)((ulong)param_1 >> 0x10));
  puVar2 = local_456;
  uVar3 = unaff_SS;
  FUN_42b5_0bc4(0x29f,0x42b5);
  FUN_42b5_0c51(local_202,unaff_SS);
  FUN_42b5_0c51(0x2a2,0x42b5);
  FUN_3de3_002d(puVar2,uVar3);
  puVar2 = local_456;
  uVar3 = unaff_SS;
  FUN_42b5_0bc4(0x29f,0x3de3);
  FUN_42b5_0c51(local_102,unaff_SS);
  FUN_42b5_0c51(0x2a4,0x42b5);
  FUN_3de3_002d(puVar2,uVar3);
  local_254 = 1;
  uVar1 = extraout_AH;
  do {
    for (; (local_252[local_254 + -1] == param_5 && (local_254 < 0x51)); local_254 = local_254 + 1)
    {
      FUN_3de3_0000(CONCAT11(uVar1,param_2));
      uVar1 = extraout_AH_00;
    }
    uVar1 = 0;
    local_256 = 0;
    for (; (local_252[local_254 + -1] != param_5 && (local_254 < 0x51)); local_254 = local_254 + 1)
    {
      local_256 = local_256 + 1;
    }
    if (0 < local_256) {
      FUN_42b5_1766(0xff,local_356,unaff_SS,0,local_256,local_256 >> 0xf);
      puVar2 = local_456;
      uVar3 = unaff_SS;
      FUN_42b5_0bc4(0x29f,0x42b5);
      FUN_42b5_0c51(local_356,unaff_SS);
      FUN_42b5_0c51(0x2a6,0x42b5);
      FUN_3de3_002d(puVar2,uVar3);
      uVar1 = extraout_AH_01;
    }
  } while (local_254 < 0x51);
  return;
}

