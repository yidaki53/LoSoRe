
void FUN_1000_09dd(char param_1)

{
  undefined1 extraout_AH;
  undefined1 extraout_AH_00;
  undefined1 extraout_AH_01;
  undefined1 extraout_AH_02;
  undefined1 extraout_AH_03;
  undefined1 extraout_AH_04;
  undefined1 extraout_AH_05;
  undefined1 extraout_AH_06;
  undefined1 extraout_AH_07;
  undefined1 extraout_AH_08;
  undefined1 extraout_AH_09;
  undefined1 extraout_AH_10;
  undefined1 extraout_AH_11;
  undefined1 extraout_AH_12;
  undefined1 extraout_AH_13;
  undefined1 extraout_AH_14;
  undefined1 extraout_AH_15;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  undefined1 *puVar1;
  undefined2 uVar2;
  undefined1 local_354 [256];
  undefined1 local_254 [80];
  undefined1 local_204 [510];
  undefined2 uStack_6;
  int local_4;
  
  local_4 = 0x1000;
  uStack_6 = 0x9e8;
  FUN_42b5_04df();
  FUN_3de3_002d(0x8bf,0x42b5);
  FUN_3de3_002d(0x8d3,0x3de3);
  puVar1 = local_354;
  uVar2 = unaff_SS;
  FUN_42b5_0bc4(0x923,0x3de3);
  FUN_42b5_0c51(0x5cc,unaff_DS);
  FUN_42b5_0c51(0x92c,0x42b5);
  FUN_42b5_0c51(0x92e,0x42b5);
  FUN_42b5_0c51(0x930,0x42b5);
  FUN_3de3_002d(puVar1,uVar2);
  FUN_3de3_002d(0x935,0x3de3);
  local_4 = 1;
  while( true ) {
    FUN_42b5_1766(0xff,local_204,unaff_SS,0,local_4 + 1,local_4 + 1 >> 0xf);
    FUN_42b5_1a1f(0x50,local_254,unaff_SS,local_4 * 0x50 + 0x1f70,unaff_DS);
    FUN_1000_02a8(local_254,unaff_SS,CONCAT11(extraout_AH,0xcd),0x985,0x42b5,local_204,unaff_SS,
                  CONCAT11(extraout_AH,1));
    FUN_1000_02a8(local_254,unaff_SS,CONCAT11(extraout_AH_00,0xc4),0x985,0x42b5,local_204,unaff_SS,
                  CONCAT11(extraout_AH_00,2));
    FUN_1000_02a8(local_254,unaff_SS,CONCAT11(extraout_AH_01,0xba),0x985,0x42b5,local_204,unaff_SS,
                  CONCAT11(extraout_AH_01,3));
    FUN_1000_02a8(local_254,unaff_SS,CONCAT11(extraout_AH_02,0xb3),0x985,0x42b5,local_204,unaff_SS,
                  CONCAT11(extraout_AH_02,4));
    FUN_1000_02a8(local_254,unaff_SS,CONCAT11(extraout_AH_03,199),0x98d,0x42b5,local_204,unaff_SS,
                  CONCAT11(extraout_AH_03,7));
    FUN_1000_02a8(local_254,unaff_SS,CONCAT11(extraout_AH_04,0xc4),0x98d,0x42b5,local_204,unaff_SS,
                  CONCAT11(extraout_AH_04,8));
    FUN_1000_02a8(local_254,unaff_SS,CONCAT11(extraout_AH_05,0xb6),0x98d,0x42b5,local_204,unaff_SS,
                  CONCAT11(extraout_AH_05,9));
    FUN_1000_02a8(local_254,unaff_SS,CONCAT11(extraout_AH_06,0x5e),0x995,0x42b5,local_204,unaff_SS,
                  CONCAT11(extraout_AH_06,10));
    FUN_1000_02a8(local_254,unaff_SS,CONCAT11(extraout_AH_07,0x2b),0x99d,0x42b5,local_204,unaff_SS,
                  CONCAT11(extraout_AH_07,0xb));
    FUN_1000_02a8(local_254,unaff_SS,CONCAT11(extraout_AH_08,0xef),0x9a5,0x42b5,local_204,unaff_SS,
                  CONCAT11(extraout_AH_08,0xc));
    FUN_1000_02a8(local_254,unaff_SS,CONCAT11(extraout_AH_09,0xea),0x9ad,0x42b5,local_204,unaff_SS,
                  CONCAT11(extraout_AH_09,0xd));
    FUN_1000_02a8(local_254,unaff_SS,CONCAT11(extraout_AH_10,0x9b),0x9a5,0x42b5,local_204,unaff_SS,
                  CONCAT11(extraout_AH_10,0xe));
    FUN_1000_02a8(local_254,unaff_SS,CONCAT11(extraout_AH_11,0xea),0x9a5,0x42b5,local_204,unaff_SS,
                  CONCAT11(extraout_AH_11,0xf));
    FUN_1000_02a8(local_254,unaff_SS,CONCAT11(extraout_AH_12,0xea),0x995,0x42b5,local_204,unaff_SS,
                  CONCAT11(extraout_AH_12,0x10));
    FUN_1000_02a8(local_254,unaff_SS,CONCAT11(extraout_AH_13,0xea),0x9b1,0x42b5,local_204,unaff_SS,
                  CONCAT11(extraout_AH_13,0x11));
    FUN_1000_02a8(local_254,unaff_SS,CONCAT11(extraout_AH_14,0xea),0x9b9,0x42b5,local_204,unaff_SS,
                  CONCAT11(extraout_AH_14,0x12));
    FUN_1000_02a8(local_254,unaff_SS,CONCAT11(extraout_AH_15,0xea),0x9c1,0x42b5,local_204,unaff_SS,
                  CONCAT11(extraout_AH_15,0x13));
    FUN_3de3_002d(0x9c9,0x42b5);
    if (local_4 == 0x14) break;
    local_4 = local_4 + 1;
  }
  if (param_1 != '\0') {
    *(uint *)0x3ae = (uint)*(byte *)0x6cc;
    *(uint *)0x3b0 = (uint)*(byte *)0x6cd;
  }
  FUN_3de3_0bea(0x9ce,0x3de3,*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
  FUN_1000_06a1();
  FUN_1000_0759();
  FUN_1000_07df();
  FUN_1000_0850();
  return;
}

