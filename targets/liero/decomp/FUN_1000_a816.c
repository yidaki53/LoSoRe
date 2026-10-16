
void FUN_1000_a816(byte param_1)

{
  char cVar1;
  uint uVar2;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  undefined1 *puVar3;
  undefined2 uVar4;
  char local_206 [256];
  undefined1 local_106 [256];
  uint local_6;
  int local_4;
  
  local_4 = 0x1000;
  local_6 = 0xa821;
  FUN_24dd_0530();
  cVar1 = FUN_202c_0843(0xa80c,0x24dd);
  if (cVar1 != '\0') {
    FUN_24dd_3639(0xa80c,0x202c,local_106,unaff_SS);
    FUN_24dd_36b7(0x24dd,local_106);
    FUN_24dd_04f4();
    local_4 = -1;
    do {
      puVar3 = local_106;
      uVar4 = unaff_SS;
      FUN_24dd_3988(0xff,local_206,unaff_SS);
      FUN_24dd_38f0(puVar3,uVar4);
      FUN_24dd_04f4();
      local_4 = local_4 + 1;
    } while (local_206[0] != '\0');
    if (-1 < local_4) {
      FUN_24dd_36b7(0x24dd,local_106);
      FUN_24dd_04f4();
      uVar2 = FUN_24dd_4654(local_4);
      if (uVar2 < 0x8000) {
        local_6 = 0;
        while( true ) {
          puVar3 = local_106;
          uVar4 = unaff_SS;
          FUN_24dd_3988(0x14,(uint)param_1 * 0x15 + 0x66ec,unaff_DS);
          FUN_24dd_38f0(puVar3,uVar4);
          FUN_24dd_04f4();
          if (local_6 == uVar2) break;
          local_6 = local_6 + 1;
        }
      }
    }
    FUN_24dd_3711(local_106,unaff_SS);
    FUN_24dd_04f4();
  }
  return;
}

