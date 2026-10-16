
void __cdecl16near FUN_235c_11aa(void)

{
  int *piVar1;
  undefined1 *puVar2;
  int iVar3;
  int *piVar4;
  undefined1 *puVar5;
  undefined2 unaff_DS;
  
  piVar4 = (int *)0x6a58;
  puVar2 = (undefined1 *)*(undefined4 *)0x6e6c;
  iVar3 = 0x200;
  puVar5 = (undefined1 *)puVar2;
  do {
    piVar1 = piVar4;
    piVar4 = piVar4 + 1;
    *puVar5 = *(undefined1 *)(*piVar1 + 0x7286);
    iVar3 = iVar3 + -1;
    puVar5 = puVar5 + 1;
  } while (iVar3 != 0);
  return;
}

