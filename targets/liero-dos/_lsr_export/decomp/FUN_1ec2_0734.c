
void __stdcall16far
FUN_1ec2_0734(char param_1,undefined4 param_2,char *param_3,int param_4,int param_5)

{
  char *pcVar1;
  char *pcVar2;
  int iVar3;
  char *pcVar4;
  char *pcVar5;
  undefined2 uVar6;
  undefined2 unaff_SS;
  int local_108;
  int local_104;
  char local_102 [256];
  
  pcVar5 = local_102;
  pcVar4 = (char *)param_3;
  for (iVar3 = 0x100; iVar3 != 0; iVar3 = iVar3 + -1) {
    pcVar2 = pcVar5;
    pcVar5 = pcVar5 + 1;
    pcVar1 = pcVar4;
    pcVar4 = pcVar4 + 1;
    *pcVar2 = *pcVar1;
  }
  uVar6 = (undefined2)((ulong)param_2 >> 0x10);
  if (param_1 == '\0') {
    local_108 = 0;
    while( true ) {
      local_104 = 2;
      while( true ) {
        if (local_102[local_108 * 0x10 + local_104] != '\0') {
          FUN_1ec2_0e4a((int)param_2,uVar6,param_4 + local_108,(0xe - local_104) + param_5);
        }
        if (local_104 == 0xb) break;
        local_104 = local_104 + 1;
      }
      if (local_108 == 8) break;
      local_108 = local_108 + 1;
    }
  }
  else {
    local_108 = 0;
    while( true ) {
      local_104 = 2;
      while( true ) {
        if (local_102[local_108 * 0x10 + local_104] != '\0') {
          FUN_1ec2_0e4a((int)param_2,uVar6,param_4 + local_108,param_5 + local_104);
        }
        if (local_104 == 0xb) break;
        local_104 = local_104 + 1;
      }
      if (local_108 == 8) break;
      local_108 = local_108 + 1;
    }
  }
  return;
}

