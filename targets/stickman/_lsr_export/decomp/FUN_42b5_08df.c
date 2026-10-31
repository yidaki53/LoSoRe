
void __stdcall16far FUN_42b5_08df(int param_1,char *param_2,undefined4 param_3)

{
  char cVar1;
  int iVar2;
  int in_BX;
  char *pcVar3;
  undefined2 uVar4;
  undefined1 in_ZF;
  
  FUN_42b5_0776();
  uVar4 = (undefined2)((ulong)param_2 >> 0x10);
  pcVar3 = (char *)param_2;
  iVar2 = 0;
  if ((bool)in_ZF) {
    do {
      cVar1 = FUN_42b5_079a();
      if ((cVar1 == '\r') || (cVar1 == '\x1a')) break;
      in_BX = in_BX + 1;
      iVar2 = iVar2 + 1;
      pcVar3 = pcVar3 + 1;
      *pcVar3 = cVar1;
    } while (iVar2 != param_1);
  }
  pcVar3[-iVar2] = (char)iVar2;
  *(int *)((int)param_3 + 8) = in_BX;
  return;
}

