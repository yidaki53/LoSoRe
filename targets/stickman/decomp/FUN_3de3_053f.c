
/* WARNING: Removing unreachable block (ram,0x0003e3a6) */

void FUN_3de3_053f(undefined4 param_1,undefined4 param_2)

{
  undefined2 uVar1;
  long lVar2;
  long lVar3;
  
  FUN_42b5_04df();
  uVar1 = (undefined2)((ulong)param_2 >> 0x10);
  lVar2 = FUN_3de3_0424((int)param_2,uVar1);
  lVar3 = FUN_3de3_0424((int)param_1,(int)((ulong)param_1 >> 0x10));
  if (lVar2 < lVar3) {
    lVar2 = lVar2 + 0x15180;
  }
  FUN_3de3_0493((int)param_2,uVar1,lVar2 - lVar3);
  return;
}

