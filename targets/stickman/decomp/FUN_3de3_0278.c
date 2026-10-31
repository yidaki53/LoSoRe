
void __stdcall16far FUN_3de3_0278(undefined4 param_1)

{
  undefined2 uVar1;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  undefined1 *puVar2;
  undefined2 uVar3;
  undefined1 local_202 [256];
  undefined1 local_102 [252];
  undefined2 uStack_6;
  undefined2 uStack_4;
  
  uStack_4 = 0x3de3;
  uStack_6 = 0xe0b3;
  FUN_42b5_04df();
  FUN_42b5_0bde(0xff,local_102,unaff_SS,(int)param_1,(int)((ulong)param_1 >> 0x10));
  puVar2 = local_202;
  uVar3 = unaff_SS;
  FUN_42b5_0bc4(0x252,0x42b5);
  FUN_42b5_0c51(local_102,unaff_SS);
  FUN_42b5_0c51(0x263,0x42b5);
  FUN_42b5_0c51(0x265,0x42b5);
  FUN_3de3_002d(puVar2,uVar3);
  puVar2 = local_202;
  uVar3 = unaff_SS;
  FUN_42b5_0bc4(0x138,unaff_DS);
  uVar1 = 0x42b5;
  FUN_42b5_0c51(0x267,0x42b5);
  FUN_3de3_002d(puVar2,uVar3);
  if (*(int *)0xaaec != 0) {
    uVar1 = 0x405f;
    FUN_405f_03c9();
  }
  puVar2 = local_202;
  uVar3 = unaff_SS;
  FUN_42b5_0bc4(0x25b,uVar1);
  FUN_42b5_0c51(local_102,unaff_SS);
  FUN_3de3_00e2(puVar2,uVar3);
  FUN_42b5_00e9();
  return;
}

