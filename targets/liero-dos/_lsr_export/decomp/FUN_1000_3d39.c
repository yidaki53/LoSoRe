
void FUN_1000_3d39(int param_1)

{
  uint *puVar1;
  int *piVar2;
  char *pcVar3;
  undefined4 uVar4;
  bool bVar5;
  byte bVar6;
  byte bVar7;
  char cVar8;
  undefined2 uVar9;
  undefined2 uVar10;
  uint uVar11;
  int iVar12;
  int iVar13;
  uint uVar14;
  uint uVar15;
  uint uVar16;
  int iVar17;
  int iVar18;
  uint *puVar19;
  int iVar20;
  undefined2 uVar21;
  undefined2 unaff_DS;
  bool bVar22;
  undefined2 uVar23;
  undefined2 uVar24;
  undefined2 uVar25;
  undefined2 uVar26;
  undefined4 local_1f;
  int local_18;
  uint local_c;
  uint local_a;
  uint local_8;
  uint local_6;
  
  FUN_24dd_0530();
  uVar21 = (undefined2)((ulong)*(undefined4 *)0x6694 >> 0x10);
  puVar19 = (uint *)((int)*(undefined4 *)0x6694 + param_1 * 0x14);
  local_1f = (uint *)CONCAT22(uVar21,puVar19);
  bVar6 = (byte)puVar19[9] & 0x7f;
  bVar22 = false;
  uVar11 = puVar19[4];
  uVar14 = puVar19[5];
  puVar1 = puVar19;
  uVar15 = *puVar1;
  *puVar1 = *puVar1 + uVar11;
  puVar19[1] = puVar19[1] + uVar14 + (uint)CARRY2(uVar15,uVar11);
  uVar11 = puVar19[6];
  uVar14 = puVar19[7];
  puVar1 = puVar19 + 2;
  uVar15 = *puVar1;
  *puVar1 = *puVar1 + uVar11;
  puVar19[3] = puVar19[3] + uVar14 + (uint)CARRY2(uVar15,uVar11);
  bVar5 = false;
  if (*(char *)(bVar6 + 0x5b5) != '\0') {
    iVar17 = puVar19[1] + puVar19[5] + (uint)CARRY2(*local_1f,puVar19[4]);
    local_18 = puVar19[3] + puVar19[7] + (uint)CARRY2(puVar19[2],puVar19[6]);
    if ((0x14 < bVar6) && (bVar6 < 0x17)) {
      local_18 = local_18 + 2;
    }
    iVar18 = 0x20;
    bVar7 = FUN_24dd_4161();
    if ((((*(byte *)(iVar18 + 0x6604) & bVar7) != 0) || (iVar17 < 0)) || (0x1f7 < iVar17)) {
      uVar15 = 0;
      FUN_24dd_3d80();
      iVar17 = FUN_24dd_3dbd();
      puVar19[4] = -iVar17;
      puVar19[5] = (~uVar15 + 1) - (uint)(iVar17 != 0);
      uVar15 = puVar19[7];
      FUN_24dd_3d80();
      uVar11 = FUN_24dd_3dbd();
      puVar19[6] = uVar11;
      puVar19[7] = uVar15;
      bVar5 = true;
    }
    iVar17 = 0x20;
    bVar7 = FUN_24dd_4161();
    if ((((*(byte *)(iVar17 + 0x6604) & bVar7) != 0) || (0x15c < local_18)) || (local_18 < 0)) {
      uVar15 = 0;
      FUN_24dd_3d80();
      iVar17 = FUN_24dd_3dbd();
      puVar19[6] = -iVar17;
      puVar19[7] = (~uVar15 + 1) - (uint)(iVar17 != 0);
      uVar15 = puVar19[5];
      FUN_24dd_3d80();
      uVar11 = FUN_24dd_3dbd();
      puVar19[4] = uVar11;
      puVar19[5] = uVar15;
      bVar5 = true;
    }
  }
  if (((*(char *)(bVar6 + 0x735) == '\x01') && (*(char *)(bVar6 + 0x74d) != '\0')) &&
     (*(uint *)0x6520 % (uint)*(byte *)(bVar6 + 0x74d) == 0)) {
    uVar15 = puVar19[1];
    uVar11 = puVar19[3];
    uVar14 = puVar19[5];
    uVar9 = FUN_24dd_3dbd(uVar11,uVar15);
    uVar16 = puVar19[7];
    uVar10 = FUN_24dd_3dbd(uVar9,uVar14);
    FUN_1000_0be1(uVar10,uVar16,uVar9,uVar14,uVar11,uVar15);
  }
  iVar17 = puVar19[1] + puVar19[5] + (uint)CARRY2(*local_1f,puVar19[4]);
  local_18 = puVar19[3] + puVar19[7] + (uint)CARRY2(puVar19[2],puVar19[6]);
  if ((0x14 < bVar6) && (bVar6 < 0x17)) {
    local_18 = local_18 + 2;
  }
  if (iVar17 < 0) {
    puVar19[1] = 0;
  }
  if (local_18 < 0) {
    puVar19[3] = 0;
  }
  if (0x1f7 < iVar17) {
    puVar19[1] = 0x1f7;
  }
  if (0x15d < local_18) {
    puVar19[3] = 0x15d;
  }
  iVar18 = 0x20;
  uVar9 = 0x24dd;
  bVar7 = FUN_24dd_4161();
  if (((((*(byte *)(iVar18 + 0x6604) & bVar7) == 0) && (-1 < local_18)) && (local_18 < 0x15d)) &&
     ((-1 < iVar17 && (iVar17 < 0x1f8)))) {
    if (((!bVar5) && (*(char *)(bVar6 + 0x765) != '\0')) &&
       (*(uint *)0x6520 % (uint)*(byte *)(bVar6 + 0x77d) == 0)) {
      uVar9 = 0x202c;
      FUN_202c_1b84(0x24dd,puVar19[3],puVar19[1],*(byte *)(bVar6 + 0x765) | (byte)puVar19[9] & 0x80)
      ;
    }
    uVar11 = *(uint *)((uint)bVar6 * 2 + 0x4dc);
    puVar1 = puVar19 + 6;
    uVar15 = *puVar1;
    *puVar1 = *puVar1 + uVar11;
    puVar19[7] = puVar19[7] + ((int)uVar11 >> 0xf) + (uint)CARRY2(uVar15,uVar11);
  }
  else {
    puVar19[4] = 0;
    puVar19[5] = 0;
    puVar19[6] = 0;
    puVar19[7] = 0;
    if (*(char *)(bVar6 + 0x5fd) == '\x01') {
      if ((*(byte *)(bVar6 + 0x675) & 1) == 1) {
        uVar9 = 0x202c;
        FUN_202c_04d5(1,(int)*(undefined4 *)0x667c +
                        ((uint)*(byte *)(bVar6 + 0x645) + (uint)*(byte *)((int)puVar19 + 0x13)) *
                        0x31,(int)((ulong)*(undefined4 *)0x667c >> 0x10),puVar19[3] - 3,
                      puVar19[1] - 3);
        if (*(char *)0x66af != '\0') {
          uVar15 = puVar19[1];
          local_a = puVar19[1] - 8;
          if ((int)local_a <= (int)(uVar15 + 8)) {
            do {
              if ((local_a < 0x8000) && ((int)local_a < 0x1f8)) {
                uVar11 = puVar19[3];
                local_c = puVar19[3] - 8;
                if ((int)local_c <= (int)(uVar11 + 8)) {
                  do {
                    if ((local_c < 0x8000) && ((int)local_c < 0x15e)) {
                      iVar17 = 0x20;
                      bVar7 = FUN_24dd_4161();
                      if ((*(byte *)(iVar17 + 0x14e0) & bVar7) != 0) {
                        iVar17 = 0x20;
                        uVar9 = 0x24dd;
                        bVar7 = FUN_24dd_4161();
                        if ((*(byte *)(iVar17 + 0x6604) & bVar7) != 0) {
                          uVar4 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_c * 4);
                          pcVar3 = (char *)((int)uVar4 + local_a);
                          *pcVar3 = *pcVar3 + '\x04';
                          goto LAB_1000_4214;
                        }
                      }
                      uVar9 = 0x24dd;
                      uVar4 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_c * 4);
                      bVar7 = *(byte *)((int)uVar4 + local_a);
                      if ((0xa3 < bVar7) && (bVar7 < 0xa8)) {
                        iVar17 = 0x20;
                        uVar9 = 0x24dd;
                        bVar7 = FUN_24dd_4161();
                        if ((*(byte *)(iVar17 + 0x6604) & bVar7) != 0) {
                          uVar4 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_c * 4);
                          pcVar3 = (char *)((int)uVar4 + local_a);
                          *pcVar3 = *pcVar3 + -4;
                        }
                      }
                    }
LAB_1000_4214:
                    if (local_c == uVar11 + 8) break;
                    local_c = local_c + 1;
                  } while( true );
                }
              }
              if (local_a == uVar15 + 8) break;
              local_a = local_a + 1;
            } while( true );
          }
        }
      }
      bVar22 = true;
    }
  }
  if ((*(char *)(bVar6 + 0x65d) != '\0') && ((*(uint *)0x6520 & 7) == 0)) {
    if (((0 < (int)puVar19[5]) || ((-1 < (int)puVar19[5] && (puVar19[4] != 0)))) &&
       (*(char *)((int)puVar19 + 0x13) = *(char *)((int)puVar19 + 0x13) + '\x01',
       *(byte *)(bVar6 + 0x65d) < *(byte *)((int)puVar19 + 0x13))) {
      *(undefined1 *)((int)puVar19 + 0x13) = 0;
    }
    if (((int)puVar19[5] < 0) &&
       (*(char *)((int)puVar19 + 0x13) = *(char *)((int)puVar19 + 0x13) + -1,
       *(char *)((int)puVar19 + 0x13) == -1)) {
      *(undefined1 *)((int)puVar19 + 0x13) = *(undefined1 *)(bVar6 + 0x65d);
    }
  }
  if ((0 < *(int *)((uint)bVar6 * 2 + 0x794)) && (puVar19[8] = puVar19[8] - 1, (int)puVar19[8] < 0))
  {
    bVar22 = true;
  }
  if ((!bVar22) && ((*(char *)(bVar6 + 0x5cd) != '\0' || ((0x14 < bVar6 && (bVar6 < 0x17)))))) {
    local_8 = 0;
    while( true ) {
      cVar8 = FUN_1000_0d70(puVar19[3],puVar19[1],*(undefined1 *)(bVar6 + 0x4c5),local_8 & 0xff);
      if (cVar8 != '\0') {
        iVar17 = 0;
        FUN_24dd_3d80();
        uVar11 = FUN_24dd_3dbd();
        uVar9 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
        iVar18 = (int)*(undefined4 *)0x6670 + local_8 * 0xaa;
        puVar1 = (uint *)(iVar18 + 0x30);
        uVar15 = *puVar1;
        *puVar1 = *puVar1 + uVar11;
        piVar2 = (int *)(iVar18 + 0x32);
        *piVar2 = *piVar2 + iVar17 + (uint)CARRY2(uVar15,uVar11);
        iVar17 = 0;
        FUN_24dd_3d80();
        uVar9 = 0x24dd;
        uVar11 = FUN_24dd_3dbd();
        uVar10 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
        iVar18 = (int)*(undefined4 *)0x6670 + local_8 * 0xaa;
        puVar1 = (uint *)(iVar18 + 0x34);
        uVar15 = *puVar1;
        *puVar1 = *puVar1 + uVar11;
        piVar2 = (int *)(iVar18 + 0x36);
        *piVar2 = *piVar2 + iVar17 + (uint)CARRY2(uVar15,uVar11);
        piVar2 = (int *)((int)*(undefined4 *)0x6670 + local_8 * 0xaa + 0x50);
        *piVar2 = *piVar2 - (uint)*(byte *)(bVar6 + 0x5cd);
        if (*(char *)0x66ac == '\x02') {
          if (bVar6 == 0x15) {
            if (((local_8 == 1) && (*(char *)0x651f == '\0')) &&
               (*(char *)((int)*(undefined4 *)0x6670 + 0x13f) == '\0')) {
              *(undefined1 *)(puVar19 + 9) = 0;
              *(undefined1 *)((int)*(undefined4 *)0x6670 + 0x13f) = 1;
            }
          }
          else if (((bVar6 == 0x16) && (local_8 == 0)) &&
                  ((*(char *)0x651f == '\x01' &&
                   (*(char *)((int)*(undefined4 *)0x6670 + 0x95) == '\0')))) {
            *(undefined1 *)(puVar19 + 9) = 0;
            *(undefined1 *)((int)*(undefined4 *)0x6670 + 0x95) = 1;
          }
        }
        else if (*(char *)0x66ac == '\x03') {
          if (bVar6 == 0x15) {
            if ((local_8 == 1) && (*(char *)((int)*(undefined4 *)0x6670 + 0x13f) == '\0')) {
              *(undefined1 *)(puVar19 + 9) = 0;
              *(undefined1 *)((int)*(undefined4 *)0x6670 + 0x13f) = 1;
            }
          }
          else if (((bVar6 == 0x16) && (local_8 == 0)) &&
                  (*(char *)((int)*(undefined4 *)0x6670 + 0x95) == '\0')) {
            *(undefined1 *)(puVar19 + 9) = 0;
            *(undefined1 *)((int)*(undefined4 *)0x6670 + 0x95) = 1;
          }
        }
        if (*(int *)((int)*(undefined4 *)0x6670 + local_8 * 0xaa + 0x50) < 1) {
          if (local_8 == 0) {
            if ((puVar19[9] & 0x80) == 0x80) {
              *(undefined1 *)((int)*(undefined4 *)0x6670 + 0x96) = 0;
            }
            else {
              *(undefined1 *)((int)*(undefined4 *)0x6670 + 0x96) = 1;
            }
          }
          else if (local_8 == 1) {
            if ((puVar19[9] & 0x80) == 0x80) {
              *(undefined1 *)((int)*(undefined4 *)0x6670 + 0x140) = 1;
            }
            else {
              *(undefined1 *)((int)*(undefined4 *)0x6670 + 0x140) = 0;
            }
          }
        }
        if (((*(char *)(bVar6 + 0x5cd) != '\0') && (*(char *)0x4b8 != '\0')) &&
           (0 < *(int *)((int)*(undefined4 *)0x6670 + local_8 * 0xaa + 0x50))) {
          uVar9 = 0x24dd;
          iVar17 = FUN_24dd_4654(3);
          if (iVar17 == 0) {
            uVar9 = 0x235c;
            cVar8 = FUN_235c_0a1e(*(undefined1 *)(local_8 + 0x4b6));
            if (cVar8 == '\0') {
              iVar17 = FUN_24dd_4654(3);
              iVar18 = (iVar17 + 0x13) * 4;
              uVar9 = 0x235c;
              FUN_235c_095c(0,CONCAT11((char)((uint)(iVar17 + 0x13) >> 8),
                                       *(undefined1 *)(local_8 + 0x4b6)),
                            *(undefined2 *)(iVar18 + 0x6734),*(undefined2 *)(iVar18 + 0x6736));
            }
          }
        }
        bVar7 = *(byte *)(bVar6 + 0x643b);
        if (bVar7 != 0) {
          local_6 = 1;
          while( true ) {
            uVar26 = 7;
            uVar25 = 0;
            uVar15 = puVar19[1];
            uVar11 = puVar19[3];
            uVar14 = puVar19[5];
            uVar10 = FUN_24dd_3dbd(uVar11,uVar15,0,7);
            uVar16 = puVar19[7];
            uVar23 = FUN_24dd_3dbd(uVar10,uVar14);
            uVar24 = FUN_24dd_4654(0x80);
            uVar9 = 0x202c;
            FUN_202c_165d(uVar24,uVar23,uVar16,uVar10,uVar14,uVar11,uVar15,uVar25,uVar26);
            if (local_6 == bVar7) break;
            local_6 = local_6 + 1;
          }
        }
        bVar22 = *(char *)(bVar6 + 0x5e5) == '\x01';
        if ((*(char *)(bVar6 + 0x615) == '\x01') && (!bVar22)) {
          *(undefined1 *)(puVar19 + 9) = 0;
          return;
        }
      }
      if (local_8 == 1) break;
      local_8 = local_8 + 1;
    }
  }
  if (bVar22) {
    if (*(char *)(bVar6 + 0x6a5) != '\0') {
      FUN_202c_1b84(uVar9,puVar19[3],puVar19[1],(byte)puVar19[9] & 0x80 | *(byte *)(bVar6 + 0x6a5));
    }
    if (*(char *)(bVar6 + 0x6d5) != '\0') {
      uVar15 = (uint)*(byte *)(bVar6 + 0x6d5);
      iVar17 = puVar19[1] - 7;
      iVar18 = puVar19[3] - 7;
      uVar9 = (undefined2)((ulong)*(undefined4 *)0x6678 >> 0x10);
      iVar20 = (int)*(undefined4 *)0x6678 + (uint)*(byte *)(uVar15 + 0x1369) * 0x100;
      iVar12 = FUN_24dd_4654(*(undefined1 *)(uVar15 + 0x137d));
      iVar12 = (uint)*(byte *)(uVar15 + 0x1373) + iVar12;
      iVar13 = iVar12 * 0x100;
      if (*(char *)(uVar15 + 4999) == '\x01') {
        iVar13 = iVar13 + 1;
      }
      FUN_202c_005a(iVar13,(int)*(undefined4 *)0x6678 + iVar12 * 0x100,
                    (int)((ulong)*(undefined4 *)0x6678 >> 0x10),iVar20,uVar9,iVar18,iVar17);
      if (*(char *)0x66af != '\0') {
        uVar15 = puVar19[1];
        local_a = puVar19[1] - 10;
        if ((int)local_a <= (int)(uVar15 + 10)) {
          do {
            if ((local_a < 0x8000) && ((int)local_a < 0x1f8)) {
              uVar11 = puVar19[3];
              local_c = puVar19[3] - 10;
              if ((int)local_c <= (int)(uVar11 + 10)) {
                do {
                  if ((local_c < 0x8000) && ((int)local_c < 0x15e)) {
                    iVar17 = 0x20;
                    bVar7 = FUN_24dd_4161();
                    if ((*(byte *)(iVar17 + 0x14e0) & bVar7) != 0) {
                      iVar17 = 0x20;
                      bVar7 = FUN_24dd_4161();
                      if ((*(byte *)(iVar17 + 0x6604) & bVar7) != 0) {
                        uVar4 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_c * 4);
                        pcVar3 = (char *)((int)uVar4 + local_a);
                        *pcVar3 = *pcVar3 + '\x04';
                        goto LAB_1000_48b3;
                      }
                    }
                    uVar4 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_c * 4);
                    bVar7 = *(byte *)((int)uVar4 + local_a);
                    if ((0xa3 < bVar7) && (bVar7 < 0xa8)) {
                      iVar17 = 0x20;
                      bVar7 = FUN_24dd_4161();
                      if ((*(byte *)(iVar17 + 0x6604) & bVar7) != 0) {
                        uVar4 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_c * 4);
                        pcVar3 = (char *)((int)uVar4 + local_a);
                        *pcVar3 = *pcVar3 + -4;
                      }
                    }
                  }
LAB_1000_48b3:
                  if (local_c == uVar11 + 10) break;
                  local_c = local_c + 1;
                } while( true );
              }
            }
            if (local_a == uVar15 + 10) break;
            local_a = local_a + 1;
          } while( true );
        }
      }
    }
    if ((*(char *)(bVar6 + 0x6ed) != '\0') && (bVar7 = *(byte *)(bVar6 + 0x6ed), bVar7 != 0)) {
      local_6 = 1;
      while( true ) {
        uVar14 = (uint)((byte)puVar19[9] & 0x80 | *(byte *)(bVar6 + 0x71d));
        iVar17 = FUN_24dd_4654(2);
        iVar17 = (uint)*(byte *)(bVar6 + 0x705) - iVar17;
        uVar15 = puVar19[1];
        uVar11 = puVar19[3];
        uVar25 = 0;
        uVar24 = 0;
        uVar23 = 0;
        uVar10 = 0;
        uVar9 = FUN_24dd_4654(0x80);
        FUN_202c_165d(uVar9,uVar10,uVar23,uVar24,uVar25,uVar11,uVar15,iVar17,uVar14);
        if (local_6 == bVar7) break;
        local_6 = local_6 + 1;
      }
    }
    *(undefined1 *)(puVar19 + 9) = 0;
  }
  return;
}

