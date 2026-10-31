
long __stdcall16far FUN_428f_00de(void)

{
  code *pcVar1;
  long lVar2;
  int iVar3;
  int in_CX;
  uint in_BX;
  
  pcVar1 = (code *)swi(0x21);
  iVar3 = (*pcVar1)();
  lVar2 = CONCAT22(iVar3,iVar3);
  if (iVar3 != -1) {
    lVar2 = (ulong)(uint)(iVar3 * in_CX) * (ulong)in_BX;
  }
  return lVar2;
}

