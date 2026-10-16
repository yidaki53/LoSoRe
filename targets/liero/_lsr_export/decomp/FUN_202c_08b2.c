
void __stdcall16far FUN_202c_08b2(byte *param_1)

{
  byte *pbVar1;
  byte *pbVar2;
  uint uVar3;
  byte *pbVar4;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  undefined1 *puVar5;
  undefined1 local_382 [640];
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
  FUN_24dd_3eaf(8,0x6664,unaff_DS,&local_102,unaff_SS);
  puVar5 = local_382;
  FUN_24dd_3e95(&local_102,unaff_SS);
  FUN_24dd_3f14(0x8ad,0x24dd);
  FUN_202c_079e(0x9b,0,0x669c,unaff_DS,puVar5,unaff_SS);
  *(bool *)0x666e = *(char *)0x66ec == '\0';
  *(bool *)0x666f = *(char *)0x6701 == '\0';
  return;
}

