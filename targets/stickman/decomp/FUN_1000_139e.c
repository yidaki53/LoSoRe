
void FUN_1000_139e(int param_1,int param_2)

{
  int *piVar1;
  char cVar2;
  int iVar3;
  int *piVar4;
  undefined2 uVar5;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  undefined1 *puVar6;
  undefined1 local_108 [256];
  int *local_8;
  int local_4;
  
  _local_8 = (int *)CONCAT22(0x13a9,local_8);
  FUN_42b5_04df();
  FUN_3de3_0b67(param_1 + 1,param_2);
  FUN_3de3_002d(0x136a,0x3de3);
  cVar2 = *(char *)(param_1 * 0x50 + param_2 + 0x1f6f);
  if (cVar2 == '\x04') {
    *(undefined1 *)(param_1 * 0x50 + param_2 + 0x1f6f) = 0;
  }
  else if (cVar2 == '\x0e') {
    *(undefined1 *)(param_1 * 0x50 + param_2 + 0x1f6f) = 0;
    FUN_1000_0007(0x1376,0x3de3);
  }
  local_4 = 1;
  while( true ) {
    iVar3 = local_4 * 0x275;
    _local_8 = (int *)CONCAT22(unaff_DS,(int *)(iVar3 + 0x459));
    if ((((*_local_8 <= param_2) && (param_2 <= *_local_8 + *(int *)(iVar3 + 0x465) + -1)) &&
        (*(int *)(iVar3 + 0x45b) <= param_1)) &&
       (param_1 <= *(int *)(iVar3 + 0x45b) + *(int *)(iVar3 + 0x467) + -1)) {
      *(int *)(iVar3 + 0x461) = *(int *)(iVar3 + 0x461) + -1;
      FUN_3de3_002d(0x1397,0x3de3);
      uVar5 = (undefined2)((ulong)_local_8 >> 0x10);
      piVar4 = (int *)_local_8;
      if (piVar4[4] < 1) {
        if (piVar4[2] < 0x15) {
          piVar1 = (int *)(piVar4[2] * 2 + 0x509);
          *piVar1 = *piVar1 + 1;
        }
        FUN_3de3_0b67(piVar4[1] + 1,*_local_8);
        puVar6 = local_108;
        uVar5 = unaff_SS;
        FUN_42b5_0bc4(0x1397,0x3de3);
        FUN_42b5_0c51((int)(int *)_local_8 + 0x135,(int)((ulong)_local_8 >> 0x10));
        FUN_3de3_002d(puVar6,uVar5);
        FUN_1000_132a();
        *_local_8 = 0;
      }
    }
    if (local_4 == 10) break;
    local_4 = local_4 + 1;
  }
  FUN_410e_029c(0xfa);
  FUN_1000_04bc(param_1,param_2);
  FUN_3de3_002d(0x1399,0x410e);
  return;
}

