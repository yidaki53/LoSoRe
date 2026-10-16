
void __cdecl16near FUN_24dd_0642(void)

{
  undefined2 *puVar1;
  undefined2 *puVar2;
  int iVar3;
  undefined2 *unaff_SI;
  undefined2 *puVar4;
  undefined2 unaff_DS;
  
  puVar4 = (undefined2 *)(*(int *)0xd8 + -0xc);
  *(undefined2 *)0xd8 = puVar4;
  for (iVar3 = 6; iVar3 != 0; iVar3 = iVar3 + -1) {
    puVar2 = puVar4;
    puVar4 = puVar4 + 1;
    puVar1 = unaff_SI;
    unaff_SI = unaff_SI + 1;
    *puVar2 = *puVar1;
  }
  return;
}

