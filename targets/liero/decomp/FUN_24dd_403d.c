
void __stdcall16far FUN_24dd_403d(int param_1,int param_2,undefined4 param_3)

{
  undefined2 uVar1;
  undefined2 uVar2;
  undefined2 unaff_SS;
  undefined1 *puVar3;
  undefined1 *puVar4;
  undefined2 uVar5;
  undefined1 local_202 [256];
  undefined1 local_102 [256];
  
  if (((0 < param_1) && (0 < param_2)) && (param_2 < 0x100)) {
    if (0xff < param_1) {
      param_1 = 0xff;
    }
    puVar4 = local_102;
    uVar2 = (undefined2)((ulong)param_3 >> 0x10);
    uVar1 = (undefined2)param_3;
    uVar5 = unaff_SS;
    FUN_24dd_3ed3(param_2 + -1,1,uVar1,uVar2);
    puVar3 = local_202;
    FUN_24dd_3ed3(0xff,param_2 + param_1,uVar1,uVar2);
    FUN_24dd_3f14(puVar3,unaff_SS);
    FUN_24dd_3eaf(0xff,uVar1,uVar2,puVar4,uVar5);
  }
  return;
}

