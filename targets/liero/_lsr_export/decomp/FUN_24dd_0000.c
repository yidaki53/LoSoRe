
void __cdecl16far FUN_24dd_0000(void)

{
  code *pcVar1;
  undefined2 uVar2;
  int iVar3;
  undefined2 in_BX;
  undefined2 *puVar4;
  undefined2 unaff_ES;
  int unaff_SS;
  
  DAT_2971_640c = unaff_ES;
  FUN_24dd_492c();
  FUN_24dd_00b1();
  uVar2 = DAT_2971_640c;
  DAT_2971_63de = ((uint)&stack0x0013 >> 4) + unaff_SS;
  DAT_2971_63e2 = DAT_2971_63de + DAT_2971_63d8;
  DAT_2971_63f4 = *(undefined2 *)0x2;
  DAT_2971_63fe = 0xd6;
  DAT_2971_6400 = 0x24dd;
  puVar4 = (undefined2 *)0x7af0;
  iVar3 = 0x13;
  DAT_2971_63e0 = DAT_2971_63de;
  DAT_2971_63ec = DAT_2971_63e2;
  DAT_2971_63f0 = DAT_2971_63e2;
  DAT_2971_63f8 = DAT_2971_63e2;
  do {
    pcVar1 = (code *)swi(0x21);
    (*pcVar1)();
    *puVar4 = in_BX;
    puVar4[1] = uVar2;
    puVar4 = puVar4 + 2;
    iVar3 = iVar3 + -1;
  } while (iVar3 != 0);
  pcVar1 = (code *)swi(0x21);
  (*pcVar1)();
  pcVar1 = (code *)swi(0x21);
  (*pcVar1)();
  pcVar1 = (code *)swi(0x21);
  (*pcVar1)();
  pcVar1 = (code *)swi(0x21);
  (*pcVar1)();
  FUN_24dd_3639();
  FUN_24dd_36b7();
  FUN_24dd_3639();
  FUN_24dd_36bc();
  return;
}

