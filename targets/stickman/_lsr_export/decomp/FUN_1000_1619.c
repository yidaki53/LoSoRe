
void FUN_1000_1619(int param_1)

{
  undefined2 uVar1;
  undefined2 uVar2;
  int iVar3;
  
  uVar2 = 0x1000;
  uVar1 = 0x1624;
  FUN_42b5_04df();
  if (param_1 == 0) {
    FUN_1000_1514(uVar1,uVar2);
  }
  else if (0 < param_1) {
    iVar3 = 1;
    while( true ) {
      FUN_1000_1514();
      if (iVar3 == param_1) break;
      iVar3 = iVar3 + 1;
    }
  }
  FUN_1000_00e8();
  return;
}

