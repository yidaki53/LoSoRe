
void __cdecl16near FUN_1000_51ea(void)

{
  char cVar1;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  undefined1 *puVar2;
  undefined2 uVar3;
  undefined1 local_102 [252];
  undefined2 uStack_6;
  undefined2 uStack_4;
  
  uStack_4 = 0x1000;
  uStack_6 = 0x51f5;
  FUN_42b5_04df();
  FUN_3de3_0b67(0x17,1);
  puVar2 = local_102;
  uVar3 = unaff_SS;
  FUN_42b5_0bc4(0x518d,0x3de3);
  FUN_42b5_0c51(0xa7d6,unaff_DS);
  FUN_42b5_0c51(0x51a7,0x42b5);
  FUN_3de3_002d(puVar2,uVar3);
  cVar1 = FUN_1000_4f50();
  if (cVar1 == '\0') {
    FUN_3de3_0c2f(*(byte *)0xa7d6 + 0x10);
    puVar2 = local_102;
    FUN_42b5_0bc4(0x51a7,0x3de3);
    FUN_42b5_0c51(0xa7d6,unaff_DS);
    FUN_42b5_0c51(0x51a9,0x42b5);
    FUN_3de3_002d(puVar2,unaff_SS);
    FUN_1000_503c();
    FUN_3de3_0c2f(*(byte *)0xa7d6 + 0x30);
  }
  FUN_3de3_0c2f(*(byte *)0xa7d6 + 0x10);
  FUN_3de3_002d(0x51d9,0x3de3);
  FUN_3de3_0b37();
  return;
}

