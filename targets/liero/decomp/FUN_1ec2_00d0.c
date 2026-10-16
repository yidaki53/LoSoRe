
void __stdcall16far FUN_1ec2_00d0(undefined2 param_1,int param_2,undefined4 param_3)

{
  uint uVar1;
  int iVar2;
  undefined2 unaff_SS;
  undefined1 *puVar3;
  undefined2 uVar4;
  undefined1 *puVar5;
  undefined2 uVar6;
  undefined1 local_20c [256];
  undefined1 local_10c [256];
  undefined1 local_c [6];
  uint local_6;
  int local_4;
  
  local_6 = FUN_24dd_3dbd();
  uVar1 = 0x3c;
  iVar2 = 0;
  local_4 = param_2;
  FUN_24dd_3dbd();
  local_c[0] = 0;
  if ((local_4 < 0) || ((local_4 < 1 && (local_6 < 10)))) {
    FUN_24dd_3eaf(5,local_c,unaff_SS,0xcc,0x24dd);
  }
  puVar5 = local_20c;
  uVar6 = unaff_SS;
  FUN_24dd_3e95(local_c,unaff_SS);
  puVar3 = local_10c;
  uVar4 = unaff_SS;
  FUN_202c_076d(local_6,local_4);
  FUN_24dd_3f14(puVar3,uVar4);
  FUN_24dd_3f14(0xce,0x24dd);
  FUN_24dd_3eaf(5,local_c,unaff_SS,puVar5,uVar6);
  if ((iVar2 < 0) || ((iVar2 < 1 && (uVar1 < 10)))) {
    puVar5 = local_10c;
    uVar4 = unaff_SS;
    FUN_24dd_3e95(local_c,unaff_SS);
    FUN_24dd_3f14(0xcc,0x24dd);
    FUN_24dd_3eaf(5,local_c,unaff_SS,puVar5,uVar4);
  }
  puVar5 = local_20c;
  uVar6 = unaff_SS;
  FUN_24dd_3e95(local_c,unaff_SS);
  puVar3 = local_10c;
  uVar4 = unaff_SS;
  FUN_202c_076d(uVar1,iVar2);
  FUN_24dd_3f14(puVar3,uVar4);
  FUN_24dd_3eaf(5,local_c,unaff_SS,puVar5,uVar6);
  FUN_24dd_3eaf(0xff,(int)param_3,(int)((ulong)param_3 >> 0x10),local_c,unaff_SS);
  return;
}

