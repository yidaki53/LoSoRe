
void FUN_1000_ccf1(int param_1,char param_2,char param_3)

{
  char cVar1;
  undefined1 extraout_AH;
  undefined1 extraout_AH_00;
  undefined1 extraout_AH_01;
  undefined1 uVar2;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  
  FUN_24dd_0530();
  if (((((param_3 == '\x04') || (param_3 == '\x05')) || (param_3 == '\b')) ||
      ((param_3 == '\t' || (param_3 == '\n')))) || (param_3 == '\v')) {
    uVar2 = extraout_AH;
    if (*(char *)0x4b8 != '\0') {
      if (param_2 < '\x01') {
        FUN_235c_095c(0,0,*(undefined2 *)0x679c,*(undefined2 *)0x679e);
        uVar2 = extraout_AH_01;
      }
      else {
        FUN_235c_095c(0,0,*(undefined2 *)0x67a0,*(undefined2 *)0x67a2);
        uVar2 = extraout_AH_00;
      }
    }
    *(undefined1 *)0x78e0 = 0;
    *(undefined1 *)0x78de = 0;
    FUN_1000_bfd7(param_1,CONCAT11(uVar2,param_3));
  }
  else if (param_3 == '\0') {
    if (*(char *)0x4b8 != '\0') {
      if (param_2 < '\x01') {
        FUN_235c_095c(0,0,*(undefined2 *)0x679c,*(undefined2 *)0x679e);
      }
      else {
        FUN_235c_095c(0,0,*(undefined2 *)0x67a0,*(undefined2 *)0x67a2);
      }
    }
    *(undefined1 *)0x78de = 0;
    *(undefined1 *)0x78e0 = 0;
    *(char *)0x66ac = *(char *)0x66ac + param_2;
    if (*(char *)0x66ac < '\0') {
      *(undefined1 *)0x66ac = 3;
    }
    if ('\x03' < *(char *)0x66ac) {
      *(undefined1 *)0x66ac = 0;
    }
  }
  else if (param_3 == '\x01') {
    if (*(char *)(param_1 + -0x10d) == '\0') {
      cVar1 = *(char *)0x66ac;
      if (cVar1 == '\0') {
        if ((param_2 < '\0') && (1 < *(int *)0x669f)) {
          *(int *)0x669f = *(int *)0x669f + (int)param_2;
        }
        if (('\0' < param_2) && (*(int *)0x669f < 999)) {
          *(int *)0x669f = *(int *)0x669f + (int)param_2;
        }
      }
      else if (cVar1 == '\x01') {
        if ((param_2 < '\0') && (0x3c < *(int *)0x66a1)) {
          *(int *)0x66a1 = *(int *)0x66a1 + param_2 * 10;
        }
        if (('\0' < param_2) && (*(int *)0x66a1 < 0xe10)) {
          *(int *)0x66a1 = *(int *)0x66a1 + param_2 * 10;
        }
      }
      else if ((cVar1 == '\x02') || (cVar1 == '\x03')) {
        if ((param_2 < '\0') && (1 < *(int *)0x66a3)) {
          *(int *)0x66a3 = *(int *)0x66a3 + (int)param_2;
        }
        if (('\0' < param_2) && (*(int *)0x66a3 < 999)) {
          *(int *)0x66a3 = *(int *)0x66a3 + (int)param_2;
        }
      }
    }
  }
  else if (param_3 == '\x02') {
    if (*(char *)(param_1 + -0x10d) == '\0') {
      if ((param_2 < '\0') && (*(int *)0x669d != 0)) {
        *(int *)0x669d = *(int *)0x669d + (int)param_2;
      }
      if (('\0' < param_2) && (*(uint *)0x669d < 9999)) {
        *(int *)0x669d = *(int *)0x669d + (int)param_2;
      }
    }
  }
  else if (param_3 == '\x03') {
    if (*(char *)(param_1 + -0x10d) == '\0') {
      if ((param_2 < '\0') && (*(char *)0x669c != '\0')) {
        *(char *)0x669c = *(char *)0x669c + param_2;
      }
      if (('\0' < param_2) && (*(byte *)0x669c < 99)) {
        *(char *)0x669c = *(char *)0x669c + param_2;
      }
    }
  }
  else if ((param_3 == '\x06') && (*(char *)(param_1 + -0x10d) == '\0')) {
    if ((param_2 < '\0') && (0 < *(int *)0x66aa)) {
      *(int *)0x66aa = *(int *)0x66aa + -0x19;
    }
    if (('\0' < param_2) && (*(int *)0x66aa < 500)) {
      *(int *)0x66aa = *(int *)0x66aa + 0x19;
    }
  }
  return;
}

