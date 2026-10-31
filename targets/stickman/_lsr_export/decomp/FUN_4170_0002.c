
undefined1 __stdcall16far FUN_4170_0002(undefined4 param_1)

{
  undefined1 uVar1;
  undefined2 unaff_SS;
  undefined1 *puVar2;
  undefined2 uVar3;
  undefined1 local_218 [256];
  undefined2 local_118 [2];
  uint local_114;
  undefined1 *local_112;
  uint local_106;
  undefined1 local_104;
  undefined1 local_103 [253];
  undefined2 uStack_6;
  undefined2 uStack_4;
  
  uStack_4 = 0x4170;
  uStack_6 = 0x170d;
  FUN_42b5_04df();
  FUN_42b5_0bde(0xff,&local_104,unaff_SS,(int)param_1,(int)((ulong)param_1 >> 0x10));
  puVar2 = local_218;
  uVar3 = unaff_SS;
  FUN_42b5_0bc4(&local_104,unaff_SS);
  FUN_42b5_0c51(0,0x42b5);
  FUN_42b5_0bde(0xff,&local_104,unaff_SS,puVar2,uVar3);
  local_118[0] = 0x4300;
  local_112 = local_103;
  FUN_428f_0000(0x42b5,local_118);
  if (((local_114 & 0x18) == 0) && ((local_106 & 1) == 0)) {
    uVar1 = 1;
  }
  else {
    uVar1 = 0;
  }
  return uVar1;
}

