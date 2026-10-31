
void __stdcall16far FUN_3de3_05b6(undefined4 param_1)

{
  undefined1 extraout_AH;
  undefined1 extraout_AH_00;
  undefined1 extraout_AH_01;
  undefined1 extraout_AH_02;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  undefined1 *puVar1;
  undefined2 uVar2;
  undefined2 uVar3;
  undefined2 uVar4;
  undefined1 local_320 [256];
  undefined1 local_220 [6];
  undefined2 local_21a;
  undefined2 local_218;
  int local_216;
  undefined1 local_214 [256];
  byte local_114 [256];
  uint local_14;
  uint local_12;
  uint local_10;
  undefined1 local_e [8];
  undefined2 uStack_6;
  undefined2 uStack_4;
  
  uStack_4 = 0x3de3;
  uStack_6 = 0xe3f1;
  FUN_42b5_04df();
  FUN_42b5_0af8(0xc,local_e,unaff_SS,(int)param_1,(int)((ulong)param_1 >> 0x10));
  FUN_42b5_0af8(0xc,local_220,unaff_SS,0xa8d6,unaff_DS);
  FUN_3de3_053f(local_e,unaff_SS,local_220,unaff_SS);
  if ((*(int *)0x148 < 0) || (local_216 != *(int *)0x148)) {
    local_12 = FUN_410e_023f();
    local_12 = local_12 & 0xff;
    local_14 = FUN_410e_024b();
    local_14 = local_14 & 0xff;
    local_10 = (uint)*(byte *)0xeb08;
    FUN_410e_0180(0x19,0x50,1,1);
    *(undefined1 *)0xeb08 = 0x70;
    FUN_410e_0213(CONCAT11(extraout_AH,0x19),CONCAT11(extraout_AH,0x37));
    uVar3 = 0xec16;
    uVar2 = unaff_DS;
    FUN_42b5_0917(0,0x5a9,0x410e);
    FUN_42b5_086c(uVar3,uVar2);
    FUN_42b5_04a9();
    FUN_410e_0213(CONCAT11(extraout_AH_00,0x19),CONCAT11(extraout_AH_00,0x37));
    FUN_42b5_1766(0xff,local_114,unaff_SS,0,local_21a,0);
    if (local_114[0] < 2) {
      puVar1 = local_320;
      uVar2 = unaff_SS;
      FUN_42b5_0bc4(0x5b2,0x42b5);
      FUN_42b5_0c51(local_114,unaff_SS);
      FUN_42b5_0bde(0xff,local_114,unaff_SS,puVar1,uVar2);
    }
    uVar4 = 0xec16;
    puVar1 = local_320;
    uVar2 = unaff_SS;
    uVar3 = unaff_DS;
    FUN_42b5_0bc4(local_114,unaff_SS);
    FUN_42b5_0c51(0x5b4,0x42b5);
    FUN_42b5_0917(0,puVar1,uVar2);
    FUN_42b5_086c(uVar4,uVar3);
    FUN_42b5_04a9();
    puVar1 = local_320;
    uVar2 = unaff_SS;
    FUN_42b5_0bc4(local_114,unaff_SS);
    FUN_42b5_0c51(0x5b4,0x42b5);
    FUN_42b5_0bde(0xff,local_214,unaff_SS,puVar1,uVar2);
    FUN_42b5_1766(0xff,local_114,unaff_SS,0,local_218,0);
    if (local_114[0] < 2) {
      puVar1 = local_320;
      uVar2 = unaff_SS;
      FUN_42b5_0bc4(0x5b2,0x42b5);
      FUN_42b5_0c51(local_114,unaff_SS);
      FUN_42b5_0bde(0xff,local_114,unaff_SS,puVar1,uVar2);
    }
    uVar4 = 0xec16;
    puVar1 = local_320;
    uVar2 = unaff_SS;
    uVar3 = unaff_DS;
    FUN_42b5_0bc4(local_114,unaff_SS);
    FUN_42b5_0c51(0x5b4,0x42b5);
    FUN_42b5_0917(0,puVar1,uVar2);
    FUN_42b5_086c(uVar4,uVar3);
    FUN_42b5_04a9();
    puVar1 = local_320;
    uVar2 = unaff_SS;
    FUN_42b5_0bc4(local_214,unaff_SS);
    FUN_42b5_0c51(local_114,unaff_SS);
    FUN_42b5_0c51(0x5b4,0x42b5);
    FUN_42b5_0bde(0xff,local_214,unaff_SS,puVar1,uVar2);
    FUN_42b5_1766(0xff,local_114,unaff_SS,0,local_216,0);
    if (local_114[0] < 2) {
      puVar1 = local_320;
      uVar2 = unaff_SS;
      FUN_42b5_0bc4(0x5b2,0x42b5);
      FUN_42b5_0c51(local_114,unaff_SS);
      FUN_42b5_0bde(0xff,local_114,unaff_SS,puVar1,uVar2);
    }
    uVar3 = 0xec16;
    uVar2 = unaff_DS;
    FUN_42b5_0917(0,local_114,unaff_SS);
    FUN_42b5_086c(uVar3,uVar2);
    FUN_42b5_04a9();
    puVar1 = local_320;
    uVar2 = unaff_SS;
    FUN_42b5_0bc4(local_214,unaff_SS);
    FUN_42b5_0c51(local_114,unaff_SS);
    FUN_42b5_0bde(0xff,local_214,unaff_SS,puVar1,uVar2);
    *(undefined1 *)0xeb08 = (undefined1)local_10;
    FUN_410e_0180(CONCAT11(extraout_AH_01,0x17),CONCAT11(extraout_AH_01,0x50),
                  CONCAT11(extraout_AH_01,1),CONCAT11(extraout_AH_01,1));
    FUN_410e_0213(CONCAT11(extraout_AH_02,(undefined1)local_14),
                  CONCAT11(extraout_AH_02,(undefined1)local_12));
    if (*(char *)0x136 != '\0') {
      FUN_3de3_0b67(0x17,0x46);
      FUN_3de3_002d(local_214,unaff_SS);
      FUN_3de3_0b67(local_14,local_12);
    }
    *(int *)0x148 = local_216;
  }
  return;
}

