
void __stdcall16far FUN_202c_093b(byte *param_1)

{
  byte *pbVar1;
  byte *pbVar2;
  uint uVar3;
  byte *pbVar4;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  undefined1 *puVar5;
  undefined2 uVar6;
  undefined1 *puVar7;
  undefined2 uVar8;
  undefined1 local_382 [246];
  undefined1 local_28c [10];
  undefined1 local_282 [256];
  undefined1 local_182 [128];
  byte local_102;
  byte abStack_101 [255];
  
  pbVar4 = (byte *)param_1;
  local_102 = *param_1;
  pbVar2 = abStack_101;
  for (uVar3 = (uint)local_102; pbVar4 = pbVar4 + 1, uVar3 != 0; uVar3 = uVar3 - 1) {
    pbVar1 = pbVar2;
    pbVar2 = pbVar2 + 1;
    *pbVar1 = *pbVar4;
  }
  if (*(char *)0x666e != '\0') {
    *(undefined1 *)0x66ec = 0;
  }
  if (*(char *)0x666f != '\0') {
    *(undefined1 *)0x6701 = 0;
  }
  if (local_102 == 0) {
    FUN_24dd_3eaf(0xff,&local_102,unaff_SS,0x926,0x202c);
    puVar7 = local_282;
    puVar5 = local_28c;
    uVar6 = unaff_SS;
    uVar8 = unaff_SS;
    FUN_24dd_3e95(0x92c,0x24dd);
    FUN_24dd_3639(puVar5,uVar6,puVar7,uVar8);
    FUN_24dd_36bc(0x24dd,local_282);
    FUN_24dd_04f4();
    if (*(char *)0x6664 == '\0') {
      FUN_24dd_3eaf(8,0x6664,unaff_DS,0x926,0x24dd);
    }
    puVar7 = local_282;
    uVar6 = unaff_SS;
    FUN_24dd_39c3(0,0x6664,unaff_DS);
    FUN_24dd_3930(puVar7,uVar6);
    FUN_24dd_04f4();
    FUN_24dd_3711(local_282,unaff_SS);
    FUN_24dd_04f4();
  }
  FUN_24dd_3eaf(8,0x6664,unaff_DS,&local_102,unaff_SS);
  puVar7 = local_182;
  puVar5 = local_382;
  uVar6 = unaff_SS;
  uVar8 = unaff_SS;
  FUN_24dd_3e95(&local_102,unaff_SS);
  FUN_24dd_3f14(0x936,0x24dd);
  FUN_24dd_3b22(puVar5,uVar6,puVar7,uVar8);
  FUN_24dd_3b66(1,local_182,unaff_SS);
  FUN_24dd_04f4();
  FUN_24dd_3c4f(0,0,0x9b,0x669c,unaff_DS,local_182,unaff_SS);
  FUN_24dd_04f4();
  FUN_24dd_3bde(local_182,unaff_SS);
  FUN_24dd_04f4();
  return;
}

