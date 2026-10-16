
void FUN_1000_b28f(int param_1)

{
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  undefined1 *puVar1;
  undefined2 uVar2;
  undefined1 local_103 [253];
  undefined2 uStack_6;
  undefined1 uStack_4;
  byte local_3;
  
  uStack_4 = 0;
  local_3 = 0x10;
  uStack_6 = 0xb29a;
  FUN_24dd_0530();
  puVar1 = local_103;
  uVar2 = unaff_SS;
  FUN_202c_076d(*(undefined2 *)((uint)*(byte *)(param_1 + 6) * 2 + 0x66e8),0);
  FUN_24dd_3f14(0xb28d,0x202c);
  FUN_24dd_3eaf(0xc,param_1 + -0xa1,unaff_SS,puVar1,uVar2);
  puVar1 = local_103;
  uVar2 = unaff_SS;
  FUN_202c_076d(*(undefined1 *)((uint)*(byte *)(param_1 + 6) * 3 + 0x66d8),0);
  FUN_24dd_3eaf(0xc,param_1 + -0x94,unaff_SS,puVar1,uVar2);
  puVar1 = local_103;
  uVar2 = unaff_SS;
  FUN_202c_076d(*(undefined1 *)((uint)*(byte *)(param_1 + 6) * 3 + 0x66d9),0);
  FUN_24dd_3eaf(0xc,param_1 + -0x87,unaff_SS,puVar1,uVar2);
  puVar1 = local_103;
  uVar2 = unaff_SS;
  FUN_202c_076d(*(undefined1 *)((uint)*(byte *)(param_1 + 6) * 3 + 0x66da),0);
  FUN_24dd_3eaf(0xc,param_1 + -0x7a,unaff_SS,puVar1,uVar2);
  local_3 = 0;
  while( true ) {
    FUN_24dd_3eaf(0xc,param_1 + (local_3 + 5) * 0xd + -0xae,unaff_SS,
                  (uint)*(byte *)((uint)*(byte *)(param_1 + 6) * 7 + (uint)local_3 + 0x6720) * 0xd +
                  0x5b19,unaff_DS);
    if (local_3 == 6) break;
    local_3 = local_3 + 1;
  }
  FUN_24dd_3eaf(0xc,param_1 + -0x12,unaff_SS,*(char *)(*(byte *)(param_1 + 6) + 0x66a7) * 6 + 900,
                unaff_DS);
  return;
}

