
/* WARNING: Removing unreachable block (ram,0x00022b64) */
/* WARNING: Removing unreachable block (ram,0x00022b86) */
/* WARNING: Removing unreachable block (ram,0x00022c69) */

void FUN_202c_1b84(undefined2 param_1,int param_2,int param_3,byte param_4)

{
  uint *puVar1;
  int *piVar2;
  char *pcVar3;
  undefined4 uVar4;
  byte bVar5;
  char cVar6;
  byte bVar7;
  byte bVar8;
  int iVar9;
  undefined1 uVar16;
  uint uVar10;
  uint uVar11;
  int iVar12;
  int iVar13;
  int iVar14;
  uint uVar15;
  uint uVar17;
  uint uVar18;
  uint uVar19;
  uint uVar20;
  int *piVar21;
  int iVar22;
  int iVar23;
  undefined2 uVar24;
  undefined2 uVar25;
  undefined2 unaff_DS;
  bool bVar26;
  undefined2 uVar27;
  undefined2 uVar28;
  undefined2 uVar29;
  undefined2 uVar30;
  undefined2 uVar31;
  undefined2 uVar32;
  undefined2 uVar33;
  undefined2 uVar34;
  uint uStack_28;
  uint local_20;
  uint local_1e;
  uint local_1c;
  uint local_1a;
  uint local_18;
  int local_16;
  uint local_10;
  uint local_e;
  uint local_8;
  uint local_6;
  uint local_4;
  
  uVar25 = 0x202c;
  for (local_4 = 0;
      (*(char *)((int)*(undefined4 *)0x668c + local_4 * 7 + 4) != '\0' && ((int)local_4 < 700));
      local_4 = local_4 + 1) {
  }
  bVar5 = param_4 & 0x7f;
  if ((*(char *)0x4b8 != '\0') && (*(char *)(bVar5 + 0x1391) != '\0')) {
    iVar9 = FUN_24dd_4654(*(undefined1 *)(bVar5 + 0x139f));
    iVar9 = ((uint)*(byte *)(bVar5 + 0x1391) + iVar9) * 4;
    uVar25 = 0x235c;
    FUN_235c_095c(0,*(undefined1 *)(bVar5 + 0x1391),*(undefined2 *)(iVar9 + 0x6734),
                  *(undefined2 *)(iVar9 + 0x6736));
  }
  if ((((*(int *)0x67b0 < param_3) && (param_3 < *(int *)0x67b0 + 0x9e)) &&
      (*(int *)0x67b4 < param_2)) &&
     ((param_2 < *(int *)0x67b4 + 0x9e && (*(int *)0x67ba < (int)(uint)*(byte *)(bVar5 + 0x1435)))))
  {
    *(uint *)0x67ba = (uint)*(byte *)(bVar5 + 0x1435);
  }
  if (((*(int *)0x67b2 < param_3) && (param_3 < *(int *)0x67b2 + 0x9e)) &&
     ((*(int *)0x67b6 < param_2 &&
      ((param_2 < *(int *)0x67b6 + 0x9e && (*(int *)0x67be < (int)(uint)*(byte *)(bVar5 + 0x1435))))
      ))) {
    *(uint *)0x67be = (uint)*(byte *)(bVar5 + 0x1435);
  }
  *(byte *)((int)*(undefined4 *)0x668c + local_4 * 7 + 4) = param_4;
  *(int *)((int)*(undefined4 *)0x668c + local_4 * 7) = param_3 + -8;
  *(int *)((int)*(undefined4 *)0x668c + local_4 * 7 + 2) = param_2 + -8;
  *(undefined1 *)((int)*(undefined4 *)0x668c + local_4 * 7 + 5) = 0;
  *(undefined1 *)((int)*(undefined4 *)0x668c + local_4 * 7 + 6) = *(undefined1 *)(bVar5 + 0x13ad);
  if ((*(char *)(bVar5 + 0x1443) != '\0') && (*(byte *)0x67c0 < *(byte *)(bVar5 + 0x1443))) {
    *(undefined1 *)0x67c0 = *(undefined1 *)(bVar5 + 0x1443);
  }
  if (*(char *)(bVar5 + 0x13e5) != '\0') {
    uVar25 = (undefined2)((ulong)*(undefined4 *)0x668c >> 0x10);
    piVar21 = (int *)((int)*(undefined4 *)0x668c + local_4 * 7);
    local_1c = *piVar21 + 8;
    local_1a = (int)local_1c >> 0xf;
    local_20 = piVar21[1] + 8;
    local_1e = (int)local_20 >> 0xf;
    uVar11 = (uint)*(byte *)(bVar5 + 0x13d7);
    if (*(char *)((int)*(undefined4 *)0x6670 + 0x9a) != '\0') {
      iVar9 = local_1a + CARRY2(local_1c,uVar11);
      uVar19 = *(uint *)((int)*(undefined4 *)0x6670 + 6);
      iVar12 = (int)uVar19 >> 0xf;
      if ((iVar12 < iVar9) || ((iVar12 <= iVar9 && (uVar19 < local_1c + uVar11)))) {
        iVar9 = local_1a - (local_1c < uVar11);
        uVar19 = *(uint *)((int)*(undefined4 *)0x6670 + 6);
        iVar12 = (int)uVar19 >> 0xf;
        if ((iVar9 < iVar12) || ((iVar9 <= iVar12 && (local_1c - uVar11 < uVar19)))) {
          iVar9 = local_1e + CARRY2(local_20,uVar11);
          uVar19 = *(uint *)((int)*(undefined4 *)0x6670 + 10);
          iVar12 = (int)uVar19 >> 0xf;
          if ((iVar12 < iVar9) || ((iVar12 <= iVar9 && (uVar19 < local_20 + uVar11)))) {
            iVar9 = local_1e - (local_20 < uVar11);
            uVar19 = *(uint *)((int)*(undefined4 *)0x6670 + 10);
            iVar12 = (int)uVar19 >> 0xf;
            if ((iVar9 < iVar12) || ((iVar9 <= iVar12 && (local_20 - uVar11 < uVar19)))) {
              uVar19 = *(uint *)((int)*(undefined4 *)0x6670 + 6);
              iVar9 = (((int)uVar19 >> 0xf) - local_1a) - (uint)(uVar19 < local_1c);
              uVar24 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
              iVar12 = (int)*(undefined4 *)0x6670;
              uVar15 = *(uint *)(iVar12 + 0x32);
              if ((int)uVar15 < 0) {
                uVar15 = (~uVar15 + 1) - (uint)(*(int *)(iVar12 + 0x30) != 0);
              }
              if ((int)uVar15 < 2) {
                if ((0 < iVar9) || ((-1 < iVar9 && (uVar19 != local_1c)))) {
                  iVar12 = *(int *)((uint)bVar5 * 4 + 0x13f2);
                  uVar15 = FUN_24dd_3d80();
                  uVar24 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
                  iVar13 = (int)*(undefined4 *)0x6670;
                  puVar1 = (uint *)(iVar13 + 0x30);
                  uVar19 = *puVar1;
                  *puVar1 = *puVar1 + uVar15;
                  piVar2 = (int *)(iVar13 + 0x32);
                  *piVar2 = *piVar2 + iVar12 + (uint)CARRY2(uVar19,uVar15);
                }
                if (iVar9 < 0) {
                  iVar9 = *(int *)((uint)bVar5 * 4 + 0x13f2);
                  uVar15 = FUN_24dd_3d80();
                  uVar24 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
                  iVar12 = (int)*(undefined4 *)0x6670;
                  puVar1 = (uint *)(iVar12 + 0x30);
                  uVar19 = *puVar1;
                  *puVar1 = *puVar1 - uVar15;
                  piVar2 = (int *)(iVar12 + 0x32);
                  *piVar2 = (*piVar2 - iVar9) - (uint)(uVar19 < uVar15);
                }
              }
              uVar19 = *(uint *)((int)*(undefined4 *)0x6670 + 10);
              iVar9 = (((int)uVar19 >> 0xf) - local_1e) - (uint)(uVar19 < local_20);
              uVar24 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
              iVar12 = (int)*(undefined4 *)0x6670;
              uVar15 = *(uint *)(iVar12 + 0x36);
              if ((int)uVar15 < 0) {
                uVar15 = (~uVar15 + 1) - (uint)(*(int *)(iVar12 + 0x34) != 0);
              }
              if ((int)uVar15 < 2) {
                if ((0 < iVar9) || ((-1 < iVar9 && (uVar19 != local_20)))) {
                  iVar12 = *(int *)((uint)bVar5 * 4 + 0x13f2);
                  uVar15 = FUN_24dd_3d80();
                  uVar24 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
                  iVar13 = (int)*(undefined4 *)0x6670;
                  puVar1 = (uint *)(iVar13 + 0x34);
                  uVar19 = *puVar1;
                  *puVar1 = *puVar1 + uVar15;
                  piVar2 = (int *)(iVar13 + 0x36);
                  *piVar2 = *piVar2 + iVar12 + (uint)CARRY2(uVar19,uVar15);
                }
                if (iVar9 < 0) {
                  iVar9 = *(int *)((uint)bVar5 * 4 + 0x13f2);
                  uVar15 = FUN_24dd_3d80();
                  uVar24 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
                  iVar12 = (int)*(undefined4 *)0x6670;
                  puVar1 = (uint *)(iVar12 + 0x34);
                  uVar19 = *puVar1;
                  *puVar1 = *puVar1 - uVar15;
                  piVar2 = (int *)(iVar12 + 0x36);
                  *piVar2 = (*piVar2 - iVar9) - (uint)(uVar19 < uVar15);
                }
              }
              FUN_24dd_3e63();
              FUN_24dd_3d80(*(undefined1 *)(bVar5 + 0x13d7),0);
              iVar9 = FUN_24dd_3dbd();
              if (0 < *(int *)((int)*(undefined4 *)0x6670 + 0x50)) {
                piVar2 = (int *)((int)*(undefined4 *)0x6670 + 0x50);
                *piVar2 = *piVar2 - iVar9;
                if (*(int *)((int)*(undefined4 *)0x6670 + 0x50) < 1) {
                  if ((*(byte *)(piVar21 + 2) & 0x80) == 0x80) {
                    *(undefined1 *)((int)*(undefined4 *)0x6670 + 0x96) = 0;
                  }
                  else {
                    *(undefined1 *)((int)*(undefined4 *)0x6670 + 0x96) = 1;
                  }
                }
                uVar15 = *(int *)0x66aa >> 0xf;
                FUN_24dd_3d80();
                uVar19 = FUN_24dd_3dbd();
                if ((uVar15 < 0x8000) && ((0 < (int)uVar15 || (uVar19 != 0)))) {
                  local_10 = 1;
                  local_e = 0;
                  while( true ) {
                    uVar33 = 7;
                    uVar31 = 0;
                    uVar24 = *(undefined2 *)((int)*(undefined4 *)0x6670 + 6);
                    uVar28 = *(undefined2 *)((int)*(undefined4 *)0x6670 + 10);
                    uVar30 = *(undefined2 *)((int)*(undefined4 *)0x6670 + 0x32);
                    uVar34 = FUN_24dd_3dbd(uVar28,uVar24,0,7);
                    uVar32 = *(undefined2 *)((int)*(undefined4 *)0x6670 + 0x36);
                    uVar27 = FUN_24dd_3dbd(uVar34,uVar30);
                    uVar29 = FUN_24dd_4654(0x80);
                    FUN_202c_165d(uVar29,uVar27,uVar32,uVar34,uVar30,uVar28,uVar24,uVar31,uVar33);
                    if ((local_e == uVar15) && (local_10 == uVar19)) break;
                    bVar26 = 0xfffe < local_10;
                    local_10 = local_10 + 1;
                    local_e = local_e + bVar26;
                  }
                }
                if (((*(char *)0x4b8 != '\0') && (iVar9 = FUN_24dd_4654(3), iVar9 == 0)) &&
                   (cVar6 = FUN_235c_0a1e(*(undefined1 *)0x4b6), cVar6 == '\0')) {
                  iVar9 = FUN_24dd_4654(3);
                  iVar12 = (iVar9 + 0x13) * 4;
                  FUN_235c_095c(0,CONCAT11((char)((uint)(iVar9 + 0x13) >> 8),*(undefined1 *)0x4b6),
                                *(undefined2 *)(iVar12 + 0x6734),*(undefined2 *)(iVar12 + 0x6736));
                }
              }
            }
          }
        }
      }
    }
    if (*(char *)((int)*(undefined4 *)0x6670 + 0x144) != '\0') {
      iVar9 = local_1a + CARRY2(local_1c,uVar11);
      uVar19 = *(uint *)((int)*(undefined4 *)0x6670 + 0xb0);
      iVar12 = (int)uVar19 >> 0xf;
      if ((iVar12 < iVar9) || ((iVar12 <= iVar9 && (uVar19 < local_1c + uVar11)))) {
        iVar9 = local_1a - (local_1c < uVar11);
        uVar19 = *(uint *)((int)*(undefined4 *)0x6670 + 0xb0);
        iVar12 = (int)uVar19 >> 0xf;
        if ((iVar9 < iVar12) || ((iVar9 <= iVar12 && (local_1c - uVar11 < uVar19)))) {
          iVar9 = local_1e + CARRY2(local_20,uVar11);
          uVar19 = *(uint *)((int)*(undefined4 *)0x6670 + 0xb4);
          iVar12 = (int)uVar19 >> 0xf;
          if ((iVar12 < iVar9) || ((iVar12 <= iVar9 && (uVar19 < local_20 + uVar11)))) {
            iVar9 = local_1e - (local_20 < uVar11);
            uVar19 = *(uint *)((int)*(undefined4 *)0x6670 + 0xb4);
            iVar12 = (int)uVar19 >> 0xf;
            if ((iVar9 < iVar12) || ((iVar9 <= iVar12 && (local_20 - uVar11 < uVar19)))) {
              uVar19 = *(uint *)((int)*(undefined4 *)0x6670 + 0xb0);
              iVar9 = (((int)uVar19 >> 0xf) - local_1a) - (uint)(uVar19 < local_1c);
              uVar24 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
              iVar12 = (int)*(undefined4 *)0x6670;
              uVar15 = *(uint *)(iVar12 + 0xdc);
              if ((int)uVar15 < 0) {
                uVar15 = (~uVar15 + 1) - (uint)(*(int *)(iVar12 + 0xda) != 0);
              }
              if ((int)uVar15 < 2) {
                if ((0 < iVar9) || ((-1 < iVar9 && (uVar19 != local_1c)))) {
                  iVar12 = *(int *)((uint)bVar5 * 4 + 0x13f2);
                  uVar15 = FUN_24dd_3d80();
                  uVar24 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
                  iVar13 = (int)*(undefined4 *)0x6670;
                  puVar1 = (uint *)(iVar13 + 0xda);
                  uVar19 = *puVar1;
                  *puVar1 = *puVar1 + uVar15;
                  piVar2 = (int *)(iVar13 + 0xdc);
                  *piVar2 = *piVar2 + iVar12 + (uint)CARRY2(uVar19,uVar15);
                }
                if (iVar9 < 0) {
                  iVar9 = *(int *)((uint)bVar5 * 4 + 0x13f2);
                  uVar15 = FUN_24dd_3d80();
                  uVar24 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
                  iVar12 = (int)*(undefined4 *)0x6670;
                  puVar1 = (uint *)(iVar12 + 0xda);
                  uVar19 = *puVar1;
                  *puVar1 = *puVar1 - uVar15;
                  piVar2 = (int *)(iVar12 + 0xdc);
                  *piVar2 = (*piVar2 - iVar9) - (uint)(uVar19 < uVar15);
                }
              }
              uVar19 = *(uint *)((int)*(undefined4 *)0x6670 + 0xb4);
              iVar9 = (((int)uVar19 >> 0xf) - local_1e) - (uint)(uVar19 < local_20);
              uVar24 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
              iVar12 = (int)*(undefined4 *)0x6670;
              uVar15 = *(uint *)(iVar12 + 0xe0);
              if ((int)uVar15 < 0) {
                uVar15 = (~uVar15 + 1) - (uint)(*(int *)(iVar12 + 0xde) != 0);
              }
              if ((int)uVar15 < 2) {
                if ((0 < iVar9) || ((-1 < iVar9 && (uVar19 != local_20)))) {
                  iVar12 = *(int *)((uint)bVar5 * 4 + 0x13f2);
                  uVar15 = FUN_24dd_3d80();
                  uVar24 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
                  iVar13 = (int)*(undefined4 *)0x6670;
                  puVar1 = (uint *)(iVar13 + 0xde);
                  uVar19 = *puVar1;
                  *puVar1 = *puVar1 + uVar15;
                  piVar2 = (int *)(iVar13 + 0xe0);
                  *piVar2 = *piVar2 + iVar12 + (uint)CARRY2(uVar19,uVar15);
                }
                if (iVar9 < 0) {
                  iVar9 = *(int *)((uint)bVar5 * 4 + 0x13f2);
                  uVar15 = FUN_24dd_3d80();
                  uVar24 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
                  iVar12 = (int)*(undefined4 *)0x6670;
                  puVar1 = (uint *)(iVar12 + 0xde);
                  uVar19 = *puVar1;
                  *puVar1 = *puVar1 - uVar15;
                  piVar2 = (int *)(iVar12 + 0xe0);
                  *piVar2 = (*piVar2 - iVar9) - (uint)(uVar19 < uVar15);
                }
              }
              FUN_24dd_3e63();
              FUN_24dd_3d80(*(undefined1 *)(bVar5 + 0x13d7),0);
              iVar9 = FUN_24dd_3dbd();
              if (0 < *(int *)((int)*(undefined4 *)0x6670 + 0xfa)) {
                piVar2 = (int *)((int)*(undefined4 *)0x6670 + 0xfa);
                *piVar2 = *piVar2 - iVar9;
                if (*(int *)((int)*(undefined4 *)0x6670 + 0xfa) < 1) {
                  if ((*(byte *)(piVar21 + 2) & 0x80) == 0x80) {
                    *(undefined1 *)((int)*(undefined4 *)0x6670 + 0x140) = 1;
                  }
                  else {
                    *(undefined1 *)((int)*(undefined4 *)0x6670 + 0x140) = 0;
                  }
                }
                iVar9 = *(int *)0x66aa >> 0xf;
                FUN_24dd_3d80();
                uVar19 = FUN_24dd_3dbd();
                if ((-1 < iVar9) && ((0 < iVar9 || (uVar19 != 0)))) {
                  local_10 = 1;
                  local_e = 0;
                  while( true ) {
                    uVar31 = 7;
                    uVar29 = 0;
                    uVar25 = *(undefined2 *)((int)*(undefined4 *)0x6670 + 0xb0);
                    uVar24 = *(undefined2 *)((int)*(undefined4 *)0x6670 + 0xb4);
                    uVar28 = *(undefined2 *)((int)*(undefined4 *)0x6670 + 0xdc);
                    uVar32 = FUN_24dd_3dbd(uVar24,uVar25,0,7);
                    uVar30 = *(undefined2 *)((int)*(undefined4 *)0x6670 + 0xe0);
                    uVar34 = FUN_24dd_3dbd(uVar32,uVar28);
                    uVar27 = FUN_24dd_4654(0x80);
                    FUN_202c_165d(uVar27,uVar34,uVar30,uVar32,uVar28,uVar24,uVar25,uVar29,uVar31);
                    if ((local_e == iVar9) && (local_10 == uVar19)) break;
                    bVar26 = 0xfffe < local_10;
                    local_10 = local_10 + 1;
                    local_e = local_e + bVar26;
                  }
                }
                if (((*(char *)0x4b8 != '\0') && (iVar9 = FUN_24dd_4654(3), iVar9 == 0)) &&
                   (cVar6 = FUN_235c_0a1e(*(undefined1 *)0x4b7), cVar6 == '\0')) {
                  iVar9 = FUN_24dd_4654(3);
                  iVar12 = (iVar9 + 0x13) * 4;
                  FUN_235c_095c(0,CONCAT11((char)((uint)(iVar9 + 0x13) >> 8),*(undefined1 *)0x4b7),
                                *(undefined2 *)(iVar12 + 0x6734),*(undefined2 *)(iVar12 + 0x6736));
                }
              }
            }
          }
        }
      }
    }
    uVar25 = 0x24dd;
    FUN_24dd_3dbd();
    local_18 = 0;
    local_16 = 0;
    do {
      if ((*(char *)((int)*(undefined4 *)0x6688 + local_18 * 0x14 + 0x10) != '\0') &&
         (*(char *)((*(byte *)((int)*(undefined4 *)0x6688 + local_18 * 0x14 + 0x10) & 0x7f) + 0xfc5)
          == '\x01')) {
        iVar9 = local_1a + CARRY2(local_1c,uVar11);
        uVar19 = *(uint *)((int)*(undefined4 *)0x6688 + local_18 * 0x14 + 2);
        iVar12 = (int)uVar19 >> 0xf;
        if ((iVar12 < iVar9) || ((iVar12 <= iVar9 && (uVar19 < local_1c + uVar11)))) {
          iVar9 = local_1a - (local_1c < uVar11);
          uVar19 = *(uint *)((int)*(undefined4 *)0x6688 + local_18 * 0x14 + 2);
          iVar12 = (int)uVar19 >> 0xf;
          if ((iVar9 < iVar12) || ((iVar9 <= iVar12 && (local_1c - uVar11 < uVar19)))) {
            iVar9 = local_1e + CARRY2(local_20,uVar11);
            uVar19 = *(uint *)((int)*(undefined4 *)0x6688 + local_18 * 0x14 + 6);
            iVar12 = (int)uVar19 >> 0xf;
            if ((iVar12 < iVar9) || ((iVar12 <= iVar9 && (uVar19 < local_20 + uVar11)))) {
              iVar9 = local_1e - (local_20 < uVar11);
              uVar19 = *(uint *)((int)*(undefined4 *)0x6688 + local_18 * 0x14 + 6);
              iVar12 = (int)uVar19 >> 0xf;
              if ((iVar9 < iVar12) || ((iVar9 <= iVar12 && (local_20 - uVar11 < uVar19)))) {
                uVar19 = *(uint *)((int)*(undefined4 *)0x6688 + local_18 * 0x14 + 2);
                uVar20 = uVar19 - local_1c;
                uVar18 = (((int)uVar19 >> 0xf) - local_1a) - (uint)(uVar19 < local_1c);
                uVar19 = uVar20;
                uVar15 = uVar18;
                if ((int)uVar18 < 0) {
                  uVar19 = -uVar20;
                  uVar15 = (~uVar18 + 1) - (uint)(uVar20 != 0);
                }
                iVar9 = -(uint)(uVar11 < uVar19) - uVar15;
                if ((0 < iVar9) || ((-1 < iVar9 && (uVar11 != uVar19)))) {
                  if ((0 < (int)uVar18) || ((-1 < (int)uVar18 && (uVar20 != 0)))) {
                    uVar25 = 0x24dd;
                    iVar12 = iVar9;
                    uVar15 = FUN_24dd_3d80();
                    uVar24 = (undefined2)((ulong)*(undefined4 *)0x6688 >> 0x10);
                    iVar13 = (int)*(undefined4 *)0x6688 + local_18 * 0x14;
                    puVar1 = (uint *)(iVar13 + 8);
                    uVar19 = *puVar1;
                    *puVar1 = *puVar1 + uVar15;
                    piVar2 = (int *)(iVar13 + 10);
                    *piVar2 = *piVar2 + iVar12 + (uint)CARRY2(uVar19,uVar15);
                  }
                  if ((int)uVar18 < 0) {
                    uVar25 = 0x24dd;
                    uVar15 = FUN_24dd_3d80();
                    uVar24 = (undefined2)((ulong)*(undefined4 *)0x6688 >> 0x10);
                    iVar12 = (int)*(undefined4 *)0x6688 + local_18 * 0x14;
                    puVar1 = (uint *)(iVar12 + 8);
                    uVar19 = *puVar1;
                    *puVar1 = *puVar1 - uVar15;
                    piVar2 = (int *)(iVar12 + 10);
                    *piVar2 = (*piVar2 - iVar9) - (uint)(uVar19 < uVar15);
                  }
                }
                uVar19 = *(uint *)((int)*(undefined4 *)0x6688 + local_18 * 0x14 + 6);
                uVar20 = uVar19 - local_20;
                uVar18 = (((int)uVar19 >> 0xf) - local_1e) - (uint)(uVar19 < local_20);
                uVar19 = uVar20;
                uVar15 = uVar18;
                if ((int)uVar18 < 0) {
                  uVar19 = -uVar20;
                  uVar15 = (~uVar18 + 1) - (uint)(uVar20 != 0);
                }
                iVar9 = -(uint)(uVar11 < uVar19) - uVar15;
                if ((0 < iVar9) || ((-1 < iVar9 && (uVar11 != uVar19)))) {
                  if ((0 < (int)uVar18) || ((-1 < (int)uVar18 && (uVar20 != 0)))) {
                    uVar25 = 0x24dd;
                    iVar12 = iVar9;
                    uVar15 = FUN_24dd_3d80();
                    uVar24 = (undefined2)((ulong)*(undefined4 *)0x6688 >> 0x10);
                    iVar13 = (int)*(undefined4 *)0x6688 + local_18 * 0x14;
                    puVar1 = (uint *)(iVar13 + 0xc);
                    uVar19 = *puVar1;
                    *puVar1 = *puVar1 + uVar15;
                    piVar2 = (int *)(iVar13 + 0xe);
                    *piVar2 = *piVar2 + iVar12 + (uint)CARRY2(uVar19,uVar15);
                  }
                  if ((int)uVar18 < 0) {
                    uVar25 = 0x24dd;
                    uVar15 = FUN_24dd_3d80();
                    uVar24 = (undefined2)((ulong)*(undefined4 *)0x6688 >> 0x10);
                    iVar12 = (int)*(undefined4 *)0x6688 + local_18 * 0x14;
                    puVar1 = (uint *)(iVar12 + 0xc);
                    uVar19 = *puVar1;
                    *puVar1 = *puVar1 - uVar15;
                    piVar2 = (int *)(iVar12 + 0xe);
                    *piVar2 = (*piVar2 - iVar9) - (uint)(uVar19 < uVar15);
                  }
                }
                if ((*(byte *)((int)*(undefined4 *)0x6688 + local_18 * 0x14 + 0x10) & 0x7f) == 0x23)
                {
                  uVar24 = (undefined2)((ulong)*(undefined4 *)0x6688 >> 0x10);
                  iVar9 = (int)*(undefined4 *)0x6688 + local_18 * 0x14;
                  local_10 = (uint)(*(byte *)(iVar9 + 0x10) & 0x7f);
                  *(undefined1 *)(iVar9 + 0x10) = 0;
                  if (*(char *)(local_10 + 0xe35) != '\0') {
                    FUN_202c_1b84(uVar25,*(undefined2 *)(iVar9 + 6),*(undefined2 *)(iVar9 + 2),
                                  *(byte *)(iVar9 + 0x10) & 0x80 | *(byte *)(local_10 + 0xe35));
                  }
                  if ((*(char *)0x4b8 != '\0') && (*(char *)(local_10 + 0xbb5) != '\0')) {
                    iVar12 = (uint)*(byte *)(local_10 + 0xbb5) * 4;
                    uVar25 = 0x235c;
                    FUN_235c_095c(0,*(undefined1 *)(local_10 + 0xbb5),
                                  *(undefined2 *)(iVar12 + 0x6734),*(undefined2 *)(iVar12 + 0x6736))
                    ;
                  }
                  uVar19 = (uint)*(byte *)(local_10 + 0x11f5);
                  if ((uVar19 != 0) && (uVar19 != 0)) {
                    local_10 = 1;
                    local_e = 0;
                    uVar15 = 0;
                    while( true ) {
                      uVar16 = (undefined1)(uVar15 >> 8);
                      if (*(char *)(local_10 + 0x126d) == '\0') {
                        uVar15 = CONCAT11(uVar16,*(undefined1 *)(iVar9 + 0x10)) & 0xff80;
                        uVar30 = CONCAT11((char)(uVar15 >> 8),
                                          (byte)uVar15 | *(byte *)(local_10 + 0x1245));
                        iVar12 = FUN_24dd_4654(2);
                        iVar12 = (uint)*(byte *)(local_10 + 0x121d) - iVar12;
                        uVar25 = *(undefined2 *)(iVar9 + 2);
                        uVar28 = *(undefined2 *)(iVar9 + 6);
                        uVar31 = 0;
                        uVar29 = 0;
                        uVar27 = 0;
                        uVar34 = 0;
                        uVar32 = FUN_24dd_4654(0x80);
                        FUN_202c_165d(uVar32,uVar34,uVar27,uVar29,uVar31,uVar28,uVar25,iVar12,uVar30
                                     );
                      }
                      else {
                        uVar15 = CONCAT11(uVar16,*(undefined1 *)(iVar9 + 0x10)) & 0xff80;
                        uVar25 = CONCAT11((char)(uVar15 >> 8),
                                          (byte)uVar15 | *(byte *)(local_10 + 0x1245));
                        iVar12 = FUN_24dd_4654(2);
                        FUN_202c_14b6(*(undefined2 *)(iVar9 + 0xc),*(undefined2 *)(iVar9 + 0xe),
                                      *(undefined2 *)(iVar9 + 8),*(undefined2 *)(iVar9 + 10),
                                      *(undefined2 *)(iVar9 + 6),*(undefined2 *)(iVar9 + 2),
                                      (uint)*(byte *)(local_10 + 0x121d) - iVar12,uVar25);
                      }
                      uVar25 = 0x24dd;
                      if ((local_e == 0) && (local_10 == uVar19)) break;
                      local_e = local_e + (0xfffe < local_10);
                      uVar15 = local_10;
                      local_10 = local_10 + 1;
                    }
                  }
                  uVar19 = (uint)*(byte *)(local_10 + 0xe5d);
                  if (uVar19 != 0) {
                    iVar12 = *(int *)(iVar9 + 2) + -7;
                    iVar13 = *(int *)(iVar9 + 6) + -7;
                    uVar28 = (undefined2)((ulong)*(undefined4 *)0x6678 >> 0x10);
                    iVar22 = (int)*(undefined4 *)0x6678 + (uint)*(byte *)(uVar19 + 0x1369) * 0x100;
                    uVar25 = 0x24dd;
                    iVar14 = FUN_24dd_4654(*(undefined1 *)(uVar19 + 0x137d));
                    iVar14 = (uint)*(byte *)(uVar19 + 0x1373) + iVar14;
                    iVar23 = iVar14 * 0x100;
                    if ((*(byte *)(uVar19 + 4999) & 1) == 1) {
                      iVar23 = iVar23 + 1;
                    }
                    FUN_202c_005a(iVar23,(int)*(undefined4 *)0x6678 + iVar14 * 0x100,
                                  (int)((ulong)*(undefined4 *)0x6678 >> 0x10),iVar22,uVar28,iVar13,
                                  iVar12);
                    if (*(char *)0x66af != '\0') {
                      uVar20 = *(int *)(iVar9 + 2) + 10;
                      uVar18 = (int)uVar20 >> 0xf;
                      uVar19 = *(int *)(iVar9 + 2) - 10;
                      uVar15 = (int)uVar19 >> 0xf;
                      if (((int)uVar15 <= (int)uVar18) &&
                         (((int)uVar15 < (int)uVar18 || (uVar19 <= uVar20)))) {
                        do {
                          local_1a = uVar15;
                          local_1c = uVar19;
                          if ((local_1a < 0x8000) &&
                             (((int)local_1a < 0 || (((int)local_1a < 1 && (local_1c < 0x1f8)))))) {
                            uVar10 = *(int *)(iVar9 + 6) + 10;
                            uVar17 = (int)uVar10 >> 0xf;
                            uVar19 = *(int *)(iVar9 + 6) - 10;
                            uVar15 = (int)uVar19 >> 0xf;
                            if (((int)uVar15 <= (int)uVar17) &&
                               (((int)uVar15 < (int)uVar17 || (uVar19 <= uVar10)))) {
                              do {
                                local_1e = uVar15;
                                local_20 = uVar19;
                                if ((local_1e < 0x8000) &&
                                   (((int)local_1e < 0 ||
                                    (((int)local_1e < 1 && (local_20 < 0x15e)))))) {
                                  iVar12 = 0x20;
                                  bVar8 = FUN_24dd_4161();
                                  if ((*(byte *)(iVar12 + 0x14e0) & bVar8) != 0) {
                                    iVar12 = 0x20;
                                    bVar8 = FUN_24dd_4161();
                                    if ((*(byte *)(iVar12 + 0x6604) & bVar8) != 0) {
                                      uVar4 = *(undefined4 *)
                                               ((int)*(undefined4 *)0x6674 + local_20 * 4);
                                      pcVar3 = (char *)((int)uVar4 + local_1c);
                                      *pcVar3 = *pcVar3 + '\x04';
                                      goto LAB_202c_2be0;
                                    }
                                  }
                                  uVar4 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_20 * 4)
                                  ;
                                  bVar8 = *(byte *)((int)uVar4 + local_1c);
                                  if ((0xa3 < bVar8) && (bVar8 < 0xa8)) {
                                    iVar12 = 0x20;
                                    bVar8 = FUN_24dd_4161();
                                    if ((*(byte *)(iVar12 + 0x6604) & bVar8) != 0) {
                                      uVar4 = *(undefined4 *)
                                               ((int)*(undefined4 *)0x6674 + local_20 * 4);
                                      pcVar3 = (char *)((int)uVar4 + local_1c);
                                      *pcVar3 = *pcVar3 + -4;
                                    }
                                  }
                                }
LAB_202c_2be0:
                                if ((local_1e == uVar17) && (local_20 == uVar10)) break;
                                uVar19 = local_20 + 1;
                                uVar15 = local_1e + (0xfffe < local_20);
                              } while( true );
                            }
                          }
                          uVar25 = 0x24dd;
                          if ((local_1a == uVar18) && (local_1c == uVar20)) break;
                          uVar19 = local_1c + 1;
                          uVar15 = local_1a + (0xfffe < local_1c);
                        } while( true );
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
      if ((local_16 == 0) && (local_18 == 600)) goto LAB_202c_2c1f;
      bVar26 = 0xfffe < local_18;
      local_18 = local_18 + 1;
      local_16 = local_16 + (uint)bVar26;
    } while( true );
  }
LAB_202c_2ea2:
  bVar8 = *(byte *)(bVar5 + 0x13d7) >> 1;
  uVar11 = (uint)bVar8;
  local_6 = -uVar11;
  uStack_28 = (uint)bVar8;
  if (-uStack_28 == uVar11 || (int)local_6 < (int)uStack_28) {
    while( true ) {
      local_8 = -uVar11;
      if (-uVar11 == uVar11 || (int)local_8 < (int)uVar11) {
        while( true ) {
          iVar9 = local_8 + param_2;
          iVar12 = 0x20;
          bVar7 = FUN_24dd_4161();
          if (((*(byte *)(iVar12 + 0x6624) & bVar7) != 0) &&
             (iVar12 = FUN_24dd_4654(8), iVar12 == 0)) {
            uVar34 = 3;
            uVar4 = *(undefined4 *)((int)*(undefined4 *)0x6674 + iVar9 * 4);
            uVar19 = (uint)*(byte *)((int)uVar4 + local_6 + param_3);
            uVar32 = 0;
            uVar30 = 0;
            uVar28 = 0;
            uVar24 = 0;
            iVar12 = local_6 + param_3;
            uVar25 = FUN_24dd_4654(0x80);
            FUN_202c_165d(uVar25,uVar24,uVar28,uVar30,uVar32,iVar9,iVar12,uVar19,uVar34);
          }
          uVar25 = 0x24dd;
          if (local_8 == uVar11) break;
          local_8 = local_8 + 1;
        }
      }
      if (local_6 == bVar8) break;
      local_6 = local_6 + 1;
    }
  }
  uVar11 = (uint)*(byte *)(bVar5 + 0x1451);
  if (uVar11 != 0) {
    iVar9 = param_3 + -7;
    iVar12 = param_2 + -7;
    uVar24 = (undefined2)((ulong)*(undefined4 *)0x6678 >> 0x10);
    iVar23 = (int)*(undefined4 *)0x6678 + (uint)*(byte *)(uVar11 + 0x1369) * 0x100;
    uVar25 = 0x24dd;
    iVar13 = FUN_24dd_4654(*(undefined1 *)(uVar11 + 0x137d));
    iVar13 = (uint)*(byte *)(uVar11 + 0x1373) + iVar13;
    iVar14 = iVar13 * 0x100;
    if ((*(byte *)(uVar11 + 4999) & 1) == 1) {
      iVar14 = iVar14 + 1;
    }
    FUN_202c_005a(iVar14,(int)*(undefined4 *)0x6678 + iVar13 * 0x100,
                  (int)((ulong)*(undefined4 *)0x6678 >> 0x10),iVar23,uVar24,iVar12,iVar9);
    if (*(char *)0x66af != '\0') {
      uVar11 = param_3 + 10;
      uVar19 = (int)uVar11 >> 0xf;
      local_1c = param_3 - 10;
      local_1a = (int)local_1c >> 0xf;
      if (((int)local_1a <= (int)uVar19) && (((int)local_1a < (int)uVar19 || (local_1c <= uVar11))))
      {
        do {
          if ((local_1a < 0x8000) &&
             (((int)local_1a < 0 || (((int)local_1a < 1 && (local_1c < 0x1f8)))))) {
            uVar15 = param_2 + 10;
            uVar20 = (int)uVar15 >> 0xf;
            local_20 = param_2 - 10;
            local_1e = (int)local_20 >> 0xf;
            if (((int)local_1e <= (int)uVar20) &&
               (((int)local_1e < (int)uVar20 || (local_20 <= uVar15)))) {
              do {
                if ((local_1e < 0x8000) &&
                   (((int)local_1e < 0 || (((int)local_1e < 1 && (local_20 < 0x15e)))))) {
                  iVar9 = 0x20;
                  bVar8 = FUN_24dd_4161();
                  if ((*(byte *)(iVar9 + 0x14e0) & bVar8) != 0) {
                    iVar9 = 0x20;
                    bVar8 = FUN_24dd_4161();
                    if ((*(byte *)(iVar9 + 0x6604) & bVar8) != 0) {
                      uVar4 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_20 * 4);
                      pcVar3 = (char *)((int)uVar4 + local_1c);
                      *pcVar3 = *pcVar3 + '\x04';
                      goto LAB_202c_31ba;
                    }
                  }
                  uVar4 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_20 * 4);
                  bVar8 = *(byte *)((int)uVar4 + local_1c);
                  if ((0xa3 < bVar8) && (bVar8 < 0xa8)) {
                    iVar9 = 0x20;
                    bVar8 = FUN_24dd_4161();
                    if ((*(byte *)(iVar9 + 0x6604) & bVar8) != 0) {
                      uVar4 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_20 * 4);
                      pcVar3 = (char *)((int)uVar4 + local_1c);
                      *pcVar3 = *pcVar3 + -4;
                    }
                  }
                }
LAB_202c_31ba:
                if ((local_1e == uVar20) && (local_20 == uVar15)) break;
                bVar26 = 0xfffe < local_20;
                local_20 = local_20 + 1;
                local_1e = local_1e + bVar26;
              } while( true );
            }
          }
          uVar25 = 0x24dd;
          if ((local_1a == uVar19) && (local_1c == uVar11)) break;
          bVar26 = 0xfffe < local_1c;
          local_1c = local_1c + 1;
          local_1a = local_1a + bVar26;
        } while( true );
      }
    }
  }
  bVar8 = *(byte *)0x669c;
  if (bVar8 != 0) {
    local_4 = 1;
    while( true ) {
      if ((((*(char *)((int)*(undefined4 *)0x6698 + local_4 * 0xe + -2) != '\0') &&
           ((int)(param_3 - (uint)*(byte *)(bVar5 + 0x13d7)) <
            *(int *)((int)*(undefined4 *)0x6698 + local_4 * 0xe + -0xe))) &&
          (*(int *)((int)*(undefined4 *)0x6698 + local_4 * 0xe + -0xe) <
           (int)((uint)*(byte *)(bVar5 + 0x13d7) + param_3))) &&
         (((int)(param_2 - (uint)*(byte *)(bVar5 + 0x13d7)) <
           *(int *)((int)*(undefined4 *)0x6698 + local_4 * 0xe + -10) &&
          (*(int *)((int)*(undefined4 *)0x6698 + local_4 * 0xe + -10) <
           (int)((uint)*(byte *)(bVar5 + 0x13d7) + param_2))))) {
        *(undefined1 *)((int)*(undefined4 *)0x6698 + local_4 * 0xe + -2) = 0;
        FUN_202c_1b84(uVar25,*(undefined2 *)((int)*(undefined4 *)0x6698 + local_4 * 0xe + -10),
                      *(undefined2 *)((int)*(undefined4 *)0x6698 + local_4 * 0xe + -0xe),1);
      }
      uStack_28 = (uint)bVar8;
      if (local_4 == uStack_28) break;
      local_4 = local_4 + 1;
    }
  }
  return;
LAB_202c_2c1f:
  local_18 = 0;
  local_16 = 0;
  while( true ) {
    if ((*(char *)((int)*(undefined4 *)0x6694 + local_18 * 0x14 + 0x12) != '\0') &&
       (*(char *)((*(byte *)((int)*(undefined4 *)0x6694 + local_18 * 0x14 + 0x12) & 0x7f) + 0x6bd)
        == '\x01')) {
      iVar9 = local_1a + CARRY2(local_1c,uVar11);
      uVar19 = *(uint *)((int)*(undefined4 *)0x6694 + local_18 * 0x14 + 2);
      iVar12 = (int)uVar19 >> 0xf;
      if ((iVar12 < iVar9) || ((iVar12 <= iVar9 && (uVar19 < local_1c + uVar11)))) {
        iVar9 = local_1a - (local_1c < uVar11);
        uVar19 = *(uint *)((int)*(undefined4 *)0x6694 + local_18 * 0x14 + 2);
        iVar12 = (int)uVar19 >> 0xf;
        if ((iVar9 < iVar12) || ((iVar9 <= iVar12 && (local_1c - uVar11 < uVar19)))) {
          iVar9 = local_1e + CARRY2(local_20,uVar11);
          uVar19 = *(uint *)((int)*(undefined4 *)0x6694 + local_18 * 0x14 + 6);
          iVar12 = (int)uVar19 >> 0xf;
          if ((iVar12 < iVar9) || ((iVar12 <= iVar9 && (uVar19 < local_20 + uVar11)))) {
            iVar9 = local_1e - (local_20 < uVar11);
            uVar19 = *(uint *)((int)*(undefined4 *)0x6694 + local_18 * 0x14 + 6);
            iVar12 = (int)uVar19 >> 0xf;
            if ((iVar9 < iVar12) || ((iVar9 <= iVar12 && (local_20 - uVar11 < uVar19)))) {
              uVar19 = *(uint *)((int)*(undefined4 *)0x6694 + local_18 * 0x14 + 2);
              uVar20 = uVar19 - local_1c;
              uVar18 = (((int)uVar19 >> 0xf) - local_1a) - (uint)(uVar19 < local_1c);
              uVar19 = uVar20;
              uVar15 = uVar18;
              if ((int)uVar18 < 0) {
                uVar19 = -uVar20;
                uVar15 = (~uVar18 + 1) - (uint)(uVar20 != 0);
              }
              iVar9 = -(uint)(uVar11 < uVar19) - uVar15;
              if ((0 < iVar9) || ((-1 < iVar9 && (uVar11 != uVar19)))) {
                if ((0 < (int)uVar18) || ((-1 < (int)uVar18 && (uVar20 != 0)))) {
                  uVar25 = 0x24dd;
                  iVar12 = iVar9;
                  uVar15 = FUN_24dd_3d80();
                  uVar24 = (undefined2)((ulong)*(undefined4 *)0x6694 >> 0x10);
                  iVar13 = (int)*(undefined4 *)0x6694 + local_18 * 0x14;
                  puVar1 = (uint *)(iVar13 + 8);
                  uVar19 = *puVar1;
                  *puVar1 = *puVar1 + uVar15;
                  piVar2 = (int *)(iVar13 + 10);
                  *piVar2 = *piVar2 + iVar12 + (uint)CARRY2(uVar19,uVar15);
                }
                if ((int)uVar18 < 0) {
                  uVar25 = 0x24dd;
                  uVar15 = FUN_24dd_3d80();
                  uVar24 = (undefined2)((ulong)*(undefined4 *)0x6694 >> 0x10);
                  iVar12 = (int)*(undefined4 *)0x6694 + local_18 * 0x14;
                  puVar1 = (uint *)(iVar12 + 8);
                  uVar19 = *puVar1;
                  *puVar1 = *puVar1 - uVar15;
                  piVar2 = (int *)(iVar12 + 10);
                  *piVar2 = (*piVar2 - iVar9) - (uint)(uVar19 < uVar15);
                }
              }
              uVar19 = *(uint *)((int)*(undefined4 *)0x6694 + local_18 * 0x14 + 6);
              uVar20 = uVar19 - local_20;
              uVar18 = (((int)uVar19 >> 0xf) - local_1e) - (uint)(uVar19 < local_20);
              uVar19 = uVar20;
              uVar15 = uVar18;
              if ((int)uVar18 < 0) {
                uVar19 = -uVar20;
                uVar15 = (~uVar18 + 1) - (uint)(uVar20 != 0);
              }
              iVar9 = -(uint)(uVar11 < uVar19) - uVar15;
              if ((0 < iVar9) || ((-1 < iVar9 && (uVar11 != uVar19)))) {
                if ((0 < (int)uVar18) || ((-1 < (int)uVar18 && (uVar20 != 0)))) {
                  uVar25 = 0x24dd;
                  iVar12 = iVar9;
                  uVar15 = FUN_24dd_3d80();
                  uVar24 = (undefined2)((ulong)*(undefined4 *)0x6694 >> 0x10);
                  iVar13 = (int)*(undefined4 *)0x6694 + local_18 * 0x14;
                  puVar1 = (uint *)(iVar13 + 0xc);
                  uVar19 = *puVar1;
                  *puVar1 = *puVar1 + uVar15;
                  piVar2 = (int *)(iVar13 + 0xe);
                  *piVar2 = *piVar2 + iVar12 + (uint)CARRY2(uVar19,uVar15);
                }
                if ((int)uVar18 < 0) {
                  uVar25 = 0x24dd;
                  uVar15 = FUN_24dd_3d80();
                  uVar24 = (undefined2)((ulong)*(undefined4 *)0x6694 >> 0x10);
                  iVar12 = (int)*(undefined4 *)0x6694 + local_18 * 0x14;
                  puVar1 = (uint *)(iVar12 + 0xc);
                  uVar19 = *puVar1;
                  *puVar1 = *puVar1 - uVar15;
                  piVar2 = (int *)(iVar12 + 0xe);
                  *piVar2 = (*piVar2 - iVar9) - (uint)(uVar19 < uVar15);
                }
              }
            }
          }
        }
      }
    }
    if ((local_16 == 0) && (local_18 == 600)) break;
    bVar26 = 0xfffe < local_18;
    local_18 = local_18 + 1;
    local_16 = local_16 + (uint)bVar26;
  }
  goto LAB_202c_2ea2;
}

