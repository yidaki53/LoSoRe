
void FUN_1000_a9c1(int param_1)

{
  byte bVar1;
  undefined2 uVar2;
  undefined1 extraout_AH;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  undefined1 *puVar3;
  undefined1 *puVar4;
  undefined2 uVar5;
  undefined2 uVar6;
  undefined1 local_305 [256];
  undefined1 local_205 [256];
  byte local_105 [255];
  undefined4 uStack_6;
  
  uStack_6 = 0x1000a9cc;
  FUN_24dd_0530();
  *(undefined1 *)(param_1 + -0x20e) = 1;
  FUN_24ba_00c4();
  FUN_24dd_3eaf(0xff,local_105,unaff_SS,0x6664,unaff_DS);
  do {
    puVar3 = local_205;
    uVar2 = unaff_SS;
    FUN_24dd_3e95(0xa9b4,0x24dd);
    FUN_24dd_3f14(local_105,unaff_SS);
    FUN_24dd_3f14(0xa9bf,0x24dd);
    uVar2 = FUN_202c_0673(puVar3,uVar2);
    uStack_6._0_3_ = CONCAT21(uVar2,(undefined1)uStack_6);
    FUN_1ec2_00a5(8,0x78,(int)*(undefined4 *)0x65d7 + 0x5021,
                  (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),(int)*(undefined4 *)0x6684 + 0x5021,
                  (int)((ulong)*(undefined4 *)0x6684 >> 0x10));
    FUN_1ec2_0d88(0,7,uStack_6._1_2_,(int)*(undefined4 *)0x65d7 + 0x5021,
                  (int)((ulong)*(undefined4 *)0x65d7 >> 0x10));
    uVar6 = 0x23;
    uVar5 = 0x41;
    puVar3 = local_205;
    uVar2 = unaff_SS;
    FUN_24dd_3e95(0xa9b4,0x1ec2);
    FUN_24dd_3f14(local_105,unaff_SS);
    FUN_24dd_3f14(0xa9bf,0x24dd);
    FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x65d7,
                  (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),0x32,puVar3,uVar2,uVar5,uVar6);
    FUN_1ec2_00a5(8,0x78,0x5021,0xa000,(int)*(undefined4 *)0x65d7 + 0x5021,
                  (int)((ulong)*(undefined4 *)0x65d7 >> 0x10));
    uVar2 = FUN_249c_019d();
    bVar1 = FUN_24dd_4919(uVar2);
    uStack_6 = CONCAT13(bVar1,(undefined3)uStack_6);
    if (bVar1 == 8) {
      FUN_24dd_403d(1,local_105[0],local_105,unaff_SS);
    }
    else if ((((bVar1 != 0xd) && (bVar1 != 0x1b)) &&
             (((0x40 < bVar1 && (bVar1 < 0x5b)) ||
              ((((bVar1 == 0x8f || (bVar1 == 0x8e)) || (bVar1 == 0x99)) ||
               ((0x2f < bVar1 && (bVar1 < 0x3a)))))))) && (local_105[0] < 8)) {
      puVar3 = local_305;
      uVar5 = unaff_SS;
      FUN_24dd_3e95(local_105,unaff_SS);
      puVar4 = local_205;
      uVar2 = unaff_SS;
      FUN_24dd_3fb1(CONCAT11(extraout_AH,uStack_6._3_1_));
      FUN_24dd_3f14(puVar4,uVar2);
      FUN_24dd_3eaf(0xff,local_105,unaff_SS,puVar3,uVar5);
    }
  } while ((uStack_6._3_1_ != '\r') && (uStack_6._3_1_ != '\x1b'));
  FUN_24ba_0090();
  *(bool *)(param_1 + -0x10c) = uStack_6._3_1_ != '\x1b';
  FUN_235c_095c(0,0,*(undefined2 *)0x67a4,*(undefined2 *)0x67a6);
  if (*(char *)(param_1 + -0x10c) != '\0') {
    FUN_202c_093b(local_105,unaff_SS);
  }
  return;
}

