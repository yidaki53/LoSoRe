
void __cdecl16near FUN_1000_d7b5(void)

{
  uint uVar1;
  byte bVar3;
  int iVar2;
  undefined2 uVar4;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  bool bVar5;
  undefined1 *puVar6;
  undefined2 uVar7;
  undefined2 uVar8;
  undefined1 local_188 [252];
  int local_8c;
  undefined2 uStack_8a;
  int local_86;
  undefined2 uStack_6;
  int local_4;
  
  local_4 = 0x1000;
  uStack_6 = 0xd7c0;
  FUN_24dd_0530();
  *(undefined1 *)0x651f = 2;
  FUN_1000_05eb(0);
  FUN_1000_05eb(1);
  FUN_202c_0f10();
  FUN_24dd_4905(0,0x1fe,(int)*(undefined4 *)0x6670,(int)((ulong)*(undefined4 *)0x6670 >> 0x10));
  FUN_24dd_4905(0,0x2ef4,(int)*(undefined4 *)0x6688,(int)((ulong)*(undefined4 *)0x6688 >> 0x10));
  FUN_24dd_4905(0,0x2e8d,(int)*(undefined4 *)0x6690,(int)((ulong)*(undefined4 *)0x6690 >> 0x10));
  FUN_24dd_4905(0,0x132b,(int)*(undefined4 *)0x668c,(int)((ulong)*(undefined4 *)0x668c >> 0x10));
  FUN_24dd_4905(0,0x2ef4,(int)*(undefined4 *)0x6694,(int)((ulong)*(undefined4 *)0x6694 >> 0x10));
  FUN_24dd_4905(0,0x56a,(int)*(undefined4 *)0x6698,(int)((ulong)*(undefined4 *)0x6698 >> 0x10));
  local_4 = 0;
  while( true ) {
    uStack_8a = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
    local_8c = (int)*(undefined4 *)0x6670 + local_4 * 0xaa;
    uVar1 = FUN_24dd_4654(100);
    if (uVar1 < 0x33) {
      *(undefined2 *)(local_8c + 0x56) = 0x60;
    }
    else {
      *(undefined2 *)(local_8c + 0x56) = 0x20;
    }
    if (*(int *)(local_8c + 0x56) < 0x21) {
      *(undefined1 *)(local_8c + 0x9b) = 0;
    }
    else {
      *(undefined1 *)(local_8c + 0x9b) = 1;
    }
    *(undefined2 *)(local_8c + 0x50) = *(undefined2 *)(local_4 * 2 + 0x66e8);
    *(undefined1 *)(local_8c + 0x9a) = 0;
    *(undefined2 *)(local_8c + 0x4c) = 0x96;
    *(undefined2 *)(local_4 * 4 + 0x67ba) = 2;
    *(undefined2 *)(local_4 * 2 + 0x67b0) = 0;
    *(undefined2 *)(local_4 * 2 + 0x67b4) = 0;
    *(undefined2 *)(local_8c + 0x4e) = 1;
    for (local_86 = 1; *(undefined1 *)(local_8c + local_86 + 0x6f) = 1, local_86 != 5;
        local_86 = local_86 + 1) {
    }
    FUN_24dd_4905(0,10,local_8c + 0x7f,uStack_8a);
    if (local_4 == 1) break;
    local_4 = local_4 + 1;
  }
  *(undefined1 *)0x651d = 1;
  do {
    local_4 = FUN_1000_cfb7(*(undefined1 *)0x651d);
    bVar3 = (byte)((uint)local_4 >> 8);
    if (1 < (byte)local_4) {
      return;
    }
    if (local_4 == 1) {
      uVar4 = 0x1ec2;
      FUN_1ec2_10cf(*(undefined1 *)0x58b8,*(undefined1 *)0x58b7,*(undefined1 *)0x58b6,0xffa9);
      bVar5 = *(char *)0x66a9 == '\0';
      if (bVar5) {
        FUN_24dd_3f86(0x672e,unaff_DS,0x65f2,unaff_DS);
        if ((!bVar5) || (*(char *)0x66ae != '\0')) {
          uVar8 = 0x7d;
          uVar7 = 0x60;
          puVar6 = local_188;
          uVar4 = unaff_SS;
          FUN_24dd_3e95(0xd7a5,0x24dd);
          FUN_24dd_3f14(0x672e,unaff_DS);
          FUN_1ec2_13e9(0x19a6,unaff_DS,0,0xa000,0xffa9,puVar6,uVar4,uVar7,uVar8);
          FUN_202c_0f10();
        }
      }
      else {
        bVar5 = *(char *)0x66ae == '\0';
        if (bVar5) {
          uVar4 = 0x24dd;
          FUN_24dd_3f86(0x672e,unaff_DS,0x65f2,unaff_DS);
          if (bVar5) goto LAB_1000_d9e2;
        }
        FUN_1ec2_13e9(0x19a6,unaff_DS,0,0xa000,0xffa9,0xd791,uVar4,0x60,0x7d);
        FUN_202c_0f10();
      }
LAB_1000_d9e2:
      FUN_24dd_3eaf(0xc,0x65f2,unaff_DS,0x672e,unaff_DS);
      FUN_24dd_4905(0,0x1fe,(int)*(undefined4 *)0x6670,(int)((ulong)*(undefined4 *)0x6670 >> 0x10));
      FUN_24dd_4905(0,0x2ef4,(int)*(undefined4 *)0x6688,(int)((ulong)*(undefined4 *)0x6688 >> 0x10))
      ;
      FUN_24dd_4905(0,0x2e8d,(int)*(undefined4 *)0x6690,(int)((ulong)*(undefined4 *)0x6690 >> 0x10))
      ;
      FUN_24dd_4905(0,0x132b,(int)*(undefined4 *)0x668c,(int)((ulong)*(undefined4 *)0x668c >> 0x10))
      ;
      FUN_24dd_4905(0,0x2ef4,(int)*(undefined4 *)0x6694,(int)((ulong)*(undefined4 *)0x6694 >> 0x10))
      ;
      FUN_24dd_4905(0,0x56a,(int)*(undefined4 *)0x6698,(int)((ulong)*(undefined4 *)0x6698 >> 0x10));
      local_4 = 1;
      while( true ) {
        iVar2 = *(int *)(local_4 * 2 + 0xdbc) >> 0xf;
        FUN_24dd_3d80();
        uVar4 = FUN_24dd_3dbd();
        *(undefined2 *)(local_4 * 4 + 0x6478) = uVar4;
        *(int *)(local_4 * 4 + 0x647a) = iVar2;
        if (local_4 == 0x28) break;
        local_4 = local_4 + 1;
      }
      local_4 = 0;
      while( true ) {
        uStack_8a = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
        local_8c = (int)*(undefined4 *)0x6670 + local_4 * 0xaa;
        uVar1 = FUN_24dd_4654(100);
        if (uVar1 < 0x33) {
          *(undefined2 *)(local_8c + 0x56) = 0x60;
        }
        else {
          *(undefined2 *)(local_8c + 0x56) = 0x20;
        }
        if (*(int *)(local_8c + 0x56) < 0x21) {
          *(undefined1 *)(local_8c + 0x9b) = 0;
        }
        else {
          *(undefined1 *)(local_8c + 0x9b) = 1;
        }
        *(undefined2 *)(local_8c + 0x50) = *(undefined2 *)(local_4 * 2 + 0x66e8);
        for (local_86 = 1; *(undefined1 *)(local_8c + local_86 + 0x6f) = 1, local_86 != 5;
            local_86 = local_86 + 1) {
        }
        FUN_24dd_4905(0,10,local_8c + 0x7f,uStack_8a);
        *(undefined1 *)(local_8c + 0x9a) = 0;
        *(undefined2 *)(local_8c + 0x4c) = 0x96;
        *(undefined2 *)(local_4 * 4 + 0x67ba) = 0;
        *(undefined2 *)(local_4 * 2 + 0x67b0) = 0;
        bVar3 = 0;
        *(undefined2 *)(local_4 * 2 + 0x67b4) = 0;
        if (local_4 == 1) break;
        local_4 = local_4 + 1;
      }
    }
    iVar2 = (uint)bVar3 * 0x100;
    if (local_4 == 1) {
      iVar2 = iVar2 + 1;
    }
    FUN_1000_9f45(iVar2);
  } while( true );
}

