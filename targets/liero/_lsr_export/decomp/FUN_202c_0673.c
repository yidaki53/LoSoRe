
int __stdcall16far FUN_202c_0673(byte *param_1)

{
  byte *pbVar1;
  uint uVar2;
  byte *pbVar3;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  int local_108;
  uint local_106;
  byte local_104 [258];
  
  pbVar3 = (byte *)param_1;
  local_104[0] = *param_1;
  pbVar1 = local_104;
  for (uVar2 = (uint)local_104[0]; pbVar1 = pbVar1 + 1, pbVar3 = pbVar3 + 1, uVar2 != 0;
      uVar2 = uVar2 - 1) {
    *pbVar1 = *pbVar3;
  }
  local_108 = 1;
  if (local_104[0] != 0) {
    local_106 = 1;
    while( true ) {
      if (local_104[local_106] == 0xff) {
        local_106 = local_106 + 2;
      }
      local_108 = local_108 + (uint)*(byte *)((local_104[local_106] - 2) * 0x40 + 0x19e5);
      if (local_106 == local_104[0]) break;
      local_106 = local_106 + 1;
    }
  }
  return local_108 + 2;
}

