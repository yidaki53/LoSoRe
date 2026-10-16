
void __cdecl16near FUN_235c_118c(void)

{
  int *piVar1;
  int *piVar2;
  int iVar3;
  int *piVar4;
  int *piVar5;
  undefined2 unaff_DS;
  
  piVar4 = (int *)0x6a58;
  piVar2 = (int *)*(undefined4 *)0x6e6c;
  iVar3 = 0x200;
  piVar5 = (int *)piVar2;
  do {
    piVar1 = piVar4;
    piVar4 = piVar4 + 1;
    *piVar5 = *piVar1 << 5;
    iVar3 = iVar3 + -1;
    piVar5 = piVar5 + 1;
  } while (iVar3 != 0);
  return;
}

