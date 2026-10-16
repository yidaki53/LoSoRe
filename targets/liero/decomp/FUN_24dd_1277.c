
void FUN_24dd_1277(int *param_1,uint *param_2,uint *param_3)

{
  int iVar1;
  ulong uVar2;
  ulong uVar3;
  ulong uVar4;
  long lVar5;
  uint uVar6;
  uint uVar7;
  uint uVar8;
  uint uVar9;
  uint uVar10;
  uint uVar11;
  int iVar12;
  byte bVar13;
  uint uVar14;
  uint uVar15;
  uint uVar16;
  uint uVar17;
  uint uVar18;
  uint uVar19;
  uint uVar20;
  char cVar21;
  byte bVar22;
  uint uVar23;
  int iVar24;
  int iVar25;
  undefined2 unaff_ES;
  undefined2 unaff_DS;
  bool bVar26;
  bool bVar27;
  bool bVar28;
  uint local_14;
  uint local_12;
  uint local_10;
  uint local_e;
  uint local_c;
  int local_4;
  
  local_c = param_3[3];
  local_e = param_3[2];
  local_10 = param_3[1];
  local_12 = *param_3;
  uVar6 = param_3[5];
  uVar7 = param_2[5];
  uVar23 = param_2[4];
  uVar18 = param_3[4];
  bVar26 = uVar23 < 0x4001;
  if ((int)uVar23 < 0x4001) {
    bVar26 = uVar18 < 0x4001;
    if ((int)uVar18 < 0x4001) {
      if (-0x3fff < (int)uVar23) {
        if ((int)uVar18 < -0x3ffe) goto LAB_24dd_12db;
        local_4 = uVar18 - uVar23;
        if (local_4 < 0x4001) {
          if (local_4 < -0x3ffe) {
            FUN_24dd_2361();
          }
          else {
            uVar23 = param_2[3];
            bVar26 = uVar23 < local_c;
            uVar18 = local_c;
            if (uVar23 <= local_c) {
              bVar26 = local_c < uVar23;
              uVar18 = local_c - uVar23;
            }
            uVar8 = (uint)(CONCAT22(uVar18,local_e) / (ulong)uVar23);
            uVar18 = uVar8 + 1;
            uVar9 = uVar18 + bVar26;
            bVar13 = (uVar23 <= local_c) + (0xfffe < uVar8 || CARRY2(uVar18,(uint)bVar26));
            uVar14 = (uint)bVar13;
            uVar18 = *param_2;
            uVar8 = param_2[1];
            if (uVar14 != 0) {
              do {
                bVar26 = local_12 < uVar18;
                local_12 = local_12 - uVar18;
                bVar27 = local_10 < uVar8;
                uVar19 = local_10 - uVar8;
                local_10 = uVar19 - bVar26;
                uVar19 = (uint)(bVar27 || uVar19 < bVar26);
                bVar26 = local_e < param_2[2];
                uVar15 = local_e - param_2[2];
                local_e = uVar15 - uVar19;
                local_c = (local_c - uVar23) - (uint)(bVar26 || uVar15 < uVar19);
                uVar14 = uVar14 - 1;
              } while (uVar14 != 0);
            }
            local_14 = (uint)((ulong)uVar18 * (ulong)uVar9);
            uVar2 = (ulong)uVar8 * (ulong)uVar9 + ((ulong)uVar18 * (ulong)uVar9 >> 0x10);
            uVar23 = (uint)uVar2;
            lVar5 = (ulong)param_2[2] * (ulong)uVar9 + (uVar2 >> 0x10);
            uVar18 = (uint)lVar5;
            uVar19 = (uint)((ulong)lVar5 >> 0x10);
            uVar14 = (uint)((ulong)uVar9 * (ulong)param_2[3]);
            uVar8 = uVar14 + uVar19;
            bVar26 = uVar23 < local_12;
            local_12 = uVar23 - local_12;
            uVar23 = (uint)bVar26;
            bVar26 = uVar18 < local_10;
            uVar18 = uVar18 - local_10;
            local_10 = uVar18 - uVar23;
            uVar23 = (uint)(bVar26 || uVar18 < uVar23);
            bVar26 = uVar8 < local_e;
            uVar8 = uVar8 - local_e;
            local_e = uVar8 - uVar23;
            uVar18 = param_2[3];
            uVar2 = CONCAT22((((int)((ulong)uVar9 * (ulong)param_2[3] >> 0x10) +
                              (uint)CARRY2(uVar14,uVar19)) - local_c) -
                             (uint)(bVar26 || uVar8 < uVar23),local_e);
            uVar23 = (uint)((uVar2 % (ulong)uVar18 << 0x10 | (ulong)local_10) / (ulong)uVar18);
            uVar19 = uVar23 + 1;
            uVar15 = (int)(uVar2 / uVar18) + (uint)(0xfffe < uVar23);
            bVar26 = uVar9 < uVar15;
            uVar9 = uVar9 - uVar15;
            uVar23 = uVar9 - (uVar19 != 0);
            uVar8 = *param_2;
            uVar14 = param_2[1];
            if (uVar15 != 0) {
              do {
                bVar27 = local_14 < uVar8;
                local_14 = local_14 - uVar8;
                bVar28 = local_12 < uVar14;
                uVar16 = local_12 - uVar14;
                local_12 = uVar16 - bVar27;
                uVar16 = (uint)(bVar28 || uVar16 < bVar27);
                bVar27 = local_10 < param_2[2];
                uVar10 = local_10 - param_2[2];
                local_10 = uVar10 - uVar16;
                local_e = (local_e - uVar18) - (uint)(bVar27 || uVar10 < uVar16);
                uVar15 = uVar15 - 1;
              } while (uVar15 != 0);
            }
            uVar2 = (ulong)uVar14 * (ulong)uVar19 + ((ulong)uVar8 * (ulong)uVar19 >> 0x10);
            uVar8 = (uint)uVar2;
            lVar5 = (ulong)param_2[2] * (ulong)uVar19 + (uVar2 >> 0x10);
            uVar16 = (uint)lVar5;
            uVar20 = (uint)((ulong)lVar5 >> 0x10);
            uVar10 = (uint)((ulong)uVar19 * (ulong)param_2[3]);
            uVar11 = uVar10 + uVar20;
            uVar18 = uVar8 - local_14;
            uVar14 = (uint)(uVar8 < local_14);
            uVar15 = uVar16 - local_12;
            uVar8 = uVar15 - uVar14;
            uVar15 = (uint)(uVar16 < local_12 || uVar15 < uVar14);
            uVar16 = uVar11 - local_10;
            iVar12 = uVar16 - uVar15;
            uVar14 = param_2[3];
            uVar2 = CONCAT22((((int)((ulong)uVar19 * (ulong)param_2[3] >> 0x10) +
                              (uint)CARRY2(uVar10,uVar20)) - local_e) -
                             (uint)(uVar11 < local_10 || uVar16 < uVar15),iVar12);
            uVar15 = (uint)((uVar2 % (ulong)uVar14 << 0x10 | (ulong)uVar8) / (ulong)uVar14);
            uVar20 = uVar15 + 1;
            uVar11 = (int)(uVar2 / uVar14) + (uint)(0xfffe < uVar15);
            iVar25 = -uVar19 + uVar11;
            uVar10 = (uint)CARRY2(-uVar19,uVar11);
            iVar1 = uVar23 + uVar10;
            uVar15 = param_2[1];
            uVar16 = param_2[2];
            for (; uVar11 != 0; uVar11 = uVar11 - 1) {
              bVar27 = uVar18 < uVar15;
              uVar18 = uVar18 - uVar15;
              bVar28 = uVar8 < uVar16;
              uVar17 = uVar8 - uVar16;
              uVar8 = uVar17 - bVar27;
              iVar12 = (iVar12 - uVar14) - (uint)(bVar28 || uVar17 < bVar27);
            }
            lVar5 = (ulong)uVar16 * (ulong)uVar20 + ((ulong)uVar15 * (ulong)uVar20 >> 0x10);
            uVar14 = (uint)lVar5;
            uVar17 = (uint)((ulong)lVar5 >> 0x10);
            uVar15 = (uint)((ulong)param_2[3] * (ulong)uVar20);
            uVar16 = uVar15 + uVar17;
            iVar24 = uVar14 - uVar18;
            uVar18 = (uint)(uVar14 < uVar18);
            uVar14 = uVar16 - uVar8;
            uVar11 = uVar14 - uVar18;
            uVar8 = (((int)((ulong)param_2[3] * (ulong)uVar20 >> 0x10) + (uint)CARRY2(uVar15,uVar17)
                     ) - iVar12) - (uint)(uVar16 < uVar8 || uVar14 < uVar18);
            uVar18 = (uint)CARRY2(param_2[2],param_2[2]);
            uVar14 = param_2[3] + uVar18;
            if (!CARRY2(param_2[3],uVar18)) {
              uVar2 = (ulong)CONCAT12(iVar24 < 0,uVar11) << 1;
              bVar27 = (uVar2 & 0x10000) != 0;
              uVar2 = ((ulong)CONCAT12(bVar27,uVar8) << 1 | (ulong)bVar27) << 0x10 |
                      uVar2 & 0xffff | (ulong)(iVar24 < 0);
              uVar3 = uVar2 / uVar14;
              uVar2 = uVar2 % (ulong)uVar14 << 0x10 | (ulong)(uint)(iVar24 * 2);
              uVar4 = uVar2 / uVar14;
              uVar8 = (uint)uVar3 >> 1;
              uVar11 = (uint)(((ulong)((uVar3 & 1) != 0) << 0x10 | uVar4 & 0xffff) >> 1);
              iVar24 = (((uint)((uVar4 & 1) != 0) << 8 | (uint)(uVar2 % (ulong)uVar14) >> 8) >> 1)
                       << 8;
            }
            cVar21 = (char)((uint)iVar24 >> 8);
            bVar22 = -cVar21;
            uVar18 = (uint)(cVar21 == '\0');
            uVar15 = ~uVar11 + uVar18;
            uVar18 = (uint)CARRY2(~uVar11,uVar18);
            uVar14 = ~uVar8 + uVar20;
            uVar16 = uVar14 + uVar18;
            uVar18 = (uint)(CARRY2(~uVar8,uVar20) || CARRY2(uVar14,uVar18));
            uVar8 = iVar25 - 1;
            uVar14 = uVar8 + uVar18;
            uVar18 = (uint)(iVar25 != 0 || CARRY2(uVar8,uVar18));
            uVar8 = iVar1 - 1;
            uVar11 = uVar8 + uVar18;
            bVar13 = (bVar13 - (bVar26 || uVar9 < (uVar19 != 0))) + CARRY2(uVar23,uVar10) + -1 +
                     (iVar1 != 0 || CARRY2(uVar8,uVar18));
            uVar9 = uVar15;
            uVar18 = uVar14;
            uVar8 = uVar16;
            uVar23 = uVar11;
            if ((bool)(bVar13 & 1)) {
              uVar23 = (uint)((CONCAT12(bVar13,uVar11) & 0x1ffff) >> 1);
              uVar18 = (uint)(CONCAT12((uVar11 & 1) != 0,uVar14) >> 1);
              uVar8 = (uint)(CONCAT12((uVar14 & 1) != 0,uVar16) >> 1);
              uVar9 = (uint)(CONCAT12((uVar16 & 1) != 0,uVar15) >> 1);
              bVar22 = (byte)(CONCAT11((uVar15 & 1) != 0,bVar22) >> 1);
              local_4 = local_4 + 1;
            }
            uVar14 = (uint)CARRY2(uVar9,(uint)CARRY1(bVar22,bVar22));
            uVar19 = (uint)CARRY2(uVar8,uVar14);
            uVar15 = (uint)CARRY2(uVar18,uVar19);
            iVar25 = uVar23 + uVar15;
            if ((byte)((bVar13 >> 1) + CARRY2(uVar23,uVar15)) != '\0') {
              iVar25 = -0x8000;
              local_4 = local_4 + 1;
            }
            if (local_4 < 0x4001) {
              *param_1 = uVar9 + CARRY1(bVar22,bVar22);
              param_1[1] = uVar8 + uVar14;
              param_1[2] = uVar18 + uVar19;
              param_1[3] = iVar25;
              param_1[4] = local_4;
              param_1[5] = (int)(char)((byte)uVar6 ^ (byte)uVar7);
              return;
            }
          }
          goto LAB_24dd_12db;
        }
      }
      FUN_24dd_2361();
    }
    else {
      FUN_24dd_0e57();
      if (bVar26) {
        return;
      }
    }
  }
  else {
    FUN_24dd_0e57();
    if (bVar26) {
      return;
    }
    if (0x4000 < (int)param_3[4]) {
      FUN_24dd_060f();
      return;
    }
  }
LAB_24dd_12db:
  FUN_24dd_05fd();
  return;
}

