
void __cdecl16near FUN_1000_53c7(void)

{
  int iVar1;
  char cVar2;
  undefined1 extraout_AH;
  uint uVar3;
  undefined2 uVar4;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  undefined1 *puVar5;
  undefined1 local_208 [254];
  uint local_10a;
  int local_106;
  byte local_104 [254];
  undefined2 uStack_6;
  uint local_4;
  
  local_4 = 0x1000;
  uStack_6 = 0x53d2;
  FUN_42b5_04df();
  local_106 = FUN_4170_01b8(CONCAT11(extraout_AH,0x40),0x532d,0x42b5);
  if (local_106 == -1) {
    FUN_3de3_0278(0x533a,0x4170);
  }
  *(undefined2 *)0x26c4 = 0;
  while ((*(int *)0x26c4 < 0x100 && (cVar2 = FUN_4170_03dd(local_106), cVar2 == '\0'))) {
    FUN_4170_04c5(local_104,unaff_SS,local_106);
    while ((local_104[0] != 0 && (local_104[1] < 0x21))) {
      FUN_42b5_0d75(1,1,local_104,unaff_SS);
    }
    while ((local_104[0] != 0 && (local_104[local_104[0]] < 0x21))) {
      local_104[0] = local_104[0] - 1;
    }
    if (local_104[0] != 0) {
      local_10a = (uint)local_104[0];
      uVar3 = 0;
      if (local_10a != 0) {
        local_4 = 1;
        while( true ) {
          if (local_104[local_4] < 0x20) {
            local_104[local_4] = 0x20;
          }
          uVar3 = local_4;
          if (local_4 == local_10a) break;
          local_4 = local_4 + 1;
        }
      }
      *(int *)0x26c4 = *(int *)0x26c4 + 1;
      puVar5 = local_208;
      uVar4 = unaff_SS;
      FUN_4170_0df2(local_104,unaff_SS,CONCAT11((char)(uVar3 >> 8),0x20));
      FUN_42b5_0bde(0xc,*(int *)0x26c4 * 0x80 + 0x2687,unaff_DS,puVar5,uVar4);
      while ((local_104[0] != 0 && (local_104[1] < 0x21))) {
        FUN_42b5_0d75(1,1,local_104,unaff_SS);
      }
      puVar5 = local_208;
      uVar4 = unaff_SS;
      FUN_4170_0df2(local_104,unaff_SS,0x20);
      uVar4 = FUN_1000_529f(puVar5,uVar4);
      *(undefined2 *)(*(int *)0x26c4 * 0x80 + 0x2694) = uVar4;
      uVar4 = FUN_1000_529f(local_104,unaff_SS);
      *(undefined2 *)(*(int *)0x26c4 * 0x80 + 0x2696) = uVar4;
      iVar1 = *(int *)0x26c4;
      if (iVar1 == 1) {
        FUN_42b5_0bde(0x40,*(int *)0x26c4 * 0x80 + 0x2646,unaff_DS,0x5365,0x4170);
      }
      else if (iVar1 == 2) {
        FUN_42b5_0bde(0x40,*(int *)0x26c4 * 0x80 + 0x2646,unaff_DS,0x5378,0x4170);
      }
      else if (iVar1 == 3) {
        FUN_42b5_0bde(0x40,*(int *)0x26c4 * 0x80 + 0x2646,unaff_DS,0x538a,0x4170);
      }
      else if (iVar1 == 4) {
        FUN_42b5_0bde(0x40,*(int *)0x26c4 * 0x80 + 0x2646,unaff_DS,0x539d,0x4170);
      }
      else if (iVar1 == 5) {
        FUN_42b5_0bde(0x40,*(int *)0x26c4 * 0x80 + 0x2646,unaff_DS,0x53a9,0x4170);
      }
      else if (iVar1 == 6) {
        FUN_42b5_0bde(0x40,*(int *)0x26c4 * 0x80 + 0x2646,unaff_DS,0x53b6,0x4170);
      }
      else {
        FUN_42b5_0bde(0x40,*(int *)0x26c4 * 0x80 + 0x2646,unaff_DS,0x53c3,0x4170);
      }
    }
  }
  FUN_4170_049d(local_106);
  return;
}

