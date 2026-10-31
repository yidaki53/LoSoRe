
void __cdecl16near FUN_1000_4905(void)

{
  uint uVar1;
  char cVar2;
  undefined2 uVar3;
  int iVar4;
  undefined2 uVar5;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  undefined1 *puVar6;
  undefined2 uVar7;
  undefined2 uVar8;
  undefined1 local_208 [256];
  byte local_108 [256];
  int local_8;
  int local_6;
  undefined1 uStack_4;
  char local_3;
  
  uStack_4 = 0;
  local_3 = 0x10;
  local_6 = 0x4910;
  FUN_42b5_04df();
  FUN_3de3_0c99(0x48dd,0x42b5);
  FUN_42b5_1766(0xff,local_108,unaff_SS,0,*(undefined2 *)0x4fd,*(undefined2 *)0x4ff);
  while (local_108[0] < 3) {
    puVar6 = local_208;
    uVar3 = unaff_SS;
    FUN_42b5_0bc4(0x48e5,0x42b5);
    FUN_42b5_0c51(local_108,unaff_SS);
    FUN_42b5_0bde(0xff,local_108,unaff_SS,puVar6,uVar3);
  }
  uVar8 = 0x42;
  uVar7 = 8;
  puVar6 = local_208;
  uVar3 = unaff_SS;
  FUN_42b5_0bc4(0x48e7,0x42b5);
  FUN_42b5_0c51(local_108,unaff_SS);
  uVar5 = 0x3de3;
  FUN_3de3_0bea(puVar6,uVar3,uVar7,uVar8);
  local_8 = *(int *)0x4fd;
  local_6 = local_8 + -8;
  if (local_6 < 1) {
    local_6 = 1;
  }
  FUN_1000_40d4(local_8,local_6);
  local_3 = '\0';
  while (local_3 == '\0') {
    FUN_3de3_0b67(3,0x2b);
    FUN_3de3_0d8a();
    uVar3 = FUN_3de3_0339();
    uVar5 = 0x42b5;
    cVar2 = FUN_42b5_1bc4(uVar3);
    if (cVar2 == '\0') {
      uVar5 = 0x3de3;
      FUN_3de3_0339();
    }
    else if (cVar2 == '2') {
      FUN_1000_4328(&local_8,unaff_SS,&local_6,unaff_SS);
    }
    else if (cVar2 == '8') {
      FUN_1000_4611(&local_8,unaff_SS,&local_6,unaff_SS);
    }
    else if (cVar2 == '\r') {
      uVar1 = *(uint *)(local_8 * 0x80 + 0x2694);
      iVar4 = (int)uVar1 >> 0xf;
      if ((iVar4 < *(int *)0x4fb) || ((iVar4 <= *(int *)0x4fb && (uVar1 <= *(uint *)0x4f9)))) {
        *(int *)0x4fd = local_8;
        *(int *)0x4ff = local_8 >> 0xf;
        local_3 = '\x01';
      }
      else {
        uVar5 = 0x3de3;
        FUN_3de3_002d(0x48f2,0x42b5);
      }
    }
    else if (cVar2 == '\x1b') {
      local_3 = '\x01';
    }
  }
  FUN_1000_01cf();
  FUN_3de3_002d(0x48f4,uVar5);
  FUN_3de3_0c99(0x48fd,0x3de3);
  return;
}

