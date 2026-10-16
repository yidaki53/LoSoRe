
void FUN_1000_bfd7(int param_1,char param_2)

{
  char *pcVar1;
  undefined1 uVar2;
  char cVar3;
  undefined2 uVar4;
  int iVar5;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  bool bVar6;
  undefined1 *puVar7;
  undefined2 uVar8;
  undefined2 uVar9;
  undefined1 local_23f [252];
  uint local_143;
  int local_141;
  undefined1 local_13f [30];
  byte local_121 [13];
  uint local_114;
  uint local_112;
  uint local_110;
  undefined4 local_10e;
  int local_10a;
  undefined2 local_108;
  uint local_106;
  int local_104;
  undefined2 uStack_6;
  undefined2 uStack_4;
  
  uStack_4 = 0x1000;
  uStack_6 = 0xbfe2;
  FUN_24dd_0530();
  if (param_2 == '\0') {
    *(char *)0x66ac = *(char *)0x66ac + '\x01';
    *(char *)0x66ac = *(char *)0x66ac % '\x04';
  }
  else if (param_2 == '\x01') {
    cVar3 = *(char *)0x66ac;
    if (cVar3 == '\0') {
      uVar4 = FUN_1000_ad8b(param_1,*(undefined2 *)0x669f,999,1,0x118,0x1c);
      if (*(char *)(param_1 + -0x10c) != '\0') {
        *(undefined2 *)0x669f = uVar4;
      }
    }
    else if (((cVar3 == '\x02') || (cVar3 == '\x03')) &&
            (uVar4 = FUN_1000_ad8b(param_1,*(undefined2 *)0x66a3,999,1,0x118,0x1c),
            *(char *)(param_1 + -0x10c) != '\0')) {
      *(undefined2 *)0x66a3 = uVar4;
    }
  }
  else if (param_2 == '\x02') {
    uVar4 = FUN_1000_ad8b(param_1,*(undefined2 *)0x669d,9999,0,0x118,0x24);
    if (*(char *)(param_1 + -0x10c) != '\0') {
      *(undefined2 *)0x669d = uVar4;
    }
  }
  else if (param_2 == '\x03') {
    uVar2 = FUN_1000_ad8b(param_1,*(undefined1 *)0x669c,99,0,0x118,0x2c);
    if (*(char *)(param_1 + -0x10c) != '\0') {
      *(undefined1 *)0x669c = uVar2;
    }
  }
  else if (param_2 == '\x04') {
    *(bool *)0x66ad = *(char *)0x66ad == '\0';
  }
  else if (param_2 == '\x05') {
    *(bool *)0x66a6 = *(char *)0x66a6 == '\0';
  }
  else if (param_2 == '\a') {
    local_10e = FUN_24dd_028a(900);
    FUN_24dd_3eaf(8,local_10e,0xbf73,0x24dd);
    FUN_24cb_0000(local_13f,unaff_SS,0x2f,0xbf7c,0x24dd);
    local_110 = 0;
    while (*(int *)0x78ee == 0) {
      local_110 = local_110 + 1;
      puVar7 = local_23f;
      uVar4 = unaff_SS;
      FUN_24dd_3ed3(local_121[0] - 4,1,local_121,unaff_SS);
      FUN_24dd_3eaf(8,(int)local_10e + local_110 * 9,(int)((ulong)local_10e >> 0x10),puVar7,uVar4);
      FUN_24cb_003e(local_13f,unaff_SS);
    }
    local_114 = 0;
    local_112 = 0;
    if (*(char *)0x672e == '\0') {
      local_114 = 0;
    }
    else {
      while( true ) {
        iVar5 = (int)local_10e + local_114 * 9;
        bVar6 = iVar5 == 0;
        FUN_24dd_3f86(0x672e,unaff_DS,iVar5,(int)((ulong)local_10e >> 0x10));
        if ((bVar6) || ((int)local_110 <= (int)local_114)) break;
        local_114 = local_114 + 1;
      }
    }
    if (local_114 == local_110) {
      local_114 = 0;
    }
    if ((int)local_114 < (int)(local_110 - 0xd)) {
      local_112 = local_114;
    }
    else {
      local_112 = local_110 - 0xd;
    }
    if ((int)local_112 < 0) {
      local_112 = 0;
    }
    FUN_1ec2_00a5(0x82,0x98,(int)*(undefined4 *)0x65d7 + 0x19a8,
                  (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),(int)*(undefined4 *)0x6684 + 0x19a8,
                  (int)((ulong)*(undefined4 *)0x6684 >> 0x10));
    FUN_1ec2_00a5(8,0x8e,0x19b2,0xa000,(int)*(undefined4 *)0x65d7 + 0x19b2,
                  (int)((ulong)*(undefined4 *)0x65d7 >> 0x10));
    uVar9 = 0xa000;
    uVar8 = 0x19b2;
    uVar4 = FUN_202c_0673(0xbf82,0x1ec2);
    FUN_1ec2_0d88(0,7,uVar4,uVar8,uVar9);
    FUN_1ec2_13e9(0x19a6,unaff_DS,0,0xa000,0x32,0xbf82,0x1ec2,0x15,0xb4);
    local_108 = (undefined2)(0x540 / (long)(int)(local_110 + 1));
    do {
      FUN_1ec2_00a5(0x82,0x98,(int)*(undefined4 *)0x65d7 + 0x23a8,
                    (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),(int)*(undefined4 *)0x6684 + 0x23a8,
                    (int)((ulong)*(undefined4 *)0x6684 >> 0x10));
      uVar8 = (undefined2)((ulong)*(undefined4 *)0x65d7 >> 0x10);
      iVar5 = (int)*(undefined4 *)0x65d7 + ((local_114 - local_112) * 8 + 0x1c) * 0x140 + 0xb2;
      uVar4 = FUN_202c_0673((int)local_10e + local_114 * 9,(int)((ulong)local_10e >> 0x10));
      FUN_1ec2_0d88(0,7,uVar4,iVar5,uVar8);
      local_143 = local_112 + 0xd;
      local_141 = (int)local_143 >> 0xf;
      iVar5 = (int)local_112 >> 0xf;
      if ((iVar5 <= local_141) && ((iVar5 < local_141 || (local_112 <= local_143)))) {
        local_106 = local_112;
        local_104 = iVar5;
        while( true ) {
          if ((local_104 < (int)local_110 >> 0xf) ||
             ((local_104 <= (int)local_110 >> 0xf && (local_106 <= local_110)))) {
            uVar8 = 0xb5;
            uVar4 = FUN_24dd_3e7c(0xb5);
            FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x65d7 + 0x2580,
                          (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),0,
                          (int)local_10e + local_106 * 9,(int)((ulong)local_10e >> 0x10),uVar4,uVar8
                         );
            uVar8 = 0xb4;
            uVar4 = FUN_24dd_3e7c(0xb4);
            if (((int)local_114 >> 0xf == local_104) && (local_114 == local_106)) {
              cVar3 = '\x01';
            }
            else {
              cVar3 = '\0';
            }
            FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x65d7 + 0x2440,
                          (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),*(undefined1 *)(cVar3 + 0x381)
                          ,(int)local_10e + local_106 * 9,(int)((ulong)local_10e >> 0x10),uVar4,
                          uVar8);
          }
          if ((local_104 == local_141) && (local_106 == local_143)) break;
          bVar6 = 0xfffe < local_106;
          local_106 = local_106 + 1;
          local_104 = local_104 + (uint)bVar6;
        }
      }
      if (0xd < (int)local_110) {
        FUN_1ec2_12e6(0,0x1f26,unaff_DS,(int)*(undefined4 *)0x65d7,
                      (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),0x1e,0xac);
        FUN_1ec2_12e6(0x32,0x1f26,unaff_DS,(int)*(undefined4 *)0x65d7,
                      (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),0x1d,0xab);
        FUN_1ec2_12e6(0,0x1f66,unaff_DS,(int)*(undefined4 *)0x65d7,
                      (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),0x86,0xac);
        FUN_1ec2_12e6(0x32,0x1f66,unaff_DS,(int)*(undefined4 *)0x65d7,
                      (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),0x85,0xab);
        local_10a = (int)(local_112 * 0x60) / (int)(local_110 + 1);
        FUN_1ec2_0d5d(0,local_108,7,(int)*(undefined4 *)0x65d7 + (local_10a + 0x25) * 0x140 + 0xab,
                      (int)((ulong)*(undefined4 *)0x65d7 >> 0x10));
        FUN_1ec2_0d5d(7,local_108,7,(int)*(undefined4 *)0x65d7 + (local_10a + 0x24) * 0x140 + 0xaa,
                      (int)((ulong)*(undefined4 *)0x65d7 >> 0x10));
      }
      if (*(char *)0x78db != '\0') {
        if (*(char *)0x4b8 != '\0') {
          FUN_235c_095c(0,0,*(undefined2 *)0x67a0,*(undefined2 *)0x67a2);
        }
        *(undefined1 *)0x78db = 0;
        local_114 = local_114 - 1;
        if ((int)local_114 < 0) {
          local_114 = 0;
        }
        if ((int)local_114 < (int)local_112) {
          local_112 = local_112 - 1;
        }
      }
      if (*(char *)0x78e3 != '\0') {
        if (*(char *)0x4b8 != '\0') {
          FUN_235c_095c(0,0,*(undefined2 *)0x679c,*(undefined2 *)0x679e);
        }
        *(undefined1 *)0x78e3 = 0;
        local_114 = local_114 + 1;
        if ((int)local_110 < (int)local_114) {
          local_114 = local_110;
        }
        if ((int)(local_112 + 0xd) < (int)local_114) {
          local_112 = local_112 + 1;
        }
      }
      FUN_1ec2_13c5();
      FUN_1ec2_1619(0xffae,0xffa8);
      FUN_1ec2_00a5(0x82,0x98,0x23a8,0xa000,(int)*(undefined4 *)0x65d7 + 0x23a8,
                    (int)((ulong)*(undefined4 *)0x65d7 >> 0x10));
    } while ((*(char *)0x7857 == '\0') && (*(char *)0x783c == '\0'));
    if (*(char *)0x4b8 != '\0') {
      FUN_235c_095c(0,0,*(undefined2 *)0x67a4,*(undefined2 *)0x67a6);
    }
    *(undefined1 *)0x7857 = 0;
    if (*(char *)0x783c == '\0') {
      if (local_114 == 0) {
        *(undefined1 *)0x66a9 = 1;
        *(undefined1 *)0x672e = 0;
      }
      else {
        *(undefined1 *)0x66a9 = 0;
        FUN_24dd_3eaf(8,0x672e,unaff_DS,(int)local_10e + local_114 * 9,
                      (int)((ulong)local_10e >> 0x10));
      }
    }
    *(undefined1 *)0x783c = 0;
    FUN_24dd_029f(900,(undefined2)local_10e,local_10e._2_2_);
  }
  else if (param_2 == '\b') {
    *(bool *)0x66ae = *(char *)0x66ae == '\0';
  }
  else if (param_2 == '\t') {
    *(bool *)0x66af = *(char *)0x66af == '\0';
  }
  else if (param_2 == '\n') {
    *(bool *)0x66a5 = *(char *)0x66a5 == '\0';
  }
  else if (param_2 == '\v') {
    *(bool *)0x6716 = *(char *)0x6716 == '\0';
  }
  else if (param_2 == '\f') {
    FUN_1000_b45e(param_1,0);
  }
  else if (param_2 == '\r') {
    FUN_1000_b45e(param_1,1);
  }
  else if (param_2 == '\x0e') {
    local_114 = 1;
    local_112 = 1;
    while( true ) {
      FUN_1ec2_00a5(0x82,0x98,(int)*(undefined4 *)0x65d7 + 0x19a8,
                    (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),(int)*(undefined4 *)0x6684 + 0x19a8,
                    (int)((ulong)*(undefined4 *)0x6684 >> 0x10));
      FUN_1ec2_00a5(8,0x8e,0x19b2,0xa000,(int)*(undefined4 *)0x65d7 + 0x19b2,
                    (int)((ulong)*(undefined4 *)0x65d7 >> 0x10));
      uVar9 = 0xa000;
      uVar8 = 0x19b2;
      uVar4 = FUN_202c_0673(0xbf90,0x1ec2);
      FUN_1ec2_0d88(0,7,uVar4,uVar8,uVar9);
      uVar9 = 0xa000;
      uVar8 = 0x19f8;
      uVar4 = FUN_202c_0673(0xbf97,0x1ec2);
      FUN_1ec2_0d88(0,7,uVar4,uVar8,uVar9);
      FUN_1ec2_13e9(0x19a6,unaff_DS,0,0xa000,0x32,0xbf90,0x1ec2,0x15,0xb4);
      FUN_1ec2_13e9(0x19a6,unaff_DS,0,0xa000,0x32,0xbf97,0x1ec2,0x15,0xfa);
      local_108 = 0x21;
      do {
        FUN_1ec2_00a5(0x82,0x98,(int)*(undefined4 *)0x65d7 + 0x23a8,
                      (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),
                      (int)*(undefined4 *)0x6684 + 0x23a8,
                      (int)((ulong)*(undefined4 *)0x6684 >> 0x10));
        uVar4 = FUN_202c_0673(*(char *)(*(byte *)(local_114 + 0xa9d) + 0x66af) * 0xd + 0x47e,
                              unaff_DS);
        *(undefined2 *)(param_1 + -4) = uVar4;
        uVar8 = (undefined2)((ulong)*(undefined4 *)0x65d7 >> 0x10);
        iVar5 = (int)*(undefined4 *)0x65d7 + ((local_114 - local_112) * 8 + 0x1c) * 0x140 + 0xb2;
        uVar4 = FUN_202c_0673((uint)*(byte *)(local_114 + 0xa9d) * 0xe + 0x7e8,unaff_DS);
        FUN_1ec2_0d88(0,7,uVar4,iVar5,uVar8);
        FUN_1ec2_0d88(0,7,*(undefined2 *)(param_1 + -4),
                      (int)*(undefined4 *)0x65d7 + ((local_114 - local_112) * 8 + 0x1c) * 0x140 +
                      (0x10c - (*(uint *)(param_1 + -4) >> 1)),
                      (int)((ulong)*(undefined4 *)0x65d7 >> 0x10));
        local_143 = local_112 + 0xd;
        local_141 = (int)local_143 >> 0xf;
        iVar5 = (int)local_112 >> 0xf;
        if ((iVar5 <= local_141) && ((iVar5 < local_141 || (local_112 <= local_143)))) {
          local_106 = local_112;
          local_104 = iVar5;
          while( true ) {
            uVar4 = FUN_202c_0673(*(char *)(*(byte *)(local_106 + 0xa9d) + 0x66af) * 0xd + 0x47e,
                                  unaff_DS);
            *(undefined2 *)(param_1 + -4) = uVar4;
            uVar8 = 0xb5;
            uVar4 = FUN_24dd_3e7c(0xb5);
            FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x65d7 + 0x2580,
                          (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),0,
                          (uint)*(byte *)(local_106 + 0xa9d) * 0xe + 0x7e8,unaff_DS,uVar4,uVar8);
            uVar8 = 0xb4;
            uVar4 = FUN_24dd_3e7c(0xb4);
            if (((int)local_114 >> 0xf == local_104) && (local_114 == local_106)) {
              cVar3 = '\x01';
            }
            else {
              cVar3 = '\0';
            }
            FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x65d7 + 0x2440,
                          (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),*(undefined1 *)(cVar3 + 0x381)
                          ,(uint)*(byte *)(local_106 + 0xa9d) * 0xe + 0x7e8,unaff_DS,uVar4,uVar8);
            iVar5 = 0x10f - (*(uint *)(param_1 + -4) >> 1);
            uVar4 = FUN_24dd_3e7c(iVar5);
            FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x65d7 + 0x2580,
                          (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),0,
                          *(char *)(*(byte *)(local_106 + 0xa9d) + 0x66af) * 0xd + 0x47e,unaff_DS,
                          uVar4,iVar5);
            iVar5 = 0x10e - (*(uint *)(param_1 + -4) >> 1);
            uVar4 = FUN_24dd_3e7c(iVar5);
            if (((int)local_114 >> 0xf == local_104) && (local_114 == local_106)) {
              cVar3 = '\x01';
            }
            else {
              cVar3 = '\0';
            }
            FUN_1ec2_13e9(0x19a6,unaff_DS,(int)*(undefined4 *)0x65d7 + 0x2440,
                          (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),*(undefined1 *)(cVar3 + 0x381)
                          ,*(char *)(*(byte *)(local_106 + 0xa9d) + 0x66af) * 0xd + 0x47e,unaff_DS,
                          uVar4,iVar5);
            if ((local_104 == local_141) && (local_106 == local_143)) break;
            bVar6 = 0xfffe < local_106;
            local_106 = local_106 + 1;
            local_104 = local_104 + (uint)bVar6;
          }
        }
        FUN_1ec2_12e6(0,0x1f26,unaff_DS,(int)*(undefined4 *)0x65d7,
                      (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),0x1e,0xac);
        FUN_1ec2_12e6(0x32,0x1f26,unaff_DS,(int)*(undefined4 *)0x65d7,
                      (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),0x1d,0xab);
        FUN_1ec2_12e6(0,0x1f66,unaff_DS,(int)*(undefined4 *)0x65d7,
                      (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),0x86,0xac);
        FUN_1ec2_12e6(0x32,0x1f66,unaff_DS,(int)*(undefined4 *)0x65d7,
                      (int)((ulong)*(undefined4 *)0x65d7 >> 0x10),0x85,0xab);
        local_10a = (int)(local_112 * 0x60) / 0x28;
        FUN_1ec2_0d5d(0,local_108,7,(int)*(undefined4 *)0x65d7 + (local_10a + 0x22) * 0x140 + 0xab,
                      (int)((ulong)*(undefined4 *)0x65d7 >> 0x10));
        FUN_1ec2_0d5d(7,local_108,7,(int)*(undefined4 *)0x65d7 + (local_10a + 0x21) * 0x140 + 0xaa,
                      (int)((ulong)*(undefined4 *)0x65d7 >> 0x10));
        if (*(char *)0x78db != '\0') {
          if (*(char *)0x4b8 != '\0') {
            FUN_235c_095c(0,0,*(undefined2 *)0x67a0,*(undefined2 *)0x67a2);
          }
          *(undefined1 *)0x78db = 0;
          local_114 = local_114 - 1;
          if ((int)local_114 < 1) {
            local_114 = 1;
          }
          if ((int)local_114 < (int)local_112) {
            local_112 = local_112 - 1;
          }
        }
        if (*(char *)0x78e3 != '\0') {
          if (*(char *)0x4b8 != '\0') {
            FUN_235c_095c(0,0,*(undefined2 *)0x679c,*(undefined2 *)0x679e);
          }
          *(undefined1 *)0x78e3 = 0;
          local_114 = local_114 + 1;
          if (0x28 < (int)local_114) {
            local_114 = 0x28;
          }
          if ((int)(local_112 + 0xd) < (int)local_114) {
            local_112 = local_112 + 1;
          }
        }
        if (*(char *)0x78de != '\0') {
          if (*(char *)0x4b8 != '\0') {
            FUN_235c_095c(0,0,*(undefined2 *)0x679c,*(undefined2 *)0x679e);
          }
          *(undefined1 *)0x78de = 0;
          pcVar1 = (char *)(*(byte *)(local_114 + 0xa9d) + 0x66af);
          *pcVar1 = *pcVar1 + -1;
          if (*(char *)(*(byte *)(local_114 + 0xa9d) + 0x66af) < '\0') {
            *(undefined1 *)(*(byte *)(local_114 + 0xa9d) + 0x66af) = 2;
          }
        }
        if (*(char *)0x78e0 != '\0') {
          if (*(char *)0x4b8 != '\0') {
            FUN_235c_095c(0,0,*(undefined2 *)0x67a0,*(undefined2 *)0x67a2);
          }
          *(undefined1 *)0x78e0 = 0;
          pcVar1 = (char *)(*(byte *)(local_114 + 0xa9d) + 0x66af);
          *pcVar1 = *pcVar1 + '\x01';
          if ('\x02' < *(char *)(*(byte *)(local_114 + 0xa9d) + 0x66af)) {
            *(undefined1 *)(*(byte *)(local_114 + 0xa9d) + 0x66af) = 0;
          }
        }
        FUN_1ec2_13c5();
        FUN_1ec2_1619(0xffae,0xffa8);
        FUN_1ec2_00a5(0x82,0x98,0x23a8,0xa000,(int)*(undefined4 *)0x65d7 + 0x23a8,
                      (int)((ulong)*(undefined4 *)0x65d7 >> 0x10));
        local_110 = 0x28;
        local_106 = 1;
        local_104 = 0;
        while( true ) {
          if ('\0' < *(char *)(local_106 + 0x66af)) {
            local_110 = local_110 + -1;
          }
          if ((local_104 == 0) && (local_106 == 0x28)) break;
          bVar6 = 0xfffe < local_106;
          local_106 = local_106 + 1;
          local_104 = local_104 + (uint)bVar6;
        }
      } while (*(char *)0x783c == '\0');
      *(undefined1 *)0x783c = 0;
      if (0 < (int)local_110) break;
      FUN_1ec2_0d88(0,0x11,0x62,0x4932,0xa000);
      FUN_1ec2_13e9(0x19a6,unaff_DS,0,0xa000,6,0xbfa4,0x1ec2,0x3c,0xb4);
      do {
        cVar3 = FUN_24ba_00d8();
      } while (cVar3 == '\0');
    }
    if (*(char *)0x4b8 != '\0') {
      FUN_235c_095c(0,0,*(undefined2 *)0x67a4,*(undefined2 *)0x67a6);
    }
  }
  return;
}

