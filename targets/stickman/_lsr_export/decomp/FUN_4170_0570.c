
void __stdcall16far FUN_4170_0570(undefined4 param_1)

{
  undefined2 unaff_SS;
  undefined1 *puVar1;
  undefined2 uVar2;
  undefined1 local_216 [256];
  undefined1 local_116;
  undefined1 local_115;
  undefined1 *local_110;
  undefined1 local_102;
  undefined1 local_101 [251];
  undefined2 uStack_6;
  undefined2 uStack_4;
  
  uStack_4 = 0x4170;
  uStack_6 = 0x1c7b;
  FUN_42b5_04df();
  FUN_42b5_0bde(0xff,&local_102,unaff_SS,(int)param_1,(int)((ulong)param_1 >> 0x10));
  puVar1 = local_216;
  uVar2 = unaff_SS;
  FUN_42b5_0bc4(&local_102,unaff_SS);
  FUN_42b5_0c51(0x56e,0x42b5);
  FUN_42b5_0bde(0xff,&local_102,unaff_SS,puVar1,uVar2);
  local_115 = 0x41;
  local_110 = local_101;
  FUN_428f_0000(0x42b5,&local_116);
  return;
}

