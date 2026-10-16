
void __stdcall16far FUN_235c_04bc(byte *param_1)

{
  byte *pbVar1;
  byte *pbVar2;
  uint uVar3;
  byte *pbVar4;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
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
  *(undefined1 *)0x7690 = 1;
  FUN_24dd_3eaf(0xff,0x7692,unaff_DS,&local_102,unaff_SS);
  return;
}

