
void FUN_1000_bcca(int param_1)

{
  char cVar1;
  undefined2 uVar2;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  undefined1 *puVar3;
  undefined2 uVar4;
  undefined1 local_202 [256];
  undefined1 local_102 [252];
  undefined2 uStack_6;
  undefined2 uStack_4;
  
  uStack_4 = 0x1000;
  uStack_6 = 0xbcd5;
  FUN_24dd_0530();
  FUN_24dd_3eaf(0x10,param_1 + -0x10b,unaff_SS,*(char *)0x66ac * 0x11 + 0x43a,unaff_DS);
  cVar1 = *(char *)0x66ac;
  if (cVar1 == '\0') {
    puVar3 = local_102;
    uVar4 = unaff_SS;
    FUN_202c_076d(*(int *)0x669f,*(int *)0x669f >> 0xf);
    FUN_24dd_3eaf(0x10,param_1 + -0xfa,unaff_SS,puVar3,uVar4);
    FUN_24dd_3eaf(0x14,599,unaff_DS,0xbc7c,0x24dd);
  }
  else if (cVar1 == '\x01') {
    puVar3 = local_102;
    uVar4 = unaff_SS;
    FUN_1ec2_00d0(*(int *)0x66a1,*(int *)0x66a1 >> 0xf);
    FUN_24dd_3eaf(0x10,param_1 + -0xfa,unaff_SS,puVar3,uVar4);
    FUN_24dd_3eaf(0x14,599,unaff_DS,0xbc82,0x24dd);
  }
  else if ((cVar1 == '\x02') || (cVar1 == '\x03')) {
    puVar3 = local_102;
    uVar4 = unaff_SS;
    FUN_202c_076d(*(int *)0x66a3,*(int *)0x66a3 >> 0xf);
    FUN_24dd_3eaf(0x10,param_1 + -0xfa,unaff_SS,puVar3,uVar4);
    FUN_24dd_3eaf(0x14,599,unaff_DS,0xbc8f,0x24dd);
  }
  puVar3 = local_102;
  uVar4 = unaff_SS;
  FUN_202c_076d(*(undefined2 *)0x669d,0);
  FUN_24dd_3f14(0xbc9c,0x202c);
  FUN_24dd_3eaf(0x10,param_1 + -0xe9,unaff_SS,puVar3,uVar4);
  puVar3 = local_102;
  uVar4 = unaff_SS;
  FUN_202c_076d(*(undefined1 *)0x669c,0);
  FUN_24dd_3eaf(0x10,param_1 + -0xd8,unaff_SS,puVar3,uVar4);
  FUN_24dd_3eaf(0x10,param_1 + -199,unaff_SS,*(char *)0x66ad * 4 + 4,unaff_DS);
  FUN_24dd_3eaf(0x10,param_1 + -0xb6,unaff_SS,*(char *)0x66a6 * 4 + 4,unaff_DS);
  puVar3 = local_102;
  uVar4 = unaff_SS;
  FUN_202c_076d(*(int *)0x66aa,*(int *)0x66aa >> 0xf);
  FUN_24dd_3f14(0xbc9c,0x202c);
  uVar2 = 0x24dd;
  FUN_24dd_3eaf(0x10,param_1 + -0xa5,unaff_SS,puVar3,uVar4);
  if (*(char *)0x66a9 == '\0') {
    puVar3 = local_102;
    uVar4 = unaff_SS;
    FUN_24dd_3e95(0x672e,unaff_DS);
    FUN_24dd_3f14(0xbc9e,0x24dd);
    uVar2 = 0x202c;
    cVar1 = FUN_202c_0843(puVar3,uVar4);
    if (cVar1 != '\0') {
      puVar3 = local_202;
      uVar4 = unaff_SS;
      FUN_24dd_3e95(0xbcbb,0x202c);
      FUN_24dd_3f14(0x672e,unaff_DS);
      FUN_24dd_3f14(0xbcbb,0x24dd);
      FUN_24dd_3eaf(0x10,param_1 + -0x94,unaff_SS,puVar3,uVar4);
      FUN_24dd_3eaf(0x14,0x2ea,unaff_DS,0xbcbd,0x24dd);
      goto LAB_1000_bef3;
    }
  }
  FUN_24dd_3eaf(0x10,param_1 + -0x94,unaff_SS,0xbca3,uVar2);
  FUN_24dd_3eaf(0x14,0x2ea,unaff_DS,0xbcaa,0x24dd);
LAB_1000_bef3:
  FUN_24dd_3eaf(0x10,param_1 + -0x83,unaff_SS,*(char *)0x66ae * 4 + 4,unaff_DS);
  FUN_24dd_3eaf(0x10,param_1 + -0x72,unaff_SS,*(char *)0x66af * 4 + 4,unaff_DS);
  FUN_24dd_3eaf(0x10,param_1 + -0x61,unaff_SS,*(char *)0x66a5 * 4 + 4,unaff_DS);
  FUN_24dd_3eaf(0x10,param_1 + -0x50,unaff_SS,*(char *)0x6716 * 4 + 4,unaff_DS);
  return;
}

