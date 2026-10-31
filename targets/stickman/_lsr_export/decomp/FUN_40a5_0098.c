
void __cdecl16near FUN_40a5_0098(void)

{
  byte bVar1;
  char cVar2;
  undefined1 extraout_AH;
  undefined1 extraout_AH_00;
  undefined2 uVar3;
  undefined1 extraout_AH_01;
  undefined1 uVar8;
  undefined2 uVar4;
  byte bVar9;
  byte extraout_AH_02;
  undefined1 extraout_AH_03;
  uint uVar5;
  uint uVar6;
  int iVar7;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  bool bVar10;
  undefined1 *puVar11;
  undefined1 *puVar12;
  undefined1 local_318 [256];
  undefined1 local_218 [254];
  undefined2 local_11a;
  byte local_118 [8];
  undefined1 local_110 [256];
  int local_10;
  int local_e;
  uint local_c;
  uint local_a;
  uint local_8;
  int local_6;
  undefined1 uStack_4;
  undefined1 local_3;
  
  uStack_4 = 0xa5;
  local_3 = 0x40;
  local_6 = 0xaf3;
  FUN_42b5_04df();
  if (((*(char *)0x163 == '\x1b') && (*(char *)0x164 == '[')) && (2 < *(byte *)0x162)) {
    FUN_42b5_0d75(2,1,0x162,unaff_DS);
    local_e = 0;
    bVar10 = true;
    FUN_42b5_0e79(0x58,0x42b5,*(undefined1 *)(*(byte *)0x162 + 0x162));
    if ((!bVar10) && (*(char *)0x163 == ';')) {
      local_e = 1;
      local_118[0] = 1;
    }
    if (*(char *)0x163 == '=') {
      FUN_42b5_0d75(1,1,0x162,unaff_DS);
    }
    local_6 = 0;
    while (((1 < *(byte *)0x162 && (local_e < 7)) && (local_6 < 10))) {
      if (*(char *)0x163 == ';') {
        FUN_42b5_0d75(1,1,0x162,unaff_DS);
      }
      else {
        local_110[0] = 0;
        while ((bVar10 = *(byte *)0x162 == 1, 1 < *(byte *)0x162 &&
               (FUN_42b5_0e79(0x78,0x42b5,*(undefined1 *)0x163), !bVar10))) {
          puVar12 = local_318;
          uVar4 = unaff_SS;
          FUN_42b5_0bc4(local_110,unaff_SS);
          puVar11 = local_218;
          uVar3 = unaff_SS;
          FUN_42b5_0cf4(CONCAT11(extraout_AH,*(undefined1 *)0x163));
          FUN_42b5_0c51(puVar11,uVar3);
          FUN_42b5_0bde(0xff,local_110,unaff_SS,puVar12,uVar4);
          FUN_42b5_0d75(1,1,0x162,unaff_DS);
        }
        bVar1 = FUN_42b5_17b1(&local_10,unaff_SS,local_110,unaff_SS);
        local_118[local_e] = bVar1;
        if (local_10 == 0) {
          local_e = local_e + 1;
        }
        else {
          local_6 = local_6 + 1;
        }
      }
    }
    cVar2 = *(char *)(*(byte *)0x162 + 0x162);
    if ((cVar2 == 'f') || (cVar2 == 'H')) {
      FUN_410e_0213(1,1);
      uVar8 = extraout_AH_00;
      if (0 < local_e) {
        uVar3 = FUN_410e_023f();
        FUN_410e_0213(local_118[0],uVar3);
        uVar8 = extraout_AH_01;
      }
      if (1 < local_e) {
        uVar3 = CONCAT11(uVar8,local_118[1]);
        uVar4 = FUN_410e_024b(uVar3);
        FUN_410e_0213(uVar4,uVar3);
      }
    }
    else if (cVar2 == 'K') {
      local_8 = FUN_410e_023f();
      local_8 = local_8 & 0xff;
      local_a = FUN_410e_024b();
      local_a = local_a & 0xff;
      do {
        uVar4 = 0xec16;
        uVar3 = unaff_DS;
        FUN_42b5_08b5(0,0x20);
        FUN_42b5_086c(uVar4,uVar3);
        FUN_42b5_04a9();
        cVar2 = FUN_410e_023f();
      } while (cVar2 != '\x01');
      FUN_410e_0213(local_a & 0xff,local_8 & 0xff);
    }
    else if (cVar2 == 'm') {
      if (0 < local_e) {
        local_11a = local_e;
        uVar5 = 0;
        if (0 < local_e) {
          local_c = 1;
          while( true ) {
            bVar1 = local_118[local_c + -1];
            bVar9 = (byte)(uVar5 >> 8);
            if (bVar1 == 0) {
              *(undefined1 *)0x15b = 0;
              *(undefined1 *)0x15a = 0;
              FUN_40a5_0000(CONCAT11(bVar9,7));
              FUN_40a5_003b((uint)extraout_AH_02 << 8);
            }
            else if (bVar1 == 1) {
              *(undefined1 *)0x15b = 1;
              FUN_40a5_0000(CONCAT11(bVar9,*(undefined1 *)0x15c));
            }
            else if (bVar1 == 5) {
              *(undefined1 *)0x15a = 1;
              FUN_40a5_0000(CONCAT11(bVar9,*(undefined1 *)0x15c));
            }
            else if (bVar1 == 7) {
              local_3 = *(undefined1 *)0x15c;
              FUN_40a5_0000(CONCAT11(bVar9,*(undefined1 *)0x15d));
              FUN_40a5_003b(CONCAT11(extraout_AH_03,local_3));
            }
            else if (bVar1 == 0x1e) {
              FUN_40a5_0000((uint)bVar9 << 8);
            }
            else if (bVar1 == 0x1f) {
              FUN_40a5_0000(CONCAT11(bVar9,4));
            }
            else if (bVar1 == 0x20) {
              FUN_40a5_0000(CONCAT11(bVar9,2));
            }
            else if (bVar1 == 0x21) {
              FUN_40a5_0000(CONCAT11(bVar9,6));
            }
            else if (bVar1 == 0x22) {
              FUN_40a5_0000(CONCAT11(bVar9,1));
            }
            else if (bVar1 == 0x23) {
              FUN_40a5_0000(CONCAT11(bVar9,5));
            }
            else if (bVar1 == 0x24) {
              FUN_40a5_0000(CONCAT11(bVar9,3));
            }
            else if (bVar1 == 0x25) {
              FUN_40a5_0000(CONCAT11(bVar9,7));
            }
            else if (bVar1 == 0x28) {
              FUN_40a5_003b((uint)bVar9 << 8);
            }
            else if (bVar1 == 0x29) {
              FUN_40a5_003b(CONCAT11(bVar9,4));
            }
            else if (bVar1 == 0x2a) {
              FUN_40a5_003b(CONCAT11(bVar9,2));
            }
            else if (bVar1 == 0x2b) {
              FUN_40a5_003b(CONCAT11(bVar9,6));
            }
            else if (bVar1 == 0x2c) {
              FUN_40a5_003b(CONCAT11(bVar9,1));
            }
            else if (bVar1 == 0x2d) {
              FUN_40a5_003b(CONCAT11(bVar9,5));
            }
            else if (bVar1 == 0x2e) {
              FUN_40a5_003b(CONCAT11(bVar9,3));
            }
            else if (bVar1 == 0x2f) {
              FUN_40a5_003b(CONCAT11(bVar9,7));
            }
            uVar5 = local_c;
            if (local_c == local_11a) break;
            local_c = local_c + 1;
          }
        }
      }
    }
    else if (cVar2 == 's') {
      uVar5 = FUN_410e_023f();
      *(uint *)0x15e = uVar5 & 0xff;
      uVar5 = FUN_410e_024b();
      *(uint *)0x160 = uVar5 & 0xff;
    }
    else if (cVar2 == 'u') {
      FUN_410e_0213(*(undefined1 *)0x160,*(undefined1 *)0x15e);
    }
    else if (cVar2 == 'A') {
      if (local_e == 0) {
        local_118[0] = 1;
      }
      uVar5 = (uint)local_118[0];
      uVar6 = FUN_410e_024b();
      local_c = (uVar6 & 0xff) - uVar5;
      if ((int)local_c < 1) {
        local_c = 1;
      }
      uVar3 = FUN_410e_023f();
      FUN_410e_0213(local_c & 0xff,uVar3);
    }
    else if (cVar2 == 'B') {
      if (local_e == 0) {
        local_118[0] = 1;
      }
      uVar5 = FUN_410e_024b();
      local_c = (uint)local_118[0] + (uVar5 & 0xff);
      if (*(byte *)0xeb0d + 1 < local_c) {
        local_c = *(byte *)0xeb0d + 1;
      }
      uVar3 = FUN_410e_023f();
      FUN_410e_0213(local_c & 0xff,uVar3);
    }
    else if (cVar2 == 'C') {
      if (local_e == 0) {
        local_118[0] = 1;
      }
      uVar5 = FUN_410e_023f();
      local_c = (uint)local_118[0] + (uVar5 & 0xff);
      uVar5 = *(byte *)0xeb0c + 1;
      if (uVar5 < local_c) {
        uVar5 = *(byte *)0xeb0c + 1;
        local_c = uVar5;
      }
      uVar3 = CONCAT11((char)(uVar5 >> 8),(undefined1)local_c);
      uVar4 = FUN_410e_024b(uVar3);
      FUN_410e_0213(uVar4,uVar3);
    }
    else if (cVar2 == 'D') {
      if (local_e == 0) {
        local_118[0] = 1;
      }
      uVar5 = (uint)local_118[0];
      uVar6 = FUN_410e_023f();
      iVar7 = (uVar6 & 0xff) - uVar5;
      local_c = iVar7;
      if (iVar7 < 1) {
        local_c = 1;
      }
      uVar3 = CONCAT11((char)((uint)iVar7 >> 8),(undefined1)local_c);
      uVar4 = FUN_410e_024b(uVar3);
      FUN_410e_0213(uVar4,uVar3);
    }
    else if (cVar2 == 'J') {
      if ((local_e == 1) && (local_118[0] == 2)) {
        FUN_410e_01c0();
      }
    }
    else if (((cVar2 == 'h') || (cVar2 == 'l')) && (local_e == 1)) {
      if (local_118[0] == 0) {
        FUN_410e_016b(0);
      }
      else if (local_118[0] == 1) {
        FUN_410e_016b(1);
      }
      else if (local_118[0] == 2) {
        FUN_410e_016b(2);
      }
      else if (local_118[0] == 3) {
        FUN_410e_016b(3);
      }
      else if (local_118[0] == 4) {
        FUN_410e_016b(1);
      }
      else if (local_118[0] == 5) {
        FUN_410e_016b(0);
      }
      else if (local_118[0] == 6) {
        FUN_410e_016b(2);
      }
    }
    *(undefined1 *)0x162 = 0;
  }
  else {
    *(undefined1 *)0x162 = 0;
  }
  return;
}

