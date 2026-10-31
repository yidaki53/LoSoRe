
void FUN_1000_0d44(int param_1,undefined4 param_2)

{
  byte bVar1;
  byte bVar2;
  byte bVar3;
  undefined1 extraout_AH;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  bool bVar4;
  undefined1 *puVar5;
  undefined2 uVar6;
  undefined1 local_214 [256];
  undefined4 local_114;
  uint local_110;
  int local_10e;
  int local_106;
  int local_104;
  undefined1 local_102 [252];
  undefined2 uStack_6;
  undefined2 uStack_4;
  
  uStack_4 = 0x1000;
  uStack_6 = 0xd4f;
  FUN_42b5_04df();
  FUN_42b5_0bde(0xff,local_102,unaff_SS,(int)param_2,(int)((ulong)param_2 >> 0x10));
  puVar5 = local_214;
  uVar6 = unaff_SS;
  FUN_4170_0df2(local_102,unaff_SS,CONCAT11(extraout_AH,0x2e));
  FUN_42b5_0bde(0xff,local_102,unaff_SS,puVar5,uVar6);
  local_104 = FUN_42b5_17b1(&local_106,unaff_SS,local_102,unaff_SS);
  if (local_106 != 0) {
    local_104 = -1;
  }
  if (local_104 == 1) {
    local_114 = 0x31cf0000;
  }
  else if (local_104 == 2) {
    local_114 = 0x31cf2034;
  }
  else if (local_104 == 3) {
    local_114 = 0x31cf4068;
  }
  else if (local_104 == 4) {
    local_114 = 0x27be0000;
  }
  else if (local_104 == 5) {
    local_114 = 0x15a00000;
  }
  else if (local_104 == 6) {
    local_114 = 0x1fb10000;
  }
  else {
    FUN_3de3_0278(0xd2f,0x42b5);
  }
  if (1 < param_1) {
    local_114 = CONCAT22((int)((ulong)local_114 >> 0x10),(int)local_114 + (param_1 + -1) * 0x2034);
  }
  FUN_42b5_1a1f(0x2034,0x5cc,unaff_DS,(int)local_114,(int)((ulong)local_114 >> 0x10));
  local_110 = 0;
  local_10e = 0;
  bVar3 = 0xab;
  bVar2 = 0xee;
  while( true ) {
    bVar1 = bVar3;
    bVar3 = bVar2 + bVar1;
    *(byte *)(local_110 + 0x5cc) = *(byte *)(local_110 + 0x5cc) ^ bVar3;
    if ((local_10e == 0) && (local_110 == 0x2033)) break;
    bVar4 = 0xfffe < local_110;
    local_110 = local_110 + 1;
    local_10e = local_10e + (uint)bVar4;
    bVar2 = bVar1;
  }
  return;
}

