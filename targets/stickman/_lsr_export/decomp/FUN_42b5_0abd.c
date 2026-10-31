
undefined1 __stdcall16far FUN_42b5_0abd(undefined4 param_1)

{
  byte bVar1;
  undefined1 uVar2;
  byte bVar3;
  int in_BX;
  undefined1 in_ZF;
  
  bVar3 = 0;
  FUN_42b5_0776();
  if ((bool)in_ZF) {
    while( true ) {
      bVar1 = FUN_42b5_079a();
      if ((bVar1 == 0x1a) || (((bVar3 & 1) != 0 && (bVar1 == 0xd)))) break;
      if (((bVar3 & 2) == 0) || (0x20 < bVar1)) goto LAB_42b5_0ae8;
      in_BX = in_BX + 1;
    }
    uVar2 = 1;
  }
  else {
LAB_42b5_0ae8:
    uVar2 = 0;
  }
  *(int *)((int)param_1 + 8) = in_BX;
  return uVar2;
}

