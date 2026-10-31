
void __stdcall16far FUN_42b5_18c5(undefined2 param_1,undefined2 param_2,undefined4 param_3)

{
  code *pcVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  int unaff_BP;
  undefined1 in_CF;
  undefined1 in_ZF;
  undefined2 in_stack_00000000;
  
  FUN_42b5_18b6();
  if ((bool)in_ZF) {
    iVar4 = *(int *)((int)param_3 + 4);
    pcVar1 = (code *)swi(0x21);
    iVar2 = (*pcVar1)();
    iVar3 = iVar2;
    if (((bool)in_CF) || (iVar3 = unaff_BP, iVar2 != iVar4)) {
      *(int *)0x39c = iVar3;
    }
  }
  return;
}

