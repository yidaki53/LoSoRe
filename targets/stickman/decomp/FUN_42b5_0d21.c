
void __stdcall16far
FUN_42b5_0d21(int param_1,undefined2 param_2,undefined4 param_3,undefined4 param_4)

{
  undefined2 uVar1;
  undefined2 uVar2;
  undefined2 unaff_SS;
  undefined1 *puVar3;
  undefined1 *puVar4;
  undefined2 uVar5;
  undefined1 local_202 [256];
  undefined1 local_102 [256];
  
  puVar4 = local_102;
  uVar2 = (undefined2)((ulong)param_3 >> 0x10);
  uVar1 = (undefined2)param_3;
  uVar5 = unaff_SS;
  FUN_42b5_0c10(param_1 + -1,1,uVar1,uVar2);
  FUN_42b5_0c51((int)param_4,(int)((ulong)param_4 >> 0x10));
  puVar3 = local_202;
  FUN_42b5_0c10(0xff,param_1,uVar1,uVar2);
  FUN_42b5_0c51(puVar3,unaff_SS);
  FUN_42b5_0bde(param_2,uVar1,uVar2,puVar4,uVar5);
  return;
}

