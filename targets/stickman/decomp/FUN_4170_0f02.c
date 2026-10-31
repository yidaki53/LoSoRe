
void FUN_4170_0f02(undefined2 param_1,undefined2 param_2,undefined4 param_3)

{
  undefined2 uVar1;
  undefined2 uVar2;
  undefined2 unaff_SS;
  undefined1 *puVar3;
  undefined1 local_138 [256];
  char local_38 [18];
  char local_26 [18];
  char local_14 [14];
  undefined2 uStack_6;
  undefined2 uStack_4;
  
  uStack_4 = 0x4170;
  uStack_6 = 0x260d;
  FUN_42b5_04df();
  uVar1 = FUN_42b5_0b2f();
  FUN_42b5_1766(0x10,local_14,unaff_SS,0,uVar1,param_2);
  uVar2 = 0;
  FUN_42b5_0b2f();
  uVar1 = FUN_42b5_0b2f();
  FUN_42b5_1766(0x10,local_26,unaff_SS,0,uVar1,uVar2);
  uVar2 = 0;
  FUN_42b5_0b2f();
  uVar1 = FUN_42b5_0b2f();
  FUN_42b5_1766(0x10,local_38,unaff_SS,0,uVar1,uVar2);
  if (local_14[0] == '\x01') {
    puVar3 = local_138;
    uVar1 = unaff_SS;
    FUN_42b5_0bc4(0xefe,0x42b5);
    FUN_42b5_0c51(local_14,unaff_SS);
    FUN_42b5_0bde(0x10,local_14,unaff_SS,puVar3,uVar1);
  }
  if (local_26[0] == '\x01') {
    puVar3 = local_138;
    uVar1 = unaff_SS;
    FUN_42b5_0bc4(0xefe,0x42b5);
    FUN_42b5_0c51(local_26,unaff_SS);
    FUN_42b5_0bde(0x10,local_26,unaff_SS,puVar3,uVar1);
  }
  if (local_38[0] == '\x01') {
    puVar3 = local_138;
    uVar1 = unaff_SS;
    FUN_42b5_0bc4(0xefe,0x42b5);
    FUN_42b5_0c51(local_38,unaff_SS);
    FUN_42b5_0bde(0x10,local_38,unaff_SS,puVar3,uVar1);
  }
  puVar3 = local_138;
  uVar1 = unaff_SS;
  FUN_42b5_0bc4(local_14,unaff_SS);
  FUN_42b5_0c51(0xf00,0x42b5);
  FUN_42b5_0c51(local_26,unaff_SS);
  FUN_42b5_0c51(0xf00,0x42b5);
  FUN_42b5_0c51(local_38,unaff_SS);
  FUN_42b5_0bde(0xff,(int)param_3,(int)((ulong)param_3 >> 0x10),puVar3,uVar1);
  return;
}

