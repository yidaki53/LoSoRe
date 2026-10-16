
void __cdecl16near FUN_24dd_46f6(void)

{
  ulong uVar1;
  uint in_AX;
  byte bVar2;
  uint in_DX;
  byte *unaff_DI;
  undefined2 unaff_ES;
  char cVar3;
  
  if ((int)in_DX < 0) {
    FUN_24dd_4712();
    unaff_DI[-1] = 0x2d;
    return;
  }
  do {
    uVar1 = (ulong)in_DX;
    in_DX = in_DX / 10;
    uVar1 = uVar1 % 10 << 0x10 | (ulong)in_AX;
    in_AX = (uint)(uVar1 / 10);
    cVar3 = (char)(uVar1 % 10);
    bVar2 = cVar3 + 0x30;
    if (0x39 < bVar2) {
      bVar2 = cVar3 + 0x37;
    }
    unaff_DI = unaff_DI + -1;
    *unaff_DI = bVar2;
  } while (in_AX != 0 || in_DX != 0);
  return;
}

