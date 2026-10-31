
void __cdecl16far FUN_3de3_18e2(void)

{
  char cVar1;
  undefined2 uVar2;
  undefined2 in_DX;
  undefined2 uVar3;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  undefined1 uVar4;
  long lVar5;
  undefined1 *puVar6;
  undefined1 *puVar7;
  undefined1 *puVar8;
  undefined2 uVar9;
  undefined1 local_406 [256];
  undefined1 local_306 [256];
  undefined1 local_206 [256];
  char local_106 [256];
  undefined4 local_6;
  
  local_6._2_2_ = 0x3de3;
  local_6._0_2_ = 0xf71d;
  FUN_42b5_04df();
  uVar4 = &stack0x0000 == (undefined1 *)0x406;
  uVar2 = FUN_4170_0096();
  *(undefined2 *)0xa7d2 = uVar2;
  *(undefined2 *)0xa7d4 = in_DX;
  puVar8 = local_406;
  puVar7 = local_206;
  uVar3 = unaff_SS;
  uVar9 = unaff_SS;
  FUN_4170_05ea(0x187a,0x4170);
  FUN_42b5_0c51(0x187c,0x4170);
  puVar6 = local_306;
  uVar2 = unaff_SS;
  FUN_4170_05ea(0x187e,0x42b5);
  FUN_42b5_0c51(puVar6,uVar2);
  FUN_4170_0e7d(puVar7,uVar3);
  FUN_42b5_0bde(0xff,local_106,unaff_SS,puVar8,uVar9);
  FUN_42b5_0cc9(0x187c,0x42b5,local_106,unaff_SS);
  if ((bool)uVar4) {
    FUN_42b5_0bde(0xff,0xa7d6,unaff_DS,0x1880,0x42b5);
  }
  else {
    FUN_42b5_0bde(0xff,0xa7d6,unaff_DS,local_106,unaff_SS);
  }
  FUN_42b5_1300();
  *(undefined2 *)0xa7ca = 0xf;
  *(undefined2 *)0xa7cc = 0;
  uVar3 = 0x4170;
  uVar2 = FUN_4170_079f(0x188c,0x42b5);
  *(undefined2 *)0xaaec = uVar2;
  if (*(int *)0xaaec == -1) {
    *(undefined2 *)0xaaec = 0;
    puVar8 = local_206;
    uVar2 = unaff_SS;
    FUN_4170_05ea(0x1891,0x4170);
    uVar3 = 0x42b5;
    FUN_42b5_0bde(0xff,local_106,unaff_SS,puVar8,uVar2);
    if (local_106[0] != '\0') {
      uVar3 = 0x3faf;
      cVar1 = FUN_3faf_002b(local_106,unaff_SS);
      if (cVar1 != '\0') {
        FUN_3de3_0f2d();
        goto LAB_3de3_1a63;
      }
    }
    puVar8 = local_206;
    uVar2 = unaff_SS;
    FUN_4170_05ea(0x1896,uVar3);
    uVar3 = 0x42b5;
    FUN_42b5_0bde(0xff,local_106,unaff_SS,puVar8,uVar2);
    if (local_106[0] != '\0') {
      uVar3 = 0x3faf;
      cVar1 = FUN_3faf_033a(local_106,unaff_SS);
      if (cVar1 != '\0') {
        FUN_3de3_0f2d();
        goto LAB_3de3_1a63;
      }
    }
    puVar8 = local_206;
    uVar2 = unaff_SS;
    FUN_4170_05ea(0x189a,uVar3);
    uVar3 = 0x42b5;
    FUN_42b5_0bde(0xff,local_106,unaff_SS,puVar8,uVar2);
    if (local_106[0] != '\0') {
      uVar3 = 0x3faf;
      cVar1 = FUN_3faf_0651(local_106,unaff_SS);
      if (cVar1 != '\0') {
        FUN_3de3_0f2d();
        goto LAB_3de3_1a63;
      }
    }
    FUN_3de3_1647();
  }
LAB_3de3_1a63:
  local_6 = FUN_4170_079f(0x18a0,uVar3);
  if (local_6 != 0x7fffffff) {
    *(undefined2 *)0xa7ca = (int)local_6;
    *(undefined2 *)0xa7cc = (int)((ulong)local_6 >> 0x10);
  }
  FUN_3de3_1029();
  lVar5 = FUN_4170_079f(0x18a4,0x4170);
  if (lVar5 != 0x7fffffff) {
    *(undefined2 *)0xa7ce = (int)lVar5;
    *(undefined2 *)0xa7d0 = (int)((ulong)lVar5 >> 0x10);
  }
  if ((0 < *(int *)0xa7d0) || ((-1 < *(int *)0xa7d0 && (0x9600 < *(uint *)0xa7ce)))) {
    *(undefined2 *)0xa7ce = 0x9600;
    *(undefined2 *)0xa7d0 = 0;
  }
  local_6 = lVar5;
  cVar1 = FUN_405f_02ed(*(undefined2 *)0xa7ce);
  if (cVar1 == '\0') {
    FUN_3de3_0e5b(0x18a9,0x405f);
  }
  FUN_3de3_1256();
  puVar8 = local_206;
  uVar2 = unaff_SS;
  FUN_42b5_0bc4(0x18cc,0x405f);
  FUN_42b5_0c51(0xa7d6,unaff_DS);
  FUN_42b5_0c51(0x18d9,0x42b5);
  puVar7 = local_306;
  FUN_42b5_0cf4(*(byte *)0xa8e7 + 0x30);
  FUN_42b5_0c51(puVar7,unaff_SS);
  FUN_3de3_00e2(puVar8,uVar2);
  return;
}

