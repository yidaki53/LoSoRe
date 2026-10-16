
uint __cdecl16far FUN_249c_0180(void)

{
  code *pcVar1;
  uint uVar2;
  uint uVar3;
  
  pcVar1 = (code *)swi(0x21);
  uVar2 = (*pcVar1)();
  uVar3 = uVar2 & 0xff00;
  if ((char)uVar2 == -1) {
    uVar3 = uVar3 + 1;
  }
  return uVar3;
}

