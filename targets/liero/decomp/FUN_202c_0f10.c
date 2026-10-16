
void __cdecl16far FUN_202c_0f10(void)

{
  char *pcVar1;
  undefined4 uVar2;
  byte bVar3;
  char cVar4;
  int iVar5;
  int iVar6;
  int iVar7;
  undefined2 uVar8;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  int iVar9;
  undefined1 *puVar10;
  undefined1 local_118 [250];
  uint local_1e;
  int local_1c;
  int local_1a;
  int local_10;
  int local_e;
  int local_c;
  int local_a;
  int local_8;
  int local_6;
  uint local_4;
  
  if (*(char *)0x66a9 == '\0') {
    puVar10 = local_118;
    FUN_24dd_3e95(0x672e,unaff_DS);
    FUN_24dd_3f14(0xf0b,0x24dd);
    cVar4 = FUN_202c_0b0e(&stack0xfffe,puVar10,unaff_SS);
    if (cVar4 != '\0') {
      local_e = 0;
      while( true ) {
        local_10 = 3;
        while( true ) {
          if (*(char *)0x66af != '\0') {
            iVar6 = 0x20;
            bVar3 = FUN_24dd_4161();
            if ((*(byte *)(iVar6 + 0x14e0) & bVar3) != 0) {
              iVar6 = 0x20;
              bVar3 = FUN_24dd_4161();
              if ((*(byte *)(iVar6 + 0x6604) & bVar3) != 0) {
                uVar2 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_10 * 4);
                pcVar1 = (char *)((int)uVar2 + local_e);
                *pcVar1 = *pcVar1 + '\x04';
              }
            }
          }
          uVar2 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_10 * 4);
          bVar3 = *(byte *)((int)uVar2 + local_e);
          if ((0xb < bVar3) && (bVar3 < 0x13)) {
            iVar6 = 0x20;
            bVar3 = FUN_24dd_4161();
            if (((*(byte *)(iVar6 + 0x14a0) & bVar3) != 0) &&
               (uVar2 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_10 * 4),
               pcVar1 = (char *)((int)uVar2 + local_e), *pcVar1 = *pcVar1 + -2,
               uVar2 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_10 * 4),
               *(byte *)((int)uVar2 + local_e) < 0xc)) {
              uVar2 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_10 * 4);
              *(undefined1 *)((int)uVar2 + local_e) = 0xc;
            }
          }
          if (local_10 == 0x15d) break;
          local_10 = local_10 + 1;
        }
        if (local_e == 500) break;
        local_e = local_e + 1;
      }
      return;
    }
  }
  *(undefined1 *)0x66a9 = 1;
  *(undefined1 *)0x672e = 0;
  FUN_24dd_46e9();
  uVar8 = *(undefined2 *)0x6414;
  *(undefined2 *)0x6600 = *(undefined2 *)0x6412;
  *(undefined2 *)0x6602 = uVar8;
  FUN_202c_0bc0(&stack0xfffe);
  local_1a = FUN_24dd_4654(0x32);
  local_1a = local_1a + 5;
  if (0 < local_1a) {
    local_6 = 1;
    while( true ) {
      local_8 = FUN_24dd_4654(0x1f8);
      local_8 = local_8 + -8;
      local_a = FUN_24dd_4654(0x15e);
      local_a = local_a + -8;
      local_e = FUN_24dd_4654(0xb);
      local_e = local_e + -5;
      local_10 = FUN_24dd_4654(5);
      local_10 = local_10 + -2;
      local_1c = FUN_24dd_4654(0xc);
      if (-1 < local_1c) {
        local_c = 0;
        while( true ) {
          local_1e = FUN_24dd_4654(5);
          if (local_1e < 0x8000) {
            local_4 = 0;
            while( true ) {
              iVar6 = local_8 + local_e;
              iVar9 = local_a + local_10;
              uVar8 = (undefined2)((ulong)*(undefined4 *)0x6678 >> 0x10);
              iVar7 = (int)*(undefined4 *)0x6678 + (uint)*(byte *)0x136a * 0x100;
              local_a = iVar9;
              local_8 = iVar6;
              iVar5 = FUN_24dd_4654(*(undefined1 *)0x137e);
              FUN_202c_005a(1,(int)*(undefined4 *)0x6678 + ((uint)*(byte *)0x1374 + iVar5) * 0x100,
                            (int)((ulong)*(undefined4 *)0x6678 >> 0x10),iVar7,uVar8,iVar9,iVar6);
              if (local_4 == local_1e) break;
              local_4 = local_4 + 1;
            }
          }
          local_8 = local_8 - local_4 * local_e;
          local_a = local_a - local_4 * local_10;
          iVar6 = FUN_24dd_4654(7);
          local_8 = local_8 + iVar6 + -3;
          iVar6 = FUN_24dd_4654(0xf);
          local_a = local_a + iVar6 + -7;
          if (local_c == local_1c) break;
          local_c = local_c + 1;
        }
      }
      if (local_6 == local_1a) break;
      local_6 = local_6 + 1;
    }
  }
  local_1a = FUN_24dd_4654(0xf);
  local_1a = local_1a + 5;
  if (0 < local_1a) {
    local_6 = 1;
    while( true ) {
      do {
        local_8 = FUN_24dd_4654(0x1f8);
        local_8 = local_8 + -0x10;
        local_a = FUN_24dd_4654(0x15e);
        local_a = local_a + -0x10;
        iVar6 = FUN_24dd_4654(4);
        if (iVar6 == 0) {
          local_a = FUN_24dd_4654(0x14);
          local_a = 0x15d - local_a;
        }
        cVar4 = FUN_202c_0a74(0x20,local_a,local_8);
      } while (cVar4 == '\0');
      local_c = FUN_24dd_4654(3);
      FUN_202c_032d(0,(int)*(undefined4 *)0x6678 + (uint)*(byte *)(local_c * 4 + 0x4ba) * 0x100,
                    (int)((ulong)*(undefined4 *)0x6678 >> 0x10),local_a,local_8);
      FUN_202c_032d(0,(int)*(undefined4 *)0x6678 + (uint)*(byte *)(local_c * 4 + 0x4bb) * 0x100,
                    (int)((ulong)*(undefined4 *)0x6678 >> 0x10),local_a,local_8 + 0x10);
      FUN_202c_032d(0,(int)*(undefined4 *)0x6678 + (uint)*(byte *)(local_c * 4 + 0x4bc) * 0x100,
                    (int)((ulong)*(undefined4 *)0x6678 >> 0x10),local_a + 0x10,local_8);
      FUN_202c_032d(0,(int)*(undefined4 *)0x6678 + (uint)*(byte *)(local_c * 4 + 0x4bd) * 0x100,
                    (int)((ulong)*(undefined4 *)0x6678 >> 0x10),local_a + 0x10,local_8 + 0x10);
      if (local_6 == local_1a) break;
      local_6 = local_6 + 1;
    }
  }
  local_1a = FUN_24dd_4654(0x19);
  local_1a = local_1a + 5;
  if (0 < local_1a) {
    local_6 = 1;
    while( true ) {
      do {
        local_8 = FUN_24dd_4654(0x1f8);
        local_8 = local_8 + -8;
        local_a = FUN_24dd_4654(0x15e);
        local_a = local_a + -8;
        iVar6 = FUN_24dd_4654(5);
        if (iVar6 == 0) {
          local_a = FUN_24dd_4654(0xd);
          local_a = 0x15d - local_a;
        }
        cVar4 = FUN_202c_0a74(0xf,local_a,local_8);
      } while (cVar4 == '\0');
      local_c = FUN_24dd_4654(6);
      local_c = local_c + 3;
      FUN_202c_032d(0,(int)*(undefined4 *)0x6678 + local_c * 0x100,
                    (int)((ulong)*(undefined4 *)0x6678 >> 0x10),local_a,local_8);
      if (local_6 == local_1a) break;
      local_6 = local_6 + 1;
    }
  }
  local_e = 0;
  while( true ) {
    local_10 = 3;
    while( true ) {
      if (*(char *)0x66af != '\0') {
        iVar6 = 0x20;
        bVar3 = FUN_24dd_4161();
        if ((*(byte *)(iVar6 + 0x14e0) & bVar3) != 0) {
          iVar6 = 0x20;
          bVar3 = FUN_24dd_4161();
          if ((*(byte *)(iVar6 + 0x6604) & bVar3) != 0) {
            uVar2 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_10 * 4);
            pcVar1 = (char *)((int)uVar2 + local_e);
            *pcVar1 = *pcVar1 + '\x04';
          }
        }
      }
      uVar2 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_10 * 4);
      bVar3 = *(byte *)((int)uVar2 + local_e);
      if ((0xb < bVar3) && (bVar3 < 0x13)) {
        iVar6 = 0x20;
        bVar3 = FUN_24dd_4161();
        if (((*(byte *)(iVar6 + 0x14a0) & bVar3) != 0) &&
           (uVar2 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_10 * 4),
           pcVar1 = (char *)((int)uVar2 + local_e), *pcVar1 = *pcVar1 + -2,
           uVar2 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_10 * 4),
           *(byte *)((int)uVar2 + local_e) < 0xc)) {
          uVar2 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_10 * 4);
          *(undefined1 *)((int)uVar2 + local_e) = 0xc;
        }
      }
      if (local_10 == 0x15d) break;
      local_10 = local_10 + 1;
    }
    if (local_e == 500) break;
    local_e = local_e + 1;
  }
  FUN_24dd_46e9();
  return;
}

