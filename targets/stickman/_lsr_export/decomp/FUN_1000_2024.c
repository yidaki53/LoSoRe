
void __cdecl16near FUN_1000_2024(void)

{
  char cVar1;
  int iVar2;
  int iVar3;
  undefined2 unaff_DS;
  int iVar4;
  undefined2 uVar5;
  undefined2 uVar6;
  
  uVar6 = 0x1000;
  uVar5 = 0x202f;
  FUN_42b5_04df();
  if (*(char *)0x3a6 == '\0') {
    iVar4 = 1;
    while ((iVar4 < 6 && (*(int *)(iVar4 * 0x27 + 0x25dd) != 0))) {
      iVar4 = iVar4 + 1;
    }
    if (((iVar4 < 6) && (0 < *(int *)0x3b2)) &&
       (cVar1 = FUN_1000_0c8f(*(int *)0x3b0 + 1,*(int *)0x3ae + -2), cVar1 == '\0')) {
      *(int *)0x3b2 = *(int *)0x3b2 + -1;
      FUN_1000_0759(iVar4,uVar5,uVar6);
      FUN_3de3_0bea(0x1feb,0x42b5,*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
      FUN_3de3_0bea(0x1ffa,0x3de3,*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
      iVar2 = *(int *)0x3ae + -2;
      iVar3 = *(int *)0x3b0 + 1;
      FUN_3de3_002d(0x2006,0x3de3);
      FUN_3de3_0b67(iVar3 + 1,iVar2);
      FUN_3de3_002d(0x2011,0x3de3);
      FUN_3de3_002d(0x2013,0x3de3);
      FUN_3de3_0b67(*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
      *(int *)(iVar4 * 0x27 + 0x25d9) = iVar2;
      *(int *)(iVar4 * 0x27 + 0x25db) = iVar3;
      *(undefined2 *)(iVar4 * 0x27 + 0x25dd) = 0xffff;
      FUN_42b5_0bde(0x20,iVar4 * 0x27 + 0x25df,unaff_DS,0x2018,0x3de3);
    }
  }
  return;
}

