
/* WARNING: Removing unreachable block (ram,0x000175ba) */

void FUN_1000_5e66(void)

{
  uint *puVar1;
  int *piVar2;
  uint uVar3;
  undefined4 uVar4;
  char cVar5;
  char cVar6;
  byte bVar7;
  int *piVar8;
  uint uVar9;
  uint uVar10;
  int iVar11;
  int iVar12;
  int iVar13;
  int iVar14;
  undefined2 uVar15;
  undefined2 uVar16;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  bool bVar17;
  undefined1 *puVar18;
  undefined1 *puVar19;
  undefined2 uVar20;
  undefined2 uVar21;
  undefined2 uVar22;
  undefined1 local_33a [256];
  undefined1 local_23a [252];
  int *local_13e;
  int *local_13c;
  int *piStack_13a;
  uint uStack_138;
  uint local_136;
  int local_134;
  uint local_132;
  int local_130;
  int *local_12e;
  int local_12c;
  undefined1 local_129;
  byte local_128;
  byte local_122 [264];
  uint auStack_1a [5];
  undefined2 local_10;
  undefined2 local_c;
  int local_a;
  int local_8;
  int *local_6;
  uint local_4;
  
  local_4 = 0x1000;
  local_6 = (int *)0x5e71;
  FUN_24dd_0530();
  iVar14 = *(int *)0x2;
  iVar11 = iVar14 >> 0xf;
  FUN_24dd_3dbd();
  if (iVar14 == 0 && iVar11 == 0) {
    FUN_1ec2_13d3((int)*(undefined4 *)0x6684,(int)((ulong)*(undefined4 *)0x6684 >> 0x10));
  }
  local_4 = 0;
  while( true ) {
    uStack_138 = (uint)((ulong)*(undefined4 *)0x6670 >> 0x10);
    piStack_13a = (int *)((int)*(undefined4 *)0x6670 + local_4 * 0xaa);
    if (*(int *)((int)piStack_13a + 0x4c) < 1) {
      if (*(char *)((int)piStack_13a + 0x9a) == '\0') {
        local_12e = (int *)0x0;
        local_12c = 0;
        while( true ) {
          if (*(int *)(local_4 * 2 + 0x67b0) < *(int *)((int)piStack_13a + 6) + -0x50) {
            piVar2 = (int *)(local_4 * 2 + 0x67b0);
            *piVar2 = *piVar2 + 1;
          }
          if (*(int *)((int)piStack_13a + 6) + -0x50 < *(int *)(local_4 * 2 + 0x67b0)) {
            piVar2 = (int *)(local_4 * 2 + 0x67b0);
            *piVar2 = *piVar2 + -1;
          }
          if (*(int *)(local_4 * 2 + 0x67b4) < *(int *)((int)piStack_13a + 10) + -0x50) {
            piVar2 = (int *)(local_4 * 2 + 0x67b4);
            *piVar2 = *piVar2 + 1;
          }
          if (*(int *)((int)piStack_13a + 10) + -0x50 < *(int *)(local_4 * 2 + 0x67b4)) {
            piVar2 = (int *)(local_4 * 2 + 0x67b4);
            *piVar2 = *piVar2 + -1;
          }
          if ((local_12c == 0) && (local_12e == (int *)0x3)) break;
          bVar17 = (int *)0xfffe < local_12e;
          local_12e = (int *)((int)local_12e + 1);
          local_12c = local_12c + (uint)bVar17;
        }
      }
      else {
        *(int *)(local_4 * 2 + 0x67b0) = *(int *)((int)piStack_13a + 6) + -0x50;
        *(int *)(local_4 * 2 + 0x67b4) = *(int *)((int)piStack_13a + 10) + -0x50;
        local_12e = (int *)0x0;
        local_12c = 0;
        local_132 = 0;
        local_130 = 0;
        local_136 = 0;
        local_134 = 0;
        if (*(char *)(*(int *)((int)piStack_13a + *(int *)((int)piStack_13a + 0x4e) * 2 + 0x73) +
                     0x11a5) == '\x02') {
          local_6 = (int *)0x0;
          while( true ) {
            local_128 = *(byte *)((int)*(undefined4 *)0x6688 + (int)local_6 * 0x14 + 0x10) & 0x7f;
            if (((uint)local_128 ==
                 *(uint *)((int)piStack_13a + *(int *)((int)piStack_13a + 0x4e) * 2 + 0x73)) &&
               ((*(byte *)((int)*(undefined4 *)0x6688 + (int)local_6 * 0x14 + 0x10) & 0x80) ==
                *(byte *)(local_4 + 0x6c))) {
              bVar17 = (int *)0xfffe < local_12e;
              local_12e = (int *)((int)local_12e + 1);
              local_12c = local_12c + (uint)bVar17;
              uVar9 = *(int *)((int)*(undefined4 *)0x6688 + (int)local_6 * 0x14 + 2) - 0x50;
              bVar17 = CARRY2(local_132,uVar9);
              local_132 = local_132 + uVar9;
              local_130 = local_130 + ((int)uVar9 >> 0xf) + (uint)bVar17;
              uVar9 = *(int *)((int)*(undefined4 *)0x6688 + (int)local_6 * 0x14 + 6) - 0x50;
              bVar17 = CARRY2(local_136,uVar9);
              local_136 = local_136 + uVar9;
              local_134 = local_134 + ((int)uVar9 >> 0xf) + (uint)bVar17;
            }
            if (local_6 == (int *)0x258) break;
            local_6 = (int *)((int)local_6 + 1);
          }
        }
        if ((0 < local_12c) || ((-1 < local_12c && (local_12e != (int *)0x0)))) {
          uVar15 = FUN_24dd_3dbd();
          *(undefined2 *)(local_4 * 2 + 0x67b0) = uVar15;
          uVar15 = FUN_24dd_3dbd();
          *(undefined2 *)(local_4 * 2 + 0x67b4) = uVar15;
        }
      }
    }
    else if (*(int *)((int)piStack_13a + 0x50) < 1) {
      *(int *)(local_4 * 2 + 0x67b0) = *(int *)((int)piStack_13a + 6) + -0x50;
      *(int *)(local_4 * 2 + 0x67b4) = *(int *)((int)piStack_13a + 10) + -0x50;
    }
    if (*(int *)(local_4 * 2 + 0x67b0) < 0) {
      *(undefined2 *)(local_4 * 2 + 0x67b0) = 0;
    }
    if (*(int *)(local_4 * 2 + 0x67b4) < 0) {
      *(undefined2 *)(local_4 * 2 + 0x67b4) = 0;
    }
    if (0x15a < *(int *)(local_4 * 2 + 0x67b0)) {
      *(undefined2 *)(local_4 * 2 + 0x67b0) = 0x15a;
    }
    if (0xc0 < *(int *)(local_4 * 2 + 0x67b4)) {
      *(undefined2 *)(local_4 * 2 + 0x67b4) = 0xc0;
    }
    if (0 < *(int *)(local_4 * 4 + 0x67ba)) {
      iVar14 = FUN_24dd_4654(*(int *)(local_4 * 4 + 0x67ba) << 1);
      piVar2 = (int *)(local_4 * 2 + 0x67b4);
      *piVar2 = *piVar2 + (iVar14 - *(int *)(local_4 * 4 + 0x67ba));
      iVar14 = FUN_24dd_4654(*(int *)(local_4 * 4 + 0x67ba) << 1);
      piVar2 = (int *)(local_4 * 2 + 0x67b0);
      *piVar2 = *piVar2 + (iVar14 - *(int *)(local_4 * 4 + 0x67ba));
      if (*(int *)(local_4 * 2 + 0x67b0) < 0) {
        *(undefined2 *)(local_4 * 2 + 0x67b0) = 0;
      }
      if (*(int *)(local_4 * 2 + 0x67b4) < 0) {
        *(undefined2 *)(local_4 * 2 + 0x67b4) = 0;
      }
      if (0x15a < *(int *)(local_4 * 2 + 0x67b0)) {
        *(undefined2 *)(local_4 * 2 + 0x67b0) = 0x15a;
      }
      if (0xc0 < *(int *)(local_4 * 2 + 0x67b4)) {
        *(undefined2 *)(local_4 * 2 + 0x67b4) = 0xc0;
      }
    }
    iVar14 = *(int *)0x2;
    iVar11 = iVar14 >> 0xf;
    FUN_24dd_3dbd();
    if (iVar14 == 0 && iVar11 == 0) {
      uVar4 = *(undefined4 *)((int)*(undefined4 *)0x6674 + *(int *)(local_4 * 2 + 0x67b4) * 4);
      FUN_1ea2_01a8((int)*(undefined4 *)0x6684 + *(int *)(local_4 * 4 + 0x12) * 0x140 +
                    *(int *)(local_4 * 4 + 0x10),(int)((ulong)*(undefined4 *)0x6684 >> 0x10),100,
                    0x9e,0x1f8,(int)uVar4 + *(int *)(local_4 * 2 + 0x67b0),
                    (int)((ulong)uVar4 >> 0x10));
      uVar4 = *(undefined4 *)
               ((int)*(undefined4 *)0x6674 + (*(int *)(local_4 * 2 + 0x67b4) + 100) * 4);
      uVar15 = 0x1ea2;
      FUN_1ea2_01a8((int)*(undefined4 *)0x6684 + (*(int *)(local_4 * 4 + 0x12) + 100) * 0x140 +
                    *(int *)(local_4 * 4 + 0x10),(int)((ulong)*(undefined4 *)0x6684 >> 0x10),0x3a,
                    0x9e,0x1f8,(int)uVar4 + *(int *)(local_4 * 2 + 0x67b0),
                    (int)((ulong)uVar4 >> 0x10));
      if (*(char *)((int)piStack_13a + 0x9a) == '\0') {
        uVar9 = (*(int *)((int)piStack_13a + 0x4c) * 0x19) / 0x25;
        local_12e = (int *)(100 - uVar9);
        local_12c = -(uint)(100 < uVar9) - ((int)uVar9 >> 0xf);
        if ((0 < local_12c) || ((-1 < local_12c && (local_12e != (int *)0x0)))) {
          if ((0 < local_12c) || ((-1 < local_12c && ((int *)0x64 < local_12e)))) {
            local_12e = (int *)0x64;
            local_12c = 0;
          }
          uVar16 = *(undefined2 *)(local_4 * 2 + 0x18);
          uVar20 = 0xa1;
          piVar8 = local_12e;
          iVar14 = FUN_24dd_3dbd(0xa1,local_12e,uVar16);
          uVar15 = 0x1ec2;
          FUN_1ec2_12ad((int)*(undefined4 *)0x6684,(int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                        iVar14 + 0xea,uVar20,piVar8,uVar16);
        }
      }
      else {
        iVar14 = *(int *)((int)piStack_13a + 0x50) >> 0xf;
        FUN_24dd_3d80(*(undefined2 *)(local_4 * 2 + 0x66e8),0);
        uVar15 = 0x24dd;
        piVar8 = (int *)FUN_24dd_3dbd();
        local_12e = piVar8;
        local_12c = iVar14;
        if ((0 < iVar14) || ((-1 < iVar14 && (piVar8 != (int *)0x0)))) {
          uVar16 = *(undefined2 *)(local_4 * 2 + 0x18);
          uVar20 = 0xa1;
          iVar14 = FUN_24dd_3dbd(0xa1,piVar8,uVar16);
          uVar15 = 0x1ec2;
          FUN_1ec2_12ad((int)*(undefined4 *)0x6684,(int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                        iVar14 + 0xea,uVar20,piVar8,uVar16);
        }
      }
      if (*(char *)((int)piStack_13a + *(int *)((int)piStack_13a + 0x4e) + 0x6f) == '\0') {
        iVar11 = *(int *)((int)piStack_13a + *(int *)((int)piStack_13a + 0x4e) * 2 + 0x73) * 4;
        iVar14 = *(int *)((int)piStack_13a + *(int *)((int)piStack_13a + 0x4e) * 4 + 0x5a);
        FUN_24dd_3d80(*(undefined2 *)(iVar11 + 0x6478),*(undefined2 *)(iVar11 + 0x647a));
        uVar16 = 0x24dd;
        uVar9 = FUN_24dd_3dbd();
        piVar8 = (int *)(100 - uVar9);
        local_12c = -(uint)(100 < uVar9) - iVar14;
        local_12e = piVar8;
        if ((0 < local_12c) || ((-1 < local_12c && (piVar8 != (int *)0x0)))) {
          uVar15 = *(undefined2 *)(local_4 * 2 + 0x18);
          uVar20 = 0xa6;
          iVar14 = FUN_24dd_3dbd(0xa6,piVar8,uVar15);
          uVar16 = 0x1ec2;
          FUN_1ec2_12ad((int)*(undefined4 *)0x6684,(int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                        iVar14 + 0xf5,uVar20,piVar8,uVar15);
        }
        uVar15 = uVar16;
        if ((10 < *(uint *)0x6520 % 0x14) && (*(char *)((int)piStack_13a + 0x9a) != '\0')) {
          uVar15 = 0x1ec2;
          FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x6684,
                        (int)((ulong)*(undefined4 *)0x6684 >> 0x10),0x32,0x5e13,uVar16,0xa4,
                        *(undefined2 *)(local_4 * 2 + 0x18));
        }
      }
      else if (0 < *(int *)((int)piStack_13a + *(int *)((int)piStack_13a + 0x4e) * 2 + 0x7d)) {
        piVar8 = (int *)((*(int *)((int)piStack_13a + *(int *)((int)piStack_13a + 0x4e) * 2 + 0x7d)
                         * 100) / (int)(uint)*(byte *)(*(int *)((int)piStack_13a +
                                                                *(int *)((int)piStack_13a + 0x4e) *
                                                                2 + 0x73) + 0xe0d));
        local_12c = (int)piVar8 >> 0xf;
        uVar16 = *(undefined2 *)(local_4 * 2 + 0x18);
        uVar20 = 0xa6;
        local_12e = piVar8;
        iVar14 = FUN_24dd_3dbd(0xa6,piVar8,uVar16);
        uVar15 = 0x1ec2;
        FUN_1ec2_12ad((int)*(undefined4 *)0x6684,(int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                      iVar14 + 0xf5,uVar20,piVar8,uVar16);
      }
      if (((*(char *)((int)piStack_13a + 0x9a) == '\0') && (*(int *)((int)piStack_13a + 0x4c) < 1))
         && (*(char *)((int)piStack_13a + 0x9f) == '\0')) {
        FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x6684 + 0x141,
                      (int)((ulong)*(undefined4 *)0x6684 >> 0x10),0,0x5e20,uVar15,0x4c,
                      local_4 * 0xa0 + 0x32);
        uVar15 = 0x1ec2;
        FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x6684,
                      (int)((ulong)*(undefined4 *)0x6684 >> 0x10),0x32,0x5e20,0x1ec2,0x4c,
                      local_4 * 0xa0 + 0x32);
      }
      uVar16 = *(undefined2 *)(local_4 * 2 + 0x18);
      uVar21 = 0;
      puVar19 = local_33a;
      uVar20 = unaff_SS;
      FUN_24dd_3e95(0x5e34,uVar15);
      puVar18 = local_23a;
      uVar15 = unaff_SS;
      FUN_202c_076d(*(undefined2 *)((int)piStack_13a + 0x3c),
                    *(undefined2 *)((int)piStack_13a + 0x3e));
      FUN_24dd_3f14(puVar18,uVar15);
      FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x6684 + -0x2a40,
                    (int)((ulong)*(undefined4 *)0x6684 >> 0x10),10,puVar19,uVar20,uVar21,uVar16);
      if (*(char *)0x66ac == '\0') {
        uVar15 = *(undefined2 *)(local_4 * 2 + 0x18);
        uVar21 = 0;
        puVar19 = local_33a;
        uVar20 = unaff_SS;
        FUN_24dd_3e95(0x5e3c,0x1ec2);
        puVar18 = local_23a;
        uVar16 = unaff_SS;
        FUN_202c_076d(*(undefined2 *)((int)piStack_13a + 0x38),
                      *(undefined2 *)((int)piStack_13a + 0x3a));
        FUN_24dd_3f14(puVar18,uVar16);
        FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x6684 + -0x2180,
                      (int)((ulong)*(undefined4 *)0x6684 >> 0x10),6,puVar19,uVar20,uVar21,uVar15);
      }
      if ((1 < *(byte *)0x66ac) && (*(byte *)0x66ac < 4)) {
        uVar15 = *(undefined2 *)(local_4 * 2 + 0x18);
        uVar22 = 0;
        puVar19 = local_33a;
        uVar20 = unaff_SS;
        FUN_24dd_3e95(0x5e44,0x1ec2);
        puVar18 = local_23a;
        uVar16 = unaff_SS;
        FUN_202c_076d(*(undefined2 *)((int)piStack_13a + 0x40),
                      *(undefined2 *)((int)piStack_13a + 0x42));
        FUN_24dd_3f14(puVar18,uVar16);
        uVar16 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
        iVar13 = (int)*(undefined4 *)0x6670 + (local_4 ^ 1) * 0xaa;
        iVar14 = *(int *)(iVar13 + 0x42);
        uVar21 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
        iVar12 = (int)*(undefined4 *)0x6670 + local_4 * 0xaa;
        iVar11 = *(int *)(iVar12 + 0x42);
        if ((iVar11 < iVar14) ||
           ((iVar11 <= iVar14 && (*(uint *)(iVar12 + 0x40) < *(uint *)(iVar13 + 0x40))))) {
          cVar5 = '\x01';
        }
        else {
          cVar5 = '\0';
        }
        if (((local_4 ^ 1) == (uint)*(byte *)0x651f) || (*(char *)0x66ac == '\x03')) {
          cVar6 = '\x01';
        }
        else {
          cVar6 = '\0';
        }
        FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x6684 + -0x18c0,
                      (int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                      *(undefined1 *)(cVar6 * 2 + (int)cVar5 + 0xc),puVar19,uVar20,uVar22,uVar15);
      }
    }
    if (local_4 == 1) break;
    local_4 = local_4 + 1;
  }
  cVar5 = *(char *)0x66ac;
  if (cVar5 == '\x01') {
    iVar14 = *(int *)0x2;
    iVar11 = iVar14 >> 0xf;
    FUN_24dd_3dbd();
    if (iVar14 == 0 && iVar11 == 0) {
      uStack_138 = (uint)((ulong)*(undefined4 *)0x6670 >> 0x10);
      piStack_13a = (int *)*(undefined4 *)0x6670;
      puVar19 = local_23a;
      uVar15 = unaff_SS;
      FUN_1ec2_00d0(*(undefined2 *)((int)piStack_13a + 0x44),
                    *(undefined2 *)((int)piStack_13a + 0x46));
      FUN_24dd_3eaf(0xff,local_122,unaff_SS,puVar19,uVar15);
      uVar15 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
      iVar11 = (int)*(undefined4 *)0x6670;
      iVar14 = *(int *)(iVar11 + 0xf0);
      if ((iVar14 < *(int *)((int)piStack_13a + 0x46)) ||
         ((iVar14 <= *(int *)((int)piStack_13a + 0x46) &&
          (*(uint *)(iVar11 + 0xee) < *(uint *)((int)piStack_13a + 0x44))))) {
        cVar5 = '\x01';
      }
      else {
        cVar5 = '\0';
      }
      FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x6684,
                    (int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                    *(undefined1 *)((*(char *)0x651f == '\0') * 2 + (int)cVar5 + 0xc),local_122,
                    unaff_SS,0xa1,0x6a);
      uStack_138 = (uint)((ulong)*(undefined4 *)0x6670 >> 0x10);
      iVar14 = (int)*(undefined4 *)0x6670;
      piStack_13a = (int *)(iVar14 + 0xaa);
      puVar19 = local_23a;
      uVar15 = unaff_SS;
      FUN_1ec2_00d0(*(undefined2 *)(iVar14 + 0xee),*(undefined2 *)(iVar14 + 0xf0));
      FUN_24dd_3eaf(0xff,local_122,unaff_SS,puVar19,uVar15);
      uVar15 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
      iVar11 = (int)*(undefined4 *)0x6670;
      iVar14 = *(int *)(iVar11 + 0x46);
      if ((iVar14 < *(int *)((int)piStack_13a + 0x46)) ||
         ((iVar14 <= *(int *)((int)piStack_13a + 0x46) &&
          (*(uint *)(iVar11 + 0x44) < *(uint *)((int)piStack_13a + 0x44))))) {
        cVar5 = '\x01';
      }
      else {
        cVar5 = '\0';
      }
      FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x6684,
                    (int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                    *(undefined1 *)((*(char *)0x651f == '\x01') * 2 + (int)cVar5 + 0xc),local_122,
                    unaff_SS,0xa1,0xbe);
    }
    if (((*(char *)((int)*(undefined4 *)0x6670 + (uint)*(byte *)0x651f * 0xaa + 0x9a) != '\0') &&
        (*(char *)((int)*(undefined4 *)0x6670 + (uint)(*(byte *)0x651f ^ 1) * 0xaa + 0x9a) != '\0'))
       && (*(uint *)0x6520 % 0x46 == 0)) {
      iVar11 = (int)*(uint *)0x66a1 >> 0xf;
      uVar15 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
      iVar13 = (int)*(undefined4 *)0x6670 + (uint)*(byte *)0x651f * 0xaa;
      iVar14 = *(int *)(iVar13 + 0x46);
      if ((iVar14 < iVar11) || ((iVar14 <= iVar11 && (*(uint *)(iVar13 + 0x44) < *(uint *)0x66a1))))
      {
        uVar15 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
        iVar14 = (int)*(undefined4 *)0x6670 + (uint)*(byte *)0x651f * 0xaa;
        puVar1 = (uint *)(iVar14 + 0x44);
        uVar9 = *puVar1;
        *puVar1 = *puVar1 + 1;
        piVar2 = (int *)(iVar14 + 0x46);
        *piVar2 = *piVar2 + (uint)(0xfffe < uVar9);
      }
    }
    goto LAB_1000_6dc3;
  }
  if ((cVar5 != '\x02') && (cVar5 != '\x03')) goto LAB_1000_6dc3;
  if (*(char *)0x6426 != '\0') {
    iVar14 = *(int *)0x2;
    iVar11 = iVar14 >> 0xf;
    FUN_24dd_3dbd();
    if (iVar14 == 0 && iVar11 == 0) {
      FUN_1ec2_0e8f((int)*(undefined4 *)0x6678 + 0x5000,(int)((ulong)*(undefined4 *)0x6678 >> 0x10),
                    (int)*(undefined4 *)0x6684,(int)((ulong)*(undefined4 *)0x6684 >> 0x10),0x10,0x10
                    ,(*(int *)0x642b - *(int *)0x67b4) + -7,(*(int *)0x6427 - *(int *)0x67b0) + -7);
      FUN_1ec2_0e8f((int)*(undefined4 *)0x6678 + 0x5000,(int)((ulong)*(undefined4 *)0x6678 >> 0x10),
                    (int)*(undefined4 *)0x6684 + 0xa0,(int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                    0x10,0x10,(*(int *)0x642b - *(int *)0x67b6) + -7,
                    (*(int *)0x6427 - *(int *)0x67b2) + -7);
      if (*(char *)0x66af != '\0') {
        FUN_1ec2_0f44((int)*(undefined4 *)0x6678 + 0x5000,
                      (int)((ulong)*(undefined4 *)0x6678 >> 0x10),(int)*(undefined4 *)0x6684,
                      (int)((ulong)*(undefined4 *)0x6684 >> 0x10),4,0xffa3,0xffa0,0x10,0x10,
                      (*(int *)0x642b - *(int *)0x67b4) + -4,(*(int *)0x6427 - *(int *)0x67b0) + -10
                     );
        FUN_1ec2_0f44((int)*(undefined4 *)0x6678 + 0x5000,
                      (int)((ulong)*(undefined4 *)0x6678 >> 0x10),(int)*(undefined4 *)0x6684 + 0xa0,
                      (int)((ulong)*(undefined4 *)0x6684 >> 0x10),4,0xffa3,0xffa0,0x10,0x10,
                      (*(int *)0x642b - *(int *)0x67b6) + -4,(*(int *)0x6427 - *(int *)0x67b2) + -10
                     );
      }
    }
    local_12e = (int *)0x0;
    local_12c = 0;
    local_4 = 0xfffb;
    do {
      if (*(int *)0x642b < 0x156) {
        iVar14 = 0x20;
        bVar7 = FUN_24dd_4161();
        if ((*(byte *)(iVar14 + 0x6604) & bVar7) != 0) goto LAB_1000_6a38;
      }
      else {
LAB_1000_6a38:
        bVar17 = (int *)0xfffe < local_12e;
        local_12e = (int *)((int)local_12e + 1);
        local_12c = local_12c + (uint)bVar17;
      }
      if (local_4 == 5) goto code_r0x00016a48;
      local_4 = local_4 + 1;
    } while( true );
  }
LAB_1000_6b1a:
  if (*(char *)0x6431 != '\0') {
    iVar14 = *(int *)0x2;
    iVar11 = iVar14 >> 0xf;
    FUN_24dd_3dbd();
    if (iVar14 == 0 && iVar11 == 0) {
      FUN_1ec2_0e8f((int)*(undefined4 *)0x6678 + 0x5100,(int)((ulong)*(undefined4 *)0x6678 >> 0x10),
                    (int)*(undefined4 *)0x6684,(int)((ulong)*(undefined4 *)0x6684 >> 0x10),0x10,0x10
                    ,(*(int *)0x6436 - *(int *)0x67b4) + -7,(*(int *)0x6432 - *(int *)0x67b0) + -7);
      FUN_1ec2_0e8f((int)*(undefined4 *)0x6678 + 0x5100,(int)((ulong)*(undefined4 *)0x6678 >> 0x10),
                    (int)*(undefined4 *)0x6684 + 0xa0,(int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                    0x10,0x10,(*(int *)0x6436 - *(int *)0x67b6) + -7,
                    (*(int *)0x6432 - *(int *)0x67b2) + -7);
      if (*(char *)0x66af != '\0') {
        FUN_1ec2_0f44((int)*(undefined4 *)0x6678 + 0x5100,
                      (int)((ulong)*(undefined4 *)0x6678 >> 0x10),(int)*(undefined4 *)0x6684,
                      (int)((ulong)*(undefined4 *)0x6684 >> 0x10),4,0xffa3,0xffa0,0x10,0x10,
                      (*(int *)0x6436 - *(int *)0x67b4) + -4,(*(int *)0x6432 - *(int *)0x67b0) + -10
                     );
        FUN_1ec2_0f44((int)*(undefined4 *)0x6678 + 0x5100,
                      (int)((ulong)*(undefined4 *)0x6678 >> 0x10),(int)*(undefined4 *)0x6684 + 0xa0,
                      (int)((ulong)*(undefined4 *)0x6684 >> 0x10),4,0xffa3,0xffa0,0x10,0x10,
                      (*(int *)0x6436 - *(int *)0x67b6) + -4,(*(int *)0x6432 - *(int *)0x67b2) + -10
                     );
      }
    }
    local_12e = (int *)0x0;
    local_12c = 0;
    local_4 = 0xfffb;
    do {
      if (*(int *)0x6436 < 0x156) {
        iVar14 = 0x20;
        bVar7 = FUN_24dd_4161();
        if ((*(byte *)(iVar14 + 0x6604) & bVar7) != 0) goto LAB_1000_6c65;
      }
      else {
LAB_1000_6c65:
        bVar17 = (int *)0xfffe < local_12e;
        local_12e = (int *)((int)local_12e + 1);
        local_12c = local_12c + (uint)bVar17;
      }
      if (local_4 == 5) goto code_r0x00016c75;
      local_4 = local_4 + 1;
    } while( true );
  }
LAB_1000_6d52:
  if (7 < (*(uint *)0x6520 & 0xf)) {
    if (*(char *)((int)*(undefined4 *)0x6670 + 0x95) != '\0') {
      FUN_1ec2_0e8f((int)*(undefined4 *)0x667c + (uint)*(byte *)0x65b * 0x31,
                    (int)((ulong)*(undefined4 *)0x667c >> 0x10),(int)*(undefined4 *)0x6684 + -0x3800
                    ,(int)((ulong)*(undefined4 *)0x6684 >> 0x10),7,7,1,0x6a);
    }
    if (*(char *)((int)*(undefined4 *)0x6670 + 0x13f) != '\0') {
      FUN_1ec2_0e8f((int)*(undefined4 *)0x667c + (uint)*(byte *)0x65a * 0x31,
                    (int)((ulong)*(undefined4 *)0x667c >> 0x10),(int)*(undefined4 *)0x6684 + -0x3760
                    ,(int)((ulong)*(undefined4 *)0x6684 >> 0x10),7,7,1,0x1e);
    }
  }
LAB_1000_6dc3:
  if (*(int *)((int)*(undefined4 *)0x6670 + 0x50) < 1) {
    uStack_138 = (uint)((ulong)*(undefined4 *)0x6670 >> 0x10);
    piStack_13a = (int *)*(undefined4 *)0x6670;
    iVar14 = *(int *)0x2;
    iVar11 = iVar14 >> 0xf;
    FUN_24dd_3dbd();
    if (iVar14 == 0 && iVar11 == 0) {
      FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x6684,
                    (int)((ulong)*(undefined4 *)0x6684 >> 0x10),0,
                    *(char *)((int)piStack_13a + 0x96) * 0x29 + 0x652e,unaff_DS,*(char *)0x652c + 1,
                    0xa3);
      FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x6684,
                    (int)((ulong)*(undefined4 *)0x6684 >> 0x10),0x32,
                    *(char *)((int)piStack_13a + 0x96) * 0x29 + 0x652e,unaff_DS,(int)*(char *)0x652c
                    ,0xa2);
      if ((*(char *)0x66ac == '\x01') && (*(char *)0x651e != '\0')) {
        FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x6684,
                      (int)((ulong)*(undefined4 *)0x6684 >> 0x10),0,0x5e55,0x1ec2,
                      *(char *)0x652c + 1,3);
        FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x6684,
                      (int)((ulong)*(undefined4 *)0x6684 >> 0x10),0x32,0x5e55,0x1ec2,
                      (int)*(char *)0x652c,2);
      }
    }
    if ((*(uint *)0x6520 & 1) == 0) {
      if (*(int *)((int)piStack_13a + 0x4c) < 0x11) {
        if (-8 < *(char *)0x652c) {
          *(char *)0x652c = *(char *)0x652c + -1;
        }
      }
      else if (*(char *)0x652c < '\x02') {
        *(char *)0x652c = *(char *)0x652c + '\x01';
      }
    }
  }
  if (*(int *)((int)*(undefined4 *)0x6670 + 0xfa) < 1) {
    uStack_138 = (uint)((ulong)*(undefined4 *)0x6670 >> 0x10);
    piStack_13a = (int *)((int)*(undefined4 *)0x6670 + 0xaa);
    iVar14 = *(int *)0x2;
    iVar11 = iVar14 >> 0xf;
    FUN_24dd_3dbd();
    if (iVar14 == 0 && iVar11 == 0) {
      FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x6684,
                    (int)((ulong)*(undefined4 *)0x6684 >> 0x10),0,
                    *(char *)((int)piStack_13a + 0x96) * 0x29 + 0x6580,unaff_DS,*(char *)0x652d + 1,
                    3);
      FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x6684,
                    (int)((ulong)*(undefined4 *)0x6684 >> 0x10),0x32,
                    *(char *)((int)piStack_13a + 0x96) * 0x29 + 0x6580,unaff_DS,(int)*(char *)0x652d
                    ,2);
      if ((*(char *)0x66ac == '\x01') && (*(char *)0x651e != '\0')) {
        FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x6684,
                      (int)((ulong)*(undefined4 *)0x6684 >> 0x10),0,0x5e55,0x1ec2,
                      *(char *)0x652d + 1,0xa3);
        FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x6684,
                      (int)((ulong)*(undefined4 *)0x6684 >> 0x10),0x32,0x5e55,0x1ec2,
                      (int)*(char *)0x652d,0xa2);
      }
    }
    if ((*(uint *)0x6520 & 1) == 0) {
      if (*(int *)((int)piStack_13a + 0x4c) < 0x11) {
        if (-8 < *(char *)0x652d) {
          *(char *)0x652d = *(char *)0x652d + -1;
        }
      }
      else if (*(char *)0x652d < '\x02') {
        *(char *)0x652d = *(char *)0x652d + '\x01';
      }
    }
  }
  uStack_138 = (uint)*(byte *)0x669c;
  if (uStack_138 != 0) {
    local_4 = 1;
    while( true ) {
      if (*(char *)((int)*(undefined4 *)0x6698 + local_4 * 0xe + -2) != '\0') {
        piStack_13a = (int *)((ulong)*(undefined4 *)0x6698 >> 0x10);
        local_13c = (int *)((int)*(undefined4 *)0x6698 + local_4 * 0xe + -0xe);
        iVar14 = *(int *)0x2;
        iVar11 = iVar14 >> 0xf;
        FUN_24dd_3dbd();
        if ((iVar14 == 0 && iVar11 == 0) &&
           ((0xdc < (uint)local_13c[5] ||
            (((uint)local_13c[5] < 0xdd && (1 < (*(uint *)0x6520 & 3))))))) {
          FUN_1ec2_0e8f((int)*(undefined4 *)0x667c +
                        (uint)*(byte *)(*(byte *)(local_13c + 6) + 0x135d) * 0x31,
                        (int)((ulong)*(undefined4 *)0x667c >> 0x10),(int)*(undefined4 *)0x6684,
                        (int)((ulong)*(undefined4 *)0x6684 >> 0x10),7,7,
                        (local_13c[2] - *(int *)0x67b4) + -3,
                        (*(int *)CONCAT22(piStack_13a,local_13c) - *(int *)0x67b0) + -3);
          FUN_1ec2_0e8f((int)*(undefined4 *)0x667c +
                        (uint)*(byte *)(*(byte *)(local_13c + 6) + 0x135d) * 0x31,
                        (int)((ulong)*(undefined4 *)0x667c >> 0x10),
                        (int)*(undefined4 *)0x6684 + 0xa0,
                        (int)((ulong)*(undefined4 *)0x6684 >> 0x10),7,7,
                        (local_13c[2] - *(int *)0x67b6) + -3,
                        (*(int *)CONCAT22(piStack_13a,local_13c) - *(int *)0x67b2) + -3);
          if (*(char *)0x66af != '\0') {
            FUN_1ec2_0f44((int)*(undefined4 *)0x667c +
                          (uint)*(byte *)(*(byte *)(local_13c + 6) + 0x135d) * 0x31,
                          (int)((ulong)*(undefined4 *)0x667c >> 0x10),(int)*(undefined4 *)0x6684,
                          (int)((ulong)*(undefined4 *)0x6684 >> 0x10),4,0xffa3,0xffa0,7,7,
                          local_13c[2] - *(int *)0x67b4,
                          (*(int *)CONCAT22(piStack_13a,local_13c) - *(int *)0x67b0) + -5);
            FUN_1ec2_0f44((int)*(undefined4 *)0x667c +
                          (uint)*(byte *)(*(byte *)(local_13c + 6) + 0x135d) * 0x31,
                          (int)((ulong)*(undefined4 *)0x667c >> 0x10),
                          (int)*(undefined4 *)0x6684 + 0xa0,
                          (int)((ulong)*(undefined4 *)0x6684 >> 0x10),4,0xffa3,0xffa0,7,7,
                          local_13c[2] - *(int *)0x67b6,
                          (*(int *)CONCAT22(piStack_13a,local_13c) - *(int *)0x67b2) + -5);
          }
          if ((char)local_13c[6] == '\x01') {
            local_12e = (int *)(uint)*(byte *)((uint)*(byte *)((int)local_13c + 0xd) * 0xe + 0x7e8);
            local_12c = 0;
            FUN_24dd_3eaf(0xff,local_122,unaff_SS,
                          (uint)*(byte *)((int)local_13c + 0xd) * 0xe + 0x7e8,unaff_DS);
            if ((*(char *)0x66ad != '\0') && (local_13e = local_12e, 0 < (int)local_12e)) {
              local_6 = (int *)0x1;
              while( true ) {
                if (local_122[(int)local_6] != 0x20) {
                  iVar14 = FUN_24dd_3e7c();
                  FUN_1ec2_0e8f((int)*(undefined4 *)0x6680 + (local_122[(int)local_6] - 0x41) * 0x10
                                ,(int)((ulong)*(undefined4 *)0x6680 >> 0x10),
                                (int)*(undefined4 *)0x6684,
                                (int)((ulong)*(undefined4 *)0x6684 >> 0x10),4,4,
                                (local_13c[2] - *(int *)0x67b4) + -10,
                                (int)local_6 * 4 +
                                ((*(int *)CONCAT22(piStack_13a,local_13c) - *(int *)0x67b0) - iVar14
                                ) + -2);
                  iVar14 = FUN_24dd_3e7c();
                  FUN_1ec2_0e8f((int)*(undefined4 *)0x6680 + (local_122[(int)local_6] - 0x41) * 0x10
                                ,(int)((ulong)*(undefined4 *)0x6680 >> 0x10),
                                (int)*(undefined4 *)0x6684 + 0xa0,
                                (int)((ulong)*(undefined4 *)0x6684 >> 0x10),4,4,
                                (local_13c[2] - *(int *)0x67b6) + -10,
                                (int)local_6 * 4 +
                                ((*(int *)CONCAT22(piStack_13a,local_13c) - *(int *)0x67b2) - iVar14
                                ) + -2);
                }
                if (local_6 == local_13e) break;
                local_6 = (int *)((int)local_6 + 1);
              }
            }
          }
        }
        FUN_1000_5aef(local_4);
      }
      if (local_4 == uStack_138) break;
      local_4 = local_4 + 1;
    }
  }
  local_4 = 0;
  while( true ) {
    if (*(char *)((int)*(undefined4 *)0x668c + local_4 * 7 + 4) != '\0') {
      uStack_138 = (uint)((ulong)*(undefined4 *)0x668c >> 0x10);
      piStack_13a = (int *)((int)*(undefined4 *)0x668c + local_4 * 7);
      local_128 = *(byte *)(piStack_13a + 2) & 0x7f;
      iVar14 = *(int *)0x2;
      iVar11 = iVar14 >> 0xf;
      FUN_24dd_3dbd();
      if (iVar14 == 0 && iVar11 == 0) {
        FUN_1ec2_1008((int)*(undefined4 *)0x6678 +
                      ((uint)*(byte *)(local_128 + 0x13bb) + (int)*(char *)((int)piStack_13a + 5)) *
                      0x100,(int)((ulong)*(undefined4 *)0x6678 >> 0x10),(int)*(undefined4 *)0x6684,
                      (int)((ulong)*(undefined4 *)0x6684 >> 0x10),0xffa7,0xffa0,0x10,0x10,
                      piStack_13a[1] - *(int *)0x67b4,
                      *(int *)CONCAT22(uStack_138,piStack_13a) - *(int *)0x67b0);
        FUN_1ec2_1008((int)*(undefined4 *)0x6678 +
                      ((uint)*(byte *)(local_128 + 0x13bb) + (int)*(char *)((int)piStack_13a + 5)) *
                      0x100,(int)((ulong)*(undefined4 *)0x6678 >> 0x10),
                      (int)*(undefined4 *)0x6684 + 0xa0,(int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                      0xffa7,0xffa0,0x10,0x10,piStack_13a[1] - *(int *)0x67b6,
                      *(int *)CONCAT22(uStack_138,piStack_13a) - *(int *)0x67b2);
        if ((*(char *)0x66af != '\0') && (*(char *)(local_128 + 0x1427) == '\0')) {
          FUN_1ec2_0f44((int)*(undefined4 *)0x6678 +
                        ((uint)*(byte *)(local_128 + 0x13bb) + (int)*(char *)((int)piStack_13a + 5))
                        * 0x100,(int)((ulong)*(undefined4 *)0x6678 >> 0x10),
                        (int)*(undefined4 *)0x6684,(int)((ulong)*(undefined4 *)0x6684 >> 0x10),4,
                        0xffa3,0xffa0,0x10,0x10,(piStack_13a[1] - *(int *)0x67b4) + 3,
                        (*(int *)CONCAT22(uStack_138,piStack_13a) - *(int *)0x67b0) + -3);
          FUN_1ec2_0f44((int)*(undefined4 *)0x6678 +
                        ((uint)*(byte *)(local_128 + 0x13bb) + (int)*(char *)((int)piStack_13a + 5))
                        * 0x100,(int)((ulong)*(undefined4 *)0x6678 >> 0x10),
                        (int)*(undefined4 *)0x6684 + 0xa0,
                        (int)((ulong)*(undefined4 *)0x6684 >> 0x10),4,0xffa3,0xffa0,0x10,0x10,
                        (piStack_13a[1] - *(int *)0x67b6) + 3,
                        (*(int *)CONCAT22(uStack_138,piStack_13a) - *(int *)0x67b2) + -3);
        }
      }
      *(char *)(piStack_13a + 3) = (char)piStack_13a[3] + -1;
      if ((char)piStack_13a[3] < '\0') {
        *(undefined1 *)(piStack_13a + 3) = *(undefined1 *)(local_128 + 0x13ad);
        *(char *)((int)piStack_13a + 5) = *(char *)((int)piStack_13a + 5) + '\x01';
        if ((int)(uint)*(byte *)(local_128 + 0x13c9) < (int)*(char *)((int)piStack_13a + 5)) {
          *(undefined1 *)(piStack_13a + 2) = 0;
        }
      }
    }
    if (local_4 == 700) break;
    local_4 = local_4 + 1;
  }
  local_4 = 0;
  while( true ) {
    if (*(char *)((int)*(undefined4 *)0x6688 + local_4 * 0x14 + 0x10) != '\0') {
      uStack_138 = (uint)((ulong)*(undefined4 *)0x6688 >> 0x10);
      piStack_13a = (int *)((int)*(undefined4 *)0x6688 + local_4 * 0x14);
      local_128 = *(byte *)((int)piStack_13a + 0x10) & 0x7f;
      iVar14 = *(int *)0x2;
      iVar11 = iVar14 >> 0xf;
      FUN_24dd_3dbd();
      if (iVar14 == 0 && iVar11 == 0) {
        if (*(uint *)((uint)local_128 * 2 + 0x1104) < 0x8000) {
          local_6 = (int *)(uint)*(byte *)((int)piStack_13a + 0x11);
          if (*(char *)(local_128 + 0x11a5) == '\x02') {
            local_6 = (int *)((uint)(local_6 + 2) / 8);
            if ((int *)0xf < local_6) {
              local_6 = local_6 + -8;
            }
          }
          else if (*(char *)(local_128 + 0x11a5) == '\x03') {
            if ((int *)0x40 < local_6) {
              local_6 = (int *)((int)local_6 + -1);
            }
            local_6 = (int *)((int)(local_6 + -6) / 8);
            if ((int)local_6 < 0) {
              local_6 = (int *)0x0;
            }
            if (0xc < (int)local_6) {
              local_6 = (int *)0xc;
            }
          }
          local_8 = *(int *)((int)piStack_13a + 2) + -3;
          if ((*(char *)0x66af != '\0') && (*(char *)(local_128 + 0xb15) == '\x01')) {
            FUN_1ec2_0f44((int)*(undefined4 *)0x667c +
                          (*(int *)((uint)local_128 * 2 + 0x1104) + (int)local_6) * 0x31,
                          (int)((ulong)*(undefined4 *)0x667c >> 0x10),(int)*(undefined4 *)0x6684,
                          (int)((ulong)*(undefined4 *)0x6684 >> 0x10),4,0xffa3,0xffa0,7,7,
                          *(int *)((int)piStack_13a + 6) - *(int *)0x67b4,
                          (local_8 - *(int *)0x67b0) + -3);
            FUN_1ec2_0f44((int)*(undefined4 *)0x667c +
                          (*(int *)((uint)local_128 * 2 + 0x1104) + (int)local_6) * 0x31,
                          (int)((ulong)*(undefined4 *)0x667c >> 0x10),
                          (int)*(undefined4 *)0x6684 + 0xa0,
                          (int)((ulong)*(undefined4 *)0x6684 >> 0x10),4,0xffa3,0xffa0,7,7,
                          *(int *)((int)piStack_13a + 6) - *(int *)0x67b6,
                          (local_8 - *(int *)0x67b2) + -3);
          }
          local_a = *(int *)((int)piStack_13a + 6) + -3;
          FUN_1ec2_0e8f((int)*(undefined4 *)0x667c +
                        (*(int *)((uint)local_128 * 2 + 0x1104) + (int)local_6) * 0x31,
                        (int)((ulong)*(undefined4 *)0x667c >> 0x10),(int)*(undefined4 *)0x6684,
                        (int)((ulong)*(undefined4 *)0x6684 >> 0x10),7,7,local_a - *(int *)0x67b4,
                        local_8 - *(int *)0x67b0);
          FUN_1ec2_0e8f((int)*(undefined4 *)0x667c +
                        (*(int *)((uint)local_128 * 2 + 0x1104) + (int)local_6) * 0x31,
                        (int)((ulong)*(undefined4 *)0x667c >> 0x10),
                        (int)*(undefined4 *)0x6684 + 0xa0,
                        (int)((ulong)*(undefined4 *)0x6684 >> 0x10),7,7,local_a - *(int *)0x67b6,
                        local_8 - *(int *)0x67b2);
        }
        else if (*(char *)((int)piStack_13a + 0x11) != '\0') {
          iVar14 = *(int *)((int)piStack_13a + 6) - *(int *)0x67b4;
          FUN_1ec2_0dc8((int)*(undefined4 *)0x6684,(int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                        CONCAT11((char)((uint)iVar14 >> 8),*(undefined1 *)((int)piStack_13a + 0x11))
                        ,iVar14,*(int *)((int)piStack_13a + 2) - *(int *)0x67b0);
          iVar14 = *(int *)((int)piStack_13a + 6) - *(int *)0x67b6;
          FUN_1ec2_0dc8((int)*(undefined4 *)0x6684 + 0xa0,
                        (int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                        CONCAT11((char)((uint)iVar14 >> 8),*(undefined1 *)((int)piStack_13a + 0x11))
                        ,iVar14,*(int *)((int)piStack_13a + 2) - *(int *)0x67b2);
          if ((*(char *)0x66af != '\0') && (*(char *)(local_128 + 0xb15) == '\x01')) {
            FUN_1ec2_0e4a((int)*(undefined4 *)0x6684,(int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                          (*(int *)((int)piStack_13a + 6) - *(int *)0x67b4) + 3,
                          (*(int *)((int)piStack_13a + 2) - *(int *)0x67b0) + -3);
            FUN_1ec2_0e4a((int)*(undefined4 *)0x6684 + 0xa0,
                          (int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                          (*(int *)((int)piStack_13a + 6) - *(int *)0x67b6) + 3,
                          (*(int *)((int)piStack_13a + 2) - *(int *)0x67b2) + -3);
          }
        }
        if ((local_128 == 0x23) && (*(char *)((int)piStack_13a + 0x11) == '\0')) {
          uVar9 = (int)local_4 % 0x28 + 1;
          local_129 = (undefined1)uVar9;
          local_12e = (int *)(uint)*(byte *)((uVar9 & 0xff) * 0xe + 0x7e8);
          local_12c = 0;
          FUN_24dd_3eaf(0xff,local_122,unaff_SS,(uVar9 & 0xff) * 0xe + 0x7e8,unaff_DS);
          if ((*(char *)0x66ad != '\0') && (local_13c = local_12e, 0 < (int)local_12e)) {
            local_6 = (int *)0x1;
            while( true ) {
              if (local_122[(int)local_6] != 0x20) {
                iVar14 = FUN_24dd_3e7c();
                FUN_1ec2_0e8f((int)*(undefined4 *)0x6680 + (local_122[(int)local_6] - 0x41) * 0x10,
                              (int)((ulong)*(undefined4 *)0x6680 >> 0x10),(int)*(undefined4 *)0x6684
                              ,(int)((ulong)*(undefined4 *)0x6684 >> 0x10),4,4,
                              (*(int *)((int)piStack_13a + 6) - *(int *)0x67b4) + -10,
                              (int)local_6 * 4 +
                              ((*(int *)((int)piStack_13a + 2) - *(int *)0x67b0) - iVar14) + -2);
                iVar14 = FUN_24dd_3e7c();
                FUN_1ec2_0e8f((int)*(undefined4 *)0x6680 + (local_122[(int)local_6] - 0x41) * 0x10,
                              (int)((ulong)*(undefined4 *)0x6680 >> 0x10),
                              (int)*(undefined4 *)0x6684 + 0xa0,
                              (int)((ulong)*(undefined4 *)0x6684 >> 0x10),4,4,
                              (*(int *)((int)piStack_13a + 6) - *(int *)0x67b6) + -10,
                              (int)local_6 * 4 +
                              ((*(int *)((int)piStack_13a + 2) - *(int *)0x67b2) - iVar14) + -2);
              }
              if (local_6 == local_13c) break;
              local_6 = (int *)((int)local_6 + 1);
            }
          }
        }
      }
      FUN_1000_4964(local_4);
    }
    if (local_4 == 600) break;
    local_4 = local_4 + 1;
  }
  local_4 = 0;
  while( true ) {
    if (*(char *)((int)*(undefined4 *)0x6694 + local_4 * 0x14 + 0x12) != '\0') {
      uStack_138 = (uint)((ulong)*(undefined4 *)0x6694 >> 0x10);
      piStack_13a = (int *)((int)*(undefined4 *)0x6694 + local_4 * 0x14);
      iVar14 = *(int *)0x2;
      iVar11 = iVar14 >> 0xf;
      FUN_24dd_3dbd();
      if (iVar14 == 0 && iVar11 == 0) {
        local_128 = *(byte *)((int)piStack_13a + 0x12) & 0x7f;
        if (*(char *)(local_128 + 0x645) == '\0') {
          if (1 < *(byte *)((int)piStack_13a + 0x13)) {
            iVar14 = *(int *)((int)piStack_13a + 6) - *(int *)0x67b4;
            FUN_1ec2_0dc8((int)*(undefined4 *)0x6684,(int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                          CONCAT11((char)((uint)iVar14 >> 8),
                                   *(undefined1 *)((int)piStack_13a + 0x13)),iVar14,
                          *(int *)((int)piStack_13a + 2) - *(int *)0x67b0);
            iVar14 = *(int *)((int)piStack_13a + 6) - *(int *)0x67b6;
            FUN_1ec2_0dc8((int)*(undefined4 *)0x6684 + 0xa0,
                          (int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                          CONCAT11((char)((uint)iVar14 >> 8),
                                   *(undefined1 *)((int)piStack_13a + 0x13)),iVar14,
                          *(int *)((int)piStack_13a + 2) - *(int *)0x67b2);
            if (*(char *)0x66af != '\0') {
              FUN_1ec2_0e4a((int)*(undefined4 *)0x6684,(int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                            (*(int *)((int)piStack_13a + 6) - *(int *)0x67b4) + 3,
                            (*(int *)((int)piStack_13a + 2) - *(int *)0x67b0) + -3);
              FUN_1ec2_0e4a((int)*(undefined4 *)0x6684 + 0xa0,
                            (int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                            (*(int *)((int)piStack_13a + 6) - *(int *)0x67b6) + 3,
                            (*(int *)((int)piStack_13a + 2) - *(int *)0x67b2) + -3);
            }
          }
        }
        else {
          local_8 = *(int *)((int)piStack_13a + 2) + -3;
          local_a = *(int *)((int)piStack_13a + 6) + -3;
          if ((0x14 < local_128) && (local_128 < 0x17)) {
            local_a = *(int *)((int)piStack_13a + 6) + -5;
            local_8 = *(int *)((int)piStack_13a + 2);
          }
          if (*(char *)0x66af != '\0') {
            FUN_1ec2_0f44((int)*(undefined4 *)0x667c +
                          ((uint)*(byte *)(local_128 + 0x645) +
                          (uint)*(byte *)((int)piStack_13a + 0x13)) * 0x31,
                          (int)((ulong)*(undefined4 *)0x667c >> 0x10),(int)*(undefined4 *)0x6684,
                          (int)((ulong)*(undefined4 *)0x6684 >> 0x10),4,0xffa3,0xffa0,7,7,
                          *(int *)((int)piStack_13a + 6) - *(int *)0x67b4,
                          (local_8 - *(int *)0x67b0) + -3);
            FUN_1ec2_0f44((int)*(undefined4 *)0x667c +
                          ((uint)*(byte *)(local_128 + 0x645) +
                          (uint)*(byte *)((int)piStack_13a + 0x13)) * 0x31,
                          (int)((ulong)*(undefined4 *)0x667c >> 0x10),
                          (int)*(undefined4 *)0x6684 + 0xa0,
                          (int)((ulong)*(undefined4 *)0x6684 >> 0x10),4,0xffa3,0xffa0,7,7,
                          *(int *)((int)piStack_13a + 6) - *(int *)0x67b6,
                          (local_8 - *(int *)0x67b2) + -3);
          }
          FUN_1ec2_0e8f((int)*(undefined4 *)0x667c +
                        ((uint)*(byte *)(local_128 + 0x645) +
                        (uint)*(byte *)((int)piStack_13a + 0x13)) * 0x31,
                        (int)((ulong)*(undefined4 *)0x667c >> 0x10),(int)*(undefined4 *)0x6684,
                        (int)((ulong)*(undefined4 *)0x6684 >> 0x10),7,7,local_a - *(int *)0x67b4,
                        local_8 - *(int *)0x67b0);
          FUN_1ec2_0e8f((int)*(undefined4 *)0x667c +
                        ((uint)*(byte *)(local_128 + 0x645) +
                        (uint)*(byte *)((int)piStack_13a + 0x13)) * 0x31,
                        (int)((ulong)*(undefined4 *)0x667c >> 0x10),
                        (int)*(undefined4 *)0x6684 + 0xa0,
                        (int)((ulong)*(undefined4 *)0x6684 >> 0x10),7,7,local_a - *(int *)0x67b6,
                        local_8 - *(int *)0x67b2);
        }
      }
      FUN_1000_3d39(local_4);
    }
    if (local_4 == 600) break;
    local_4 = local_4 + 1;
  }
  local_4 = 0;
  while( true ) {
    uStack_138 = (uint)((ulong)*(undefined4 *)0x6670 >> 0x10);
    piStack_13a = (int *)((int)*(undefined4 *)0x6670 + local_4 * 0xaa);
    auStack_1a[local_4 * 2 + 5] = piStack_13a[3] - 1;
    auStack_1a[local_4 * 2 + 1] = piStack_13a[5] - 2;
    auStack_1a[local_4 * 2 + 4] = 0;
    auStack_1a[local_4 * 2] = 0;
    auStack_1a[local_4 * 2 + 5] = auStack_1a[local_4 * 2 + 5] - *(int *)(local_4 * 2 + 0x67b0);
    auStack_1a[local_4 * 2 + 1] = auStack_1a[local_4 * 2 + 1] - *(int *)(local_4 * 2 + 0x67b4);
    iVar14 = *(int *)(piStack_13a[0x2b] * 8 + 0x15a0);
    uVar10 = FUN_24dd_3e7c();
    uVar3 = local_4;
    puVar1 = auStack_1a + local_4 * 2 + 4;
    uVar9 = *puVar1;
    *puVar1 = *puVar1 + uVar10;
    auStack_1a[uVar3 * 2 + 5] = auStack_1a[uVar3 * 2 + 5] + iVar14 + (uint)CARRY2(uVar9,uVar10);
    iVar14 = *(int *)(piStack_13a[0x2b] * 8 + 0x15a4);
    uVar10 = FUN_24dd_3e7c();
    uVar3 = local_4;
    puVar1 = auStack_1a + local_4 * 2;
    uVar9 = *puVar1;
    *puVar1 = *puVar1 + uVar10;
    auStack_1a[uVar3 * 2 + 1] = auStack_1a[uVar3 * 2 + 1] + iVar14 + (uint)CARRY2(uVar9,uVar10);
    if (local_4 == 1) break;
    local_4 = local_4 + 1;
  }
  iVar14 = *(int *)0x2;
  iVar11 = iVar14 >> 0xf;
  FUN_24dd_3dbd();
  if (iVar14 == 0 && iVar11 == 0) {
    local_4 = 1;
    while( true ) {
      uStack_138 = (uint)((ulong)*(undefined4 *)0x6670 >> 0x10);
      piStack_13a = (int *)((int)*(undefined4 *)0x6670 + local_4 * 0xaa);
      if ((char)piStack_13a[0x4d] != '\0') {
        local_8 = (piStack_13a[3] - *(int *)0x67b0) + -7;
        local_a = (piStack_13a[5] - *(int *)0x67b4) + -5;
        local_12e = (int *)(piStack_13a[0x2b] - 0xc);
        local_12c = (int)local_12e >> 0xf;
        if (*(char *)((int)piStack_13a + 0x9b) != '\0') {
          bVar17 = local_12e < 0x31;
          local_12e = (int *)(piStack_13a[0x2b] - 0x3d);
          local_12c = local_12c - (uint)bVar17;
        }
        local_12e = (int *)FUN_24dd_3dbd();
        if (local_12c < 0) {
          local_12e = (int *)0x0;
          local_12c = 0;
        }
        if ((0 < local_12c) || ((-1 < local_12c && ((int *)0x6 < local_12e)))) {
          local_12e = (int *)0x6;
          local_12c = 0;
        }
        if (*(char *)((int)piStack_13a + 0x9b) != '\0') {
          bVar17 = (int *)0x6 < local_12e;
          local_12e = (int *)(6 - (int)local_12e);
          local_12c = -(uint)bVar17 - local_12c;
        }
        if (*(char *)((int)piStack_13a + piStack_13a[0x27] + 0x6f) != '\0') {
          if (*(char *)(*(int *)((int)piStack_13a + piStack_13a[0x27] * 2 + 0x73) + 0xb3d) == '\x01'
             ) {
            local_132 = *(int *)CONCAT22(uStack_138,piStack_13a) - *(int *)0x67b0;
            local_130 = (int)local_132 >> 0xf;
            local_136 = piStack_13a[1] - *(int *)0x67b4;
            local_134 = (int)local_136 >> 0xf;
            FUN_1ec2_0895((int)*(undefined4 *)0x6684,(int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                          local_a + 4,local_8 + 7,local_136,local_132);
          }
          if ((*(int *)((int)piStack_13a + piStack_13a[0x27] * 2 + 0x73) == 0x1d) &&
             (*(char *)(*(byte *)(local_4 * 7 + 0x6724) + 0x783b) != '\0')) {
            local_132 = *(int *)CONCAT22(uStack_138,piStack_13a) - *(int *)0x67b0;
            local_130 = (int)local_132 >> 0xf;
            local_136 = piStack_13a[1] - *(int *)0x67b4;
            local_134 = (int)local_136 >> 0xf;
            FUN_1ec2_0b0d((int)*(undefined4 *)0x6684,(int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                          CONCAT11((char)((uint)(piStack_13a[0x27] * 2) >> 8),
                                   *(undefined1 *)
                                    (*(int *)((int)piStack_13a + piStack_13a[0x27] * 2 + 0x73) +
                                    0x11cd)),local_a + 4,local_8 + 7,local_136,local_132);
          }
        }
        if ((char)piStack_13a[0x4e] != '\0') {
          local_132 = piStack_13a[8] - *(int *)0x67b0;
          local_130 = (int)local_132 >> 0xf;
          local_136 = piStack_13a[10] - *(int *)0x67b4;
          local_134 = (int)local_136 >> 0xf;
          FUN_1ec2_0c3b((int)*(undefined4 *)0x6684,(int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                        local_a + 4,local_8 + 7,local_136,local_132);
          FUN_1ec2_0e8f((int)*(undefined4 *)0x6678 + 0x5400,
                        (int)((ulong)*(undefined4 *)0x6678 >> 0x10),(int)*(undefined4 *)0x6684,
                        (int)((ulong)*(undefined4 *)0x6684 >> 0x10),3,0x10,local_136 - 1,
                        local_132 - 1);
          if (*(char *)0x66af != '\0') {
            FUN_1ec2_09e7((int)*(undefined4 *)0x6684,(int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                          local_a + 7,local_8 + 4,local_136 + 3,local_132 - 3);
            FUN_1ec2_0f44((int)*(undefined4 *)0x6678 + 0x5400,
                          (int)((ulong)*(undefined4 *)0x6678 >> 0x10),(int)*(undefined4 *)0x6684,
                          (int)((ulong)*(undefined4 *)0x6684 >> 0x10),4,0xffa3,0xffa0,3,0x10,
                          local_136 + 2,local_132 - 4);
          }
        }
        if ((*(char *)(*(int *)((int)piStack_13a + piStack_13a[0x27] * 2 + 0x73) + 0xf75) != '\0')
           && (*(char *)((int)piStack_13a + 0x99) != '\0')) {
          FUN_1ec2_0386(piStack_13a[0x24] / 2,
                        CONCAT11((char)((int)local_12e + 9),*(undefined1 *)((int)piStack_13a + 0x9b)
                                ),(int)*(undefined4 *)0x6684,
                        (int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                        (int)*(undefined4 *)0x6678 + ((int)local_12e + 9) * 0x100,
                        (int)((ulong)*(undefined4 *)0x6678 >> 0x10),
                        *(char *)((int)local_12e + *(char *)((int)piStack_13a + 0x9b) * 0xe + 0x1f1)
                        + local_a,
                        (char)local_12e[*(char *)((int)piStack_13a + 0x9b) * 7 + 0xf5] + local_8);
        }
        if (*(char *)((int)piStack_13a + 0x9d) == '\0') {
          *(undefined1 *)((int)piStack_13a + 0xa1) = (char)(*(int *)0x1c + (int)local_12e);
          bVar7 = *(byte *)((int)piStack_13a + 0xa1);
          FUN_1ec2_01df(CONCAT11(bVar7,(undefined1)local_4),
                        CONCAT11(bVar7,*(undefined1 *)((int)piStack_13a + 0x9b)),
                        (int)*(undefined4 *)0x6684,(int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                        (int)*(undefined4 *)0x6678 + (uint)bVar7 * 0x100,
                        (int)((ulong)*(undefined4 *)0x6678 >> 0x10),local_a,local_8);
          if (*(char *)0x66af != '\0') {
            FUN_1ec2_0734(CONCAT11(*(byte *)((int)piStack_13a + 0xa1),
                                   *(undefined1 *)((int)piStack_13a + 0x9b)),
                          (int)*(undefined4 *)0x6684,(int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                          (int)*(undefined4 *)0x6678 +
                          (uint)*(byte *)((int)piStack_13a + 0xa1) * 0x100,
                          (int)((ulong)*(undefined4 *)0x6678 >> 0x10),local_a + 3,local_8 + -3);
          }
        }
        else {
          *(undefined1 *)((int)piStack_13a + 0xa1) =
               (char)(*(int *)(((*(uint *)0x6520 & 0x1f) >> 3) * 2 + 0x1c) + (int)local_12e);
          bVar7 = *(byte *)((int)piStack_13a + 0xa1);
          FUN_1ec2_01df(CONCAT11(bVar7,(undefined1)local_4),
                        CONCAT11(bVar7,*(undefined1 *)((int)piStack_13a + 0x9b)),
                        (int)*(undefined4 *)0x6684,(int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                        (int)*(undefined4 *)0x6678 + (uint)bVar7 * 0x100,
                        (int)((ulong)*(undefined4 *)0x6678 >> 0x10),local_a,local_8);
          if (*(char *)0x66af != '\0') {
            FUN_1ec2_0734(CONCAT11(*(byte *)((int)piStack_13a + 0xa1),
                                   *(undefined1 *)((int)piStack_13a + 0x9b)),
                          (int)*(undefined4 *)0x6684,(int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                          (int)*(undefined4 *)0x6678 +
                          (uint)*(byte *)((int)piStack_13a + 0xa1) * 0x100,
                          (int)((ulong)*(undefined4 *)0x6678 >> 0x10),local_a + 3,local_8 + -3);
          }
        }
      }
      if (local_4 == 0) break;
      local_4 = local_4 + -1;
    }
    if (*(char *)((int)*(undefined4 *)0x6670 + 0x9a) != '\0') {
      uStack_138 = (uint)((ulong)*(undefined4 *)0x6670 >> 0x10);
      piStack_13a = (int *)*(undefined4 *)0x6670;
      if (*(char *)((int)piStack_13a + 0x97) == '\0') {
        FUN_1ec2_0e8f((int)*(undefined4 *)0x667c + 0x83b,(int)((ulong)*(undefined4 *)0x667c >> 0x10)
                      ,(int)*(undefined4 *)0x6684,(int)((ulong)*(undefined4 *)0x6684 >> 0x10),3,7,
                      auStack_1a[1],local_10);
      }
      else {
        FUN_1ec2_0e8f((int)*(undefined4 *)0x667c + 0x86c,(int)((ulong)*(undefined4 *)0x667c >> 0x10)
                      ,(int)*(undefined4 *)0x6684,(int)((ulong)*(undefined4 *)0x6684 >> 0x10),3,7,
                      auStack_1a[1],local_10);
      }
      if (*(char *)(*(byte *)0x6725 + 0x783b) != '\0') {
        local_12e = (int *)(uint)*(byte *)(*(int *)((int)piStack_13a +
                                                    *(int *)((int)piStack_13a + 0x4e) * 2 + 0x73) *
                                           0xe + 0x7e8);
        local_12c = 0;
        FUN_24dd_3eaf(0xff,local_122,unaff_SS,
                      *(int *)((int)piStack_13a + *(int *)((int)piStack_13a + 0x4e) * 2 + 0x73) *
                      0xe + 0x7e8,unaff_DS);
        local_13c = local_12e;
        if (0 < (int)local_12e) {
          local_6 = (int *)0x1;
          while( true ) {
            if (local_122[(int)local_6] != 0x20) {
              iVar14 = FUN_24dd_3e7c();
              FUN_1ec2_0e8f((int)*(undefined4 *)0x6680 + (local_122[(int)local_6] - 0x41) * 0x10,
                            (int)((ulong)*(undefined4 *)0x6680 >> 0x10),(int)*(undefined4 *)0x6684,
                            (int)((ulong)*(undefined4 *)0x6684 >> 0x10),4,4,local_a + -5,
                            (int)local_6 * 4 + (local_8 - iVar14) + 4);
            }
            if (local_6 == local_13c) break;
            local_6 = (int *)((int)local_6 + 1);
          }
        }
      }
    }
    local_4 = 0;
    while( true ) {
      uStack_138 = (uint)((ulong)*(undefined4 *)0x6670 >> 0x10);
      piStack_13a = (int *)((int)*(undefined4 *)0x6670 + local_4 * 0xaa);
      if ((char)piStack_13a[0x4d] != '\0') {
        local_8 = (piStack_13a[3] - *(int *)0x67b2) + -7;
        local_a = (piStack_13a[5] - *(int *)0x67b6) + -5;
        local_12e = (int *)(piStack_13a[0x2b] - 0xc);
        local_12c = (int)local_12e >> 0xf;
        if (*(char *)((int)piStack_13a + 0x9b) != '\0') {
          bVar17 = local_12e < 0x31;
          local_12e = (int *)(piStack_13a[0x2b] - 0x3d);
          local_12c = local_12c - (uint)bVar17;
        }
        local_12e = (int *)FUN_24dd_3dbd();
        if (local_12c < 0) {
          local_12e = (int *)0x0;
          local_12c = 0;
        }
        if ((0 < local_12c) || ((-1 < local_12c && ((int *)0x6 < local_12e)))) {
          local_12e = (int *)0x6;
          local_12c = 0;
        }
        if (*(char *)((int)piStack_13a + 0x9b) != '\0') {
          bVar17 = (int *)0x6 < local_12e;
          local_12e = (int *)(6 - (int)local_12e);
          local_12c = -(uint)bVar17 - local_12c;
        }
        if (*(char *)((int)piStack_13a + piStack_13a[0x27] + 0x6f) != '\0') {
          if (*(char *)(*(int *)((int)piStack_13a + piStack_13a[0x27] * 2 + 0x73) + 0xb3d) == '\x01'
             ) {
            local_132 = *(int *)CONCAT22(uStack_138,piStack_13a) - *(int *)0x67b2;
            local_130 = (int)local_132 >> 0xf;
            local_136 = piStack_13a[1] - *(int *)0x67b6;
            local_134 = (int)local_136 >> 0xf;
            FUN_1ec2_0895((int)*(undefined4 *)0x6684 + 0xa0,
                          (int)((ulong)*(undefined4 *)0x6684 >> 0x10),local_a + 4,local_8 + 7,
                          local_136,local_132);
          }
          if ((*(int *)((int)piStack_13a + piStack_13a[0x27] * 2 + 0x73) == 0x1d) &&
             (*(char *)(*(byte *)(local_4 * 7 + 0x6724) + 0x783b) != '\0')) {
            local_132 = *(int *)CONCAT22(uStack_138,piStack_13a) - *(int *)0x67b2;
            local_130 = (int)local_132 >> 0xf;
            local_136 = piStack_13a[1] - *(int *)0x67b6;
            local_134 = (int)local_136 >> 0xf;
            FUN_1ec2_0b0d((int)*(undefined4 *)0x6684 + 0xa0,
                          (int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                          CONCAT11((char)((uint)(piStack_13a[0x27] * 2) >> 8),
                                   *(undefined1 *)
                                    (*(int *)((int)piStack_13a + piStack_13a[0x27] * 2 + 0x73) +
                                    0x11cd)),local_a + 4,local_8 + 7,local_136,local_132);
          }
        }
        if ((char)piStack_13a[0x4e] != '\0') {
          local_132 = piStack_13a[8] - *(int *)0x67b2;
          local_130 = (int)local_132 >> 0xf;
          local_136 = piStack_13a[10] - *(int *)0x67b6;
          local_134 = (int)local_136 >> 0xf;
          FUN_1ec2_0c3b((int)*(undefined4 *)0x6684 + 0xa0,
                        (int)((ulong)*(undefined4 *)0x6684 >> 0x10),local_a + 4,local_8 + 7,
                        local_136,local_132);
          FUN_1ec2_0e8f((int)*(undefined4 *)0x6678 + 0x5400,
                        (int)((ulong)*(undefined4 *)0x6678 >> 0x10),
                        (int)*(undefined4 *)0x6684 + 0xa0,
                        (int)((ulong)*(undefined4 *)0x6684 >> 0x10),3,0x10,local_136 - 1,
                        local_132 - 1);
          if (*(char *)0x66af != '\0') {
            FUN_1ec2_09e7((int)*(undefined4 *)0x6684 + 0xa0,
                          (int)((ulong)*(undefined4 *)0x6684 >> 0x10),local_a + 7,local_8 + 4,
                          local_136 + 3,local_132 - 3);
            FUN_1ec2_0f44((int)*(undefined4 *)0x6678 + 0x5400,
                          (int)((ulong)*(undefined4 *)0x6678 >> 0x10),
                          (int)*(undefined4 *)0x6684 + 0xa0,
                          (int)((ulong)*(undefined4 *)0x6684 >> 0x10),4,0xffa3,0xffa0,3,0x10,
                          local_136 + 2,local_132 - 4);
          }
        }
        if ((*(char *)(*(int *)((int)piStack_13a + piStack_13a[0x27] * 2 + 0x73) + 0xf75) != '\0')
           && (*(char *)((int)piStack_13a + 0x99) != '\0')) {
          FUN_1ec2_0386(piStack_13a[0x24] / 2,
                        CONCAT11((char)((int)local_12e + 9),*(undefined1 *)((int)piStack_13a + 0x9b)
                                ),(int)*(undefined4 *)0x6684 + 0xa0,
                        (int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                        (int)*(undefined4 *)0x6678 + ((int)local_12e + 9) * 0x100,
                        (int)((ulong)*(undefined4 *)0x6678 >> 0x10),
                        *(char *)((int)local_12e + *(char *)((int)piStack_13a + 0x9b) * 0xe + 0x1f1)
                        + local_a,
                        (char)local_12e[*(char *)((int)piStack_13a + 0x9b) * 7 + 0xf5] + local_8);
        }
        if (*(char *)((int)piStack_13a + 0x9d) == '\0') {
          *(undefined1 *)((int)piStack_13a + 0xa1) = (char)(*(int *)0x1c + (int)local_12e);
          bVar7 = *(byte *)((int)piStack_13a + 0xa1);
          FUN_1ec2_01df(CONCAT11(bVar7,(undefined1)local_4),
                        CONCAT11(bVar7,*(undefined1 *)((int)piStack_13a + 0x9b)),
                        (int)*(undefined4 *)0x6684 + 0xa0,
                        (int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                        (int)*(undefined4 *)0x6678 + (uint)bVar7 * 0x100,
                        (int)((ulong)*(undefined4 *)0x6678 >> 0x10),local_a,local_8);
          if (*(char *)0x66af != '\0') {
            FUN_1ec2_0734(CONCAT11(*(byte *)((int)piStack_13a + 0xa1),
                                   *(undefined1 *)((int)piStack_13a + 0x9b)),
                          (int)*(undefined4 *)0x6684 + 0xa0,
                          (int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                          (int)*(undefined4 *)0x6678 +
                          (uint)*(byte *)((int)piStack_13a + 0xa1) * 0x100,
                          (int)((ulong)*(undefined4 *)0x6678 >> 0x10),local_a + 3,local_8 + -3);
          }
        }
        else {
          *(undefined1 *)((int)piStack_13a + 0xa1) =
               (char)(*(int *)(((*(uint *)0x6520 & 0x1f) >> 3) * 2 + 0x1c) + (int)local_12e);
          bVar7 = *(byte *)((int)piStack_13a + 0xa1);
          FUN_1ec2_01df(CONCAT11(bVar7,(undefined1)local_4),
                        CONCAT11(bVar7,*(undefined1 *)((int)piStack_13a + 0x9b)),
                        (int)*(undefined4 *)0x6684 + 0xa0,
                        (int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                        (int)*(undefined4 *)0x6678 + (uint)bVar7 * 0x100,
                        (int)((ulong)*(undefined4 *)0x6678 >> 0x10),local_a,local_8);
          if (*(char *)0x66af != '\0') {
            FUN_1ec2_0734(CONCAT11(*(byte *)((int)piStack_13a + 0xa1),
                                   *(undefined1 *)((int)piStack_13a + 0x9b)),
                          (int)*(undefined4 *)0x6684 + 0xa0,
                          (int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                          (int)*(undefined4 *)0x6678 +
                          (uint)*(byte *)((int)piStack_13a + 0xa1) * 0x100,
                          (int)((ulong)*(undefined4 *)0x6678 >> 0x10),local_a + 3,local_8 + -3);
          }
        }
      }
      if (local_4 == 1) break;
      local_4 = local_4 + 1;
    }
    if (*(char *)((int)*(undefined4 *)0x6670 + 0x144) != '\0') {
      uStack_138 = (uint)((ulong)*(undefined4 *)0x6670 >> 0x10);
      iVar14 = (int)*(undefined4 *)0x6670;
      piStack_13a = (int *)(iVar14 + 0xaa);
      if (*(char *)(iVar14 + 0x141) == '\0') {
        FUN_1ec2_0e8f((int)*(undefined4 *)0x667c + 0x83b,(int)((ulong)*(undefined4 *)0x667c >> 0x10)
                      ,(int)*(undefined4 *)0x6684 + 0xa0,(int)((ulong)*(undefined4 *)0x6684 >> 0x10)
                      ,3,7,auStack_1a[3],local_c);
      }
      else {
        FUN_1ec2_0e8f((int)*(undefined4 *)0x667c + 0x86c,(int)((ulong)*(undefined4 *)0x667c >> 0x10)
                      ,(int)*(undefined4 *)0x6684 + 0xa0,(int)((ulong)*(undefined4 *)0x6684 >> 0x10)
                      ,3,7,auStack_1a[3],local_c);
      }
      if (*(char *)(*(byte *)0x672c + 0x783b) != '\0') {
        local_12e = (int *)(uint)*(byte *)(*(int *)((int)piStack_13a + piStack_13a[0x27] * 2 + 0x73)
                                           * 0xe + 0x7e8);
        local_12c = 0;
        FUN_24dd_3eaf(0xff,local_122,unaff_SS,
                      *(int *)((int)piStack_13a + piStack_13a[0x27] * 2 + 0x73) * 0xe + 0x7e8,
                      unaff_DS);
        local_13c = local_12e;
        if (0 < (int)local_12e) {
          local_6 = (int *)0x1;
          while( true ) {
            if (local_122[(int)local_6] != 0x20) {
              iVar14 = FUN_24dd_3e7c();
              FUN_1ec2_0e8f((int)*(undefined4 *)0x6680 + (local_122[(int)local_6] - 0x41) * 0x10,
                            (int)((ulong)*(undefined4 *)0x6680 >> 0x10),
                            (int)*(undefined4 *)0x6684 + 0xa0,
                            (int)((ulong)*(undefined4 *)0x6684 >> 0x10),4,4,local_a + -5,
                            (int)local_6 * 4 + (local_8 - iVar14) + 4);
            }
            if (local_6 == local_13c) break;
            local_6 = (int *)((int)local_6 + 1);
          }
        }
      }
    }
  }
  local_4 = 0;
  while( true ) {
    if (*(char *)((int)*(undefined4 *)0x6690 + local_4 * 0x11) != '\0') {
      uStack_138 = (uint)((ulong)*(undefined4 *)0x6690 >> 0x10);
      piStack_13a = (int *)((int)*(undefined4 *)0x6690 + local_4 * 0x11);
      iVar14 = *(int *)0x2;
      iVar11 = iVar14 >> 0xf;
      FUN_24dd_3dbd();
      if (iVar14 == 0 && iVar11 == 0) {
        iVar14 = *(int *)((int)piStack_13a + 7) - *(int *)0x67b4;
        FUN_1ec2_0dc8((int)*(undefined4 *)0x6684,(int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                      CONCAT11((char)((uint)iVar14 >> 8),
                               (char)*(int *)CONCAT22(uStack_138,piStack_13a)),iVar14,
                      *(int *)((int)piStack_13a + 3) - *(int *)0x67b0);
        iVar14 = *(int *)((int)piStack_13a + 7) - *(int *)0x67b6;
        FUN_1ec2_0dc8((int)*(undefined4 *)0x6684 + 0xa0,(int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                      CONCAT11((char)((uint)iVar14 >> 8),
                               (char)*(int *)CONCAT22(uStack_138,piStack_13a)),iVar14,
                      *(int *)((int)piStack_13a + 3) - *(int *)0x67b2);
        if (*(char *)0x66af != '\0') {
          FUN_1ec2_0e4a((int)*(undefined4 *)0x6684,(int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                        (*(int *)((int)piStack_13a + 7) - *(int *)0x67b4) + 3,
                        (*(int *)((int)piStack_13a + 3) - *(int *)0x67b0) + -3);
          FUN_1ec2_0e4a((int)*(undefined4 *)0x6684 + 0xa0,
                        (int)((ulong)*(undefined4 *)0x6684 >> 0x10),
                        (*(int *)((int)piStack_13a + 7) - *(int *)0x67b6) + 3,
                        (*(int *)((int)piStack_13a + 3) - *(int *)0x67b2) + -3);
        }
      }
      FUN_1000_5c36(local_4);
    }
    if (local_4 == 700) break;
    local_4 = local_4 + 1;
  }
  iVar14 = *(int *)0x2;
  iVar11 = iVar14 >> 0xf;
  FUN_24dd_3dbd();
  if ((iVar14 == 0 && iVar11 == 0) && (*(char *)0x66a6 != '\0')) {
    local_6 = (int *)0x5;
    local_8 = 0;
    while( true ) {
      local_4 = 5;
      local_a = 0;
      while( true ) {
        uVar4 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_4 * 4);
        *(undefined1 *)((int)*(undefined4 *)0x6684 + (local_a + 0xa2) * 0x140 + local_8 + 0x86) =
             *(undefined1 *)((int)uVar4 + (int)local_6);
        local_4 = local_4 + 10;
        if (local_a == 0x22) break;
        local_a = local_a + 1;
      }
      local_6 = local_6 + 5;
      if (local_8 == 0x32) break;
      local_8 = local_8 + 1;
    }
    if (*(char *)((int)*(undefined4 *)0x6670 + 0x9a) != '\0') {
      uVar15 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
      iVar14 = (int)*(undefined4 *)0x6670;
      *(undefined1 *)
       ((int)*(undefined4 *)0x6684 + (*(int *)(iVar14 + 10) / 10 + 0xa2) * 0x140 +
       *(int *)(iVar14 + 6) / 10 + 0x86) = 0x81;
    }
    local_136 = 0xc4;
    local_134 = 0;
    local_132 = 0xb8;
    local_130 = 0;
    if (*(char *)((int)*(undefined4 *)0x6670 + 0x144) != '\0') {
      uVar15 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
      iVar14 = (int)*(undefined4 *)0x6670;
      *(undefined1 *)
       ((int)*(undefined4 *)0x6684 + (*(int *)(iVar14 + 0xb4) / 10 + 0xa2) * 0x140 +
       *(int *)(iVar14 + 0xb0) / 10 + 0x86) = 0x85;
    }
  }
  iVar14 = *(int *)0x2;
  iVar11 = iVar14 >> 0xf;
  FUN_24dd_3dbd();
  if ((iVar14 == 0 && iVar11 == 0) && (*(char *)0x66a5 != '\0')) {
    FUN_1ec2_13c5();
  }
  FUN_1ec2_13b0(0,0xa000,(int)*(undefined4 *)0x6684,(int)((ulong)*(undefined4 *)0x6684 >> 0x10));
  if ((*(uint *)0x6520 & 3) == 0) {
    local_4 = 1;
    while (FUN_1ec2_1619(*(undefined1 *)(local_4 * 2 + 0x8b),*(undefined1 *)(local_4 * 2 + 0x8a)),
          local_4 != 4) {
      local_4 = local_4 + 1;
    }
  }
  if (*(int *)0x6524 < 0x21) {
    FUN_1ec2_10ea(*(undefined2 *)0x6524,0x5826,unaff_DS);
  }
  else if (*(char *)0x67c0 != '\0') {
    FUN_1ec2_11b5(*(undefined1 *)0x67c0,0x5826,unaff_DS);
    *(char *)0x67c0 = *(char *)0x67c0 + -1;
    if (*(char *)0x67c0 == '\0') {
      *(byte *)0x67c0 = *(byte *)0x67c0 ^ *(byte *)0x67c0;
      FUN_1ec2_155e(0x5826,unaff_DS);
    }
  }
  return;
code_r0x00016a48:
  if ((local_12c < 1) && ((local_12c < 0 || (local_12e < (int *)0x4)))) {
    puVar1 = (uint *)0x642d;
    uVar9 = *puVar1;
    *puVar1 = *puVar1 + 1000;
    *(int *)0x642f = *(int *)0x642f + (uint)(0xfc17 < uVar9);
  }
  else {
    uVar9 = *(uint *)0x642f;
    iVar14 = FUN_24dd_3dbd();
    *(int *)0x642d = -iVar14;
    *(int *)0x642f = (~uVar9 + 1) - (uint)(iVar14 != 0);
  }
  uVar3 = *(uint *)0x642d;
  iVar14 = *(int *)0x642f;
  puVar1 = (uint *)0x6429;
  uVar9 = *puVar1;
  *puVar1 = *puVar1 + uVar3;
  *(int *)0x642b = *(int *)0x642b + iVar14 + (uint)CARRY2(uVar9,uVar3);
  if ((((*(char *)((int)*(undefined4 *)0x6670 + 0x95) != '\0') &&
       (*(int *)0x6427 + -6 < *(int *)((int)*(undefined4 *)0x6670 + 6))) &&
      (*(int *)((int)*(undefined4 *)0x6670 + 6) < *(int *)0x6427 + 6)) &&
     ((*(int *)0x642b + -6 < *(int *)((int)*(undefined4 *)0x6670 + 10) &&
      (*(int *)((int)*(undefined4 *)0x6670 + 10) < *(int *)0x642b + 6)))) {
    FUN_1000_0ebe(*(undefined2 *)0x642b,*(undefined2 *)0x6427,1);
    *(undefined1 *)((int)*(undefined4 *)0x6670 + 0x95) = 0;
    iVar11 = (int)*(uint *)0x66a3 >> 0xf;
    uVar15 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
    iVar13 = (int)*(undefined4 *)0x6670;
    iVar14 = *(int *)(iVar13 + 0x42);
    if ((iVar14 < iVar11) || ((iVar14 <= iVar11 && (*(uint *)(iVar13 + 0x40) < *(uint *)0x66a3)))) {
      uVar15 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
      iVar14 = (int)*(undefined4 *)0x6670;
      puVar1 = (uint *)(iVar14 + 0x40);
      uVar9 = *puVar1;
      *puVar1 = *puVar1 + 1;
      piVar2 = (int *)(iVar14 + 0x42);
      *piVar2 = *piVar2 + (uint)(0xfffe < uVar9);
    }
  }
  goto LAB_1000_6b1a;
code_r0x00016c75:
  if ((local_12c < 1) && ((local_12c < 0 || (local_12e < (int *)0x4)))) {
    puVar1 = (uint *)0x6438;
    uVar9 = *puVar1;
    *puVar1 = *puVar1 + 1000;
    *(int *)0x643a = *(int *)0x643a + (uint)(0xfc17 < uVar9);
  }
  else {
    uVar9 = *(uint *)0x643a;
    iVar14 = FUN_24dd_3dbd();
    *(int *)0x6438 = -iVar14;
    *(int *)0x643a = (~uVar9 + 1) - (uint)(iVar14 != 0);
  }
  uVar3 = *(uint *)0x6438;
  iVar14 = *(int *)0x643a;
  puVar1 = (uint *)0x6434;
  uVar9 = *puVar1;
  *puVar1 = *puVar1 + uVar3;
  *(int *)0x6436 = *(int *)0x6436 + iVar14 + (uint)CARRY2(uVar9,uVar3);
  if ((((*(char *)((int)*(undefined4 *)0x6670 + 0x13f) != '\0') &&
       (*(int *)0x6432 + -6 < *(int *)((int)*(undefined4 *)0x6670 + 0xb0))) &&
      (*(int *)((int)*(undefined4 *)0x6670 + 0xb0) < *(int *)0x6432 + 6)) &&
     ((*(int *)0x6436 + -6 < *(int *)((int)*(undefined4 *)0x6670 + 0xb4) &&
      (*(int *)((int)*(undefined4 *)0x6670 + 0xb4) < *(int *)0x6436 + 6)))) {
    FUN_1000_0ebe(*(undefined2 *)0x6436,*(undefined2 *)0x6432,0);
    *(undefined1 *)((int)*(undefined4 *)0x6670 + 0x13f) = 0;
    iVar11 = (int)*(uint *)0x66a3 >> 0xf;
    uVar15 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
    iVar13 = (int)*(undefined4 *)0x6670;
    iVar14 = *(int *)(iVar13 + 0xec);
    if ((iVar14 < iVar11) || ((iVar14 <= iVar11 && (*(uint *)(iVar13 + 0xea) < *(uint *)0x66a3)))) {
      uVar15 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
      iVar14 = (int)*(undefined4 *)0x6670;
      puVar1 = (uint *)(iVar14 + 0xea);
      uVar9 = *puVar1;
      *puVar1 = *puVar1 + 1;
      piVar2 = (int *)(iVar14 + 0xec);
      *piVar2 = *piVar2 + (uint)(0xfffe < uVar9);
    }
  }
  goto LAB_1000_6d52;
}

