
void __stdcall16far FUN_3de3_0b67(int param_1,int param_2)

{
  undefined2 unaff_SS;
  undefined1 *puVar1;
  undefined2 uVar2;
  undefined1 local_302 [256];
  undefined1 local_202 [256];
  undefined1 local_102 [252];
  undefined2 uStack_6;
  undefined2 uStack_4;
  
  uStack_4 = 0x3de3;
  uStack_6 = 0xe9a2;
  FUN_42b5_04df();
  FUN_42b5_1766(0xff,local_102,unaff_SS,0,param_2,param_2 >> 0xf);
  FUN_42b5_1766(0xff,local_202,unaff_SS,0,param_1,param_1 >> 0xf);
  puVar1 = local_302;
  uVar2 = unaff_SS;
  FUN_42b5_0bc4(0xb60,0x42b5);
  FUN_42b5_0c51(local_202,unaff_SS);
  FUN_42b5_0c51(0xb63,0x42b5);
  FUN_42b5_0c51(local_102,unaff_SS);
  FUN_42b5_0c51(0xb65,0x42b5);
  FUN_3de3_002d(puVar1,uVar2);
  return;
}

