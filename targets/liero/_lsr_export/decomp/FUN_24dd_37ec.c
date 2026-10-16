
void __cdecl16near FUN_24dd_37ec(void)

{
  undefined4 uVar1;
  code *in_AX;
  undefined2 in_CX;
  undefined2 in_DX;
  int in_BX;
  int iVar2;
  undefined2 unaff_DI;
  undefined2 unaff_ES;
  undefined2 unaff_DS;
  code *pcVar3;
  
  if (*(int *)0x6410 == 0) {
    if (*(int *)(in_BX + 2) != -0x284f) {
      *(undefined2 *)0x6410 = 0x68;
      return;
    }
    iVar2 = *(int *)(in_BX + 8);
    if (iVar2 == *(int *)(in_BX + 10)) goto LAB_24dd_3830;
    while( true ) {
      uVar1 = *(undefined4 *)(in_BX + 0xc);
      pcVar3 = (code *)(*in_AX)(in_BX,unaff_ES,unaff_DS);
      in_AX = (code *)pcVar3;
      *(int *)(in_BX + 8) = (iVar2 + (int)uVar1) - (int)((ulong)pcVar3 >> 0x10);
      if (in_AX == (code *)0x0) break;
LAB_24dd_3830:
      FUN_24dd_396c(in_BX,unaff_ES,unaff_DI,in_DX,in_CX);
      iVar2 = *(int *)(in_BX + 8);
      if (iVar2 == *(int *)(in_BX + 10)) {
        return;
      }
    }
  }
  return;
}

