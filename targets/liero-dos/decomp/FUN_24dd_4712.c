
void __cdecl16near FUN_24dd_4712(void)

{
  ulong uVar1;
  uint in_AX;
  byte bVar2;
  uint in_BX;
  uint unaff_SI;
  byte *unaff_DI;
  undefined2 unaff_ES;
  char cVar3;
  
  do {
    uVar1 = (ulong)in_BX;
    in_BX = in_BX / unaff_SI;
    uVar1 = uVar1 % (ulong)unaff_SI << 0x10 | (ulong)in_AX;
    in_AX = (uint)(uVar1 / unaff_SI);
    cVar3 = (char)(uVar1 % (ulong)unaff_SI);
    bVar2 = cVar3 + 0x30;
    if (0x39 < bVar2) {
      bVar2 = cVar3 + 0x37;
    }
    unaff_DI = unaff_DI + -1;
    *unaff_DI = bVar2;
  } while (in_AX != 0 || in_BX != 0);
  return;
}

