
void __cdecl16near FUN_1000_2e9e(void)

{
  int iVar1;
  undefined2 uVar2;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  bool bVar3;
  undefined1 auStack_2ff [53];
  undefined2 uStack_2ca;
  undefined2 uStack_2c8;
  int iStack_2c6;
  undefined1 *puStack_2c4;
  int local_2bc [311];
  undefined1 local_4d;
  undefined2 local_c;
  undefined2 local_a;
  int local_8;
  int local_6;
  int local_4;
  
  local_4 = 0x1000;
  local_6 = 0x2ea9;
  FUN_42b5_04df();
  puStack_2c4 = (undefined1 *)0x42b5;
  iStack_2c6 = 0x2eba;
  local_6 = FUN_4170_01b8();
  if (local_6 == -1) {
    uVar2 = 0x4170;
    puStack_2c4 = (undefined1 *)0x2ecd;
    local_6 = FUN_4170_0123();
    if (local_6 == -1) {
      uVar2 = 0x3de3;
      puStack_2c4 = (undefined1 *)0x2ee0;
      FUN_3de3_0278();
    }
    puStack_2c4 = (undefined1 *)0x200;
    uStack_2c8 = 0x2ef2;
    iStack_2c6 = uVar2;
    FUN_42b5_1a42();
    puStack_2c4 = (undefined1 *)0x2b2;
    iStack_2c6 = 0x42b5;
    uStack_2c8 = 0x2f04;
    FUN_4170_02a4();
  }
  else {
    puStack_2c4 = (undefined1 *)0x2b2;
    iStack_2c6 = 0x4170;
    uStack_2c8 = 0x2f18;
    FUN_4170_024c();
  }
  uVar2 = 0x4170;
  FUN_4170_049d();
  local_8 = 0xb;
  local_4 = 10;
  while( true ) {
    iVar1 = *(int *)((int)local_2bc + local_4 * 0x45);
    if ((iVar1 < *(int *)0x507) ||
       ((iVar1 <= *(int *)0x507 &&
        (*(uint *)((int)local_2bc + local_4 * 0x45 + -2) < *(uint *)0x505)))) {
      local_8 = local_4;
    }
    if (local_4 == 1) break;
    local_4 = local_4 + -1;
  }
  if ((local_8 != 1) && (local_8 != 0xb)) {
    local_2bc[0] = local_8 + -1;
    bVar3 = local_2bc[0] == 1;
    if (0 < local_2bc[0]) {
      local_4 = 1;
      iStack_2c6 = uVar2;
      while( true ) {
        puStack_2c4 = (undefined1 *)0x4b8;
        uVar2 = 0x42b5;
        uStack_2c8 = 0x2f96;
        FUN_42b5_0cc9();
        if (bVar3) {
          local_8 = 0xb;
        }
        if (local_4 == local_2bc[0]) break;
        local_4 = local_4 + 1;
        bVar3 = local_4 == 0;
        iStack_2c6 = uVar2;
      }
    }
  }
  bVar3 = local_8 == 0xb;
  if (local_8 < 0xb) {
    local_4 = 1;
    while( true ) {
      puStack_2c4 = (undefined1 *)0x4b8;
      uStack_2c8 = 0x2fd1;
      iStack_2c6 = uVar2;
      FUN_42b5_0cc9();
      if (bVar3) {
        if (local_4 < 10) {
          puStack_2c4 = auStack_2ff + local_4 * 0x45;
          iStack_2c6 = (10 - local_4) * 0x45;
          uStack_2c8 = 0x42b5;
          uStack_2ca = 0x3009;
          FUN_42b5_1a1f();
        }
        local_4d = 0;
        local_c = 0;
        local_a = 0;
      }
      uVar2 = 0x42b5;
      if (local_4 == 10) break;
      local_4 = local_4 + 1;
      bVar3 = local_4 == 0;
    }
    if (local_8 < 10) {
      puStack_2c4 = auStack_2ff + (local_8 + 1) * 0x45;
      iStack_2c6 = (10 - local_8) * 0x45;
      uStack_2c8 = 0x42b5;
      uStack_2ca = 0x3051;
      FUN_42b5_1a1f();
    }
    puStack_2c4 = auStack_2ff + local_8 * 0x45;
    iStack_2c6 = 0x40;
    uStack_2c8 = 0x42b5;
    uStack_2ca = 0x306d;
    FUN_42b5_0bde();
    uVar2 = *(undefined2 *)0x507;
    iVar1 = local_8 * 0x45;
    *(undefined2 *)((int)local_2bc + iVar1 + -2) = *(undefined2 *)0x505;
    *(undefined2 *)((int)local_2bc + iVar1) = uVar2;
    puStack_2c4 = (undefined1 *)0x42b5;
    uVar2 = 0x4170;
    iStack_2c6 = 0x3092;
    local_6 = FUN_4170_01b8();
    if (local_6 == -1) {
      uVar2 = 0x3de3;
      puStack_2c4 = (undefined1 *)0x30a5;
      FUN_3de3_0278();
    }
    puStack_2c4 = (undefined1 *)0x2b2;
    uStack_2c8 = 0x30b7;
    iStack_2c6 = uVar2;
    FUN_4170_02a4();
    FUN_4170_049d();
  }
  return;
}

