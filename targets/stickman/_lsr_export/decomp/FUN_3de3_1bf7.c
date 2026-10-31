
void __cdecl16far FUN_3de3_1bf7(void)

{
  undefined2 uVar1;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  undefined1 *puVar2;
  undefined1 *puVar3;
  undefined2 uVar4;
  undefined1 local_202 [256];
  undefined1 local_102 [252];
  undefined2 uStack_6;
  undefined2 uStack_4;
  
  uStack_4 = 0x3de3;
  uStack_6 = 0xfa32;
  FUN_42b5_04df();
  puVar3 = local_102;
  uVar4 = unaff_SS;
  FUN_42b5_0bc4(0x1b68,0x42b5);
  FUN_42b5_0c51(0x138,unaff_DS);
  FUN_42b5_0c51(0x1b6b,0x42b5);
  uVar1 = 0x42b5;
  FUN_42b5_0c51(0x142,unaff_DS);
  FUN_3de3_002d(puVar3,uVar4);
  if (*(char *)0x137 == '\0') {
    FUN_3de3_002d(0x1b71,0x42b5);
  }
  FUN_3de3_002d(0x1b76,0x42b5);
  FUN_3de3_002d(0x1b84,0x42b5);
  FUN_3de3_002d(0x1bae,0x42b5);
  if (*(int *)0xaaec != 0) {
    uVar1 = 0x405f;
    FUN_405f_03c9();
  }
  puVar3 = local_102;
  uVar4 = unaff_SS;
  FUN_42b5_0bc4(0x1be1,uVar1);
  FUN_42b5_0c51(0xa7d6,unaff_DS);
  FUN_42b5_0c51(0x1bee,0x42b5);
  puVar2 = local_202;
  FUN_42b5_0cf4(*(byte *)0xa8e7 + 0x30);
  FUN_42b5_0c51(puVar2,unaff_SS);
  FUN_3de3_00e2(puVar3,uVar4);
  return;
}

