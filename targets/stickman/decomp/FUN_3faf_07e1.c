
undefined1 __stdcall16far FUN_3faf_07e1(void)

{
  undefined1 uVar1;
  undefined2 uVar2;
  undefined2 uVar3;
  int iVar4;
  undefined2 extraout_DX;
  undefined2 uVar5;
  undefined2 in_BX;
  int unaff_BP;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  undefined4 uVar6;
  
  FUN_42b5_081a();
  FUN_42b5_08df(0xff,unaff_BP + -0x20e,unaff_SS);
  FUN_42b5_081a();
  FUN_42b5_08df(0xff,unaff_BP + -0x20e,unaff_SS);
  FUN_42b5_081a();
  FUN_42b5_08df(0xff,unaff_BP + -0x20e,unaff_SS);
  FUN_42b5_081a();
  FUN_42b5_08df(0xff,unaff_BP + -0x20e,unaff_SS);
  FUN_42b5_081a();
  FUN_42b5_08df(0xff,unaff_BP + -0x20e,unaff_SS);
  FUN_42b5_081a();
  FUN_42b5_08df(0xff,unaff_BP + -0x20e,unaff_SS);
  FUN_42b5_081a();
  FUN_42b5_08df(0xff,unaff_BP + -0x20e,unaff_SS);
  FUN_42b5_081a();
  uVar5 = extraout_DX;
  uVar2 = FUN_42b5_09f6();
  *(undefined2 *)(unaff_BP + -0x10e) = uVar2;
  *(undefined2 *)(unaff_BP + -0x10c) = in_BX;
  *(undefined2 *)(unaff_BP + -0x10a) = uVar5;
  FUN_42b5_081a();
  uVar5 = *(undefined2 *)(unaff_BP + -0x10c);
  uVar2 = *(undefined2 *)(unaff_BP + -0x10a);
  uVar3 = FUN_42b5_1245();
  *(undefined2 *)(unaff_BP + -0x10e) = uVar3;
  *(undefined2 *)(unaff_BP + -0x10c) = uVar5;
  *(undefined2 *)(unaff_BP + -0x10a) = uVar2;
  uVar5 = *(undefined2 *)(unaff_BP + -0x10a);
  uVar2 = FUN_42b5_125f();
  *(undefined2 *)0xaae8 = uVar2;
  *(undefined2 *)0xaaea = uVar5;
  FUN_42b5_08df(0xff,unaff_BP + -0x20e,unaff_SS);
  FUN_42b5_081a();
  FUN_42b5_08df(0xff,unaff_BP + -0x20e,unaff_SS);
  FUN_42b5_081a();
  FUN_42b5_08df(0xff,unaff_BP + -0x20e,unaff_SS);
  FUN_42b5_081a();
  FUN_42b5_08df(0xff,unaff_BP + -0x20e,unaff_SS);
  FUN_42b5_081a();
  uVar6 = FUN_42b5_17b1(unaff_BP + -0x104,unaff_SS);
  *(undefined2 *)(unaff_BP + -0x108) = (int)uVar6;
  *(undefined2 *)(unaff_BP + -0x106) = (int)((ulong)uVar6 >> 0x10);
  if (*(int *)(unaff_BP + -0x104) == 0) {
    *(undefined2 *)0xa8e3 = 0x4b00;
    *(undefined2 *)0xa8e5 = 0;
  }
  else {
    uVar5 = *(undefined2 *)(unaff_BP + -0x106);
    *(undefined2 *)0xa8e3 = *(undefined2 *)(unaff_BP + -0x108);
    *(undefined2 *)0xa8e5 = uVar5;
  }
  uVar1 = FUN_42b5_0955();
  *(undefined1 *)0xa8e2 = uVar1;
  FUN_42b5_081a();
  FUN_42b5_08df(0xff,unaff_BP + -0x20e,unaff_SS);
  FUN_42b5_081a();
  FUN_42b5_08df(0xff,unaff_BP + -0x20e,unaff_SS);
  FUN_42b5_081a();
  FUN_42b5_08df(0xff,unaff_BP + -0x20e,unaff_SS);
  FUN_42b5_081a();
  FUN_42b5_08df(0xff,unaff_BP + -0x20e,unaff_SS);
  FUN_42b5_081a();
  FUN_42b5_08df(0xff,unaff_BP + -0x20e,unaff_SS);
  FUN_42b5_081a();
  FUN_42b5_08df(0xff,unaff_BP + -0x20e,unaff_SS);
  FUN_42b5_081a();
  FUN_42b5_08df(0xff,unaff_BP + -0x20e,unaff_SS);
  FUN_42b5_081a();
  FUN_42b5_08df(0xff,unaff_BP + -0x20e,unaff_SS);
  FUN_42b5_081a();
  FUN_42b5_08df(0xff,unaff_BP + -0x20e,unaff_SS);
  FUN_42b5_081a();
  FUN_42b5_08df(0xff,0xa8e8,unaff_DS);
  FUN_42b5_081a();
  FUN_42b5_05bf();
  iVar4 = FUN_42b5_04a2();
  if (iVar4 == 0) {
    *(undefined1 *)(unaff_BP + -1) = 1;
  }
  *(undefined1 *)0xa8e7 = 0xff;
  return *(undefined1 *)(unaff_BP + -1);
}

