
void __stdcall16far FUN_40a5_05e4(char param_1)

{
  undefined1 extraout_AH;
  undefined1 extraout_AH_00;
  undefined1 extraout_AH_01;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  undefined1 uVar1;
  undefined1 *puVar2;
  undefined1 *puVar3;
  undefined2 uVar4;
  undefined1 local_202 [256];
  undefined1 local_102 [252];
  undefined2 uStack_6;
  undefined2 uStack_4;
  
  uStack_4 = 0x40a5;
  uStack_6 = 0x103f;
  FUN_42b5_04df();
  if (param_1 == '\x1b') {
    FUN_42b5_0bde(0xff,0x162,unaff_DS,0x5c2,0x42b5);
  }
  else {
    uVar1 = *(char *)0x162 == '\0';
    if ((bool)uVar1) {
      uVar4 = 0xec16;
      FUN_42b5_08b5(0,CONCAT11(extraout_AH,param_1));
      FUN_42b5_086c(uVar4,unaff_DS);
      FUN_42b5_04a9();
    }
    else {
      puVar3 = local_202;
      uVar4 = unaff_SS;
      FUN_42b5_0bc4(0x162,unaff_DS);
      puVar2 = local_102;
      FUN_42b5_0cf4(CONCAT11(extraout_AH_00,param_1));
      FUN_42b5_0c51(puVar2,unaff_SS);
      FUN_42b5_0bde(0xff,0x162,unaff_DS,puVar3,uVar4);
      FUN_42b5_0e79(0x5c4,0x42b5,CONCAT11(extraout_AH_01,param_1));
      if ((bool)uVar1) {
        FUN_40a5_0098();
      }
      else if (0xfa < *(byte *)0x162) {
        *(undefined1 *)0x162 = 0;
      }
    }
  }
  return;
}

