
void __cdecl16near FUN_24dd_455e(void)

{
  uint uVar1;
  uint in_AX;
  uint in_DX;
  bool bVar2;
  
  if (in_AX != 0 || in_DX != 0) {
    if ((int)in_DX < 0) {
      bVar2 = in_AX != 0;
      in_AX = -in_AX;
      in_DX = -(uint)bVar2 - in_DX;
    }
    uVar1 = in_AX;
    if ((in_DX == 0) && (uVar1 = 0, in_DX = in_AX, (char)(in_AX >> 8) == '\0')) {
      in_DX = in_AX << 8;
    }
    while (-1 < (int)in_DX) {
      in_DX = in_DX * 2 + (uint)CARRY2(uVar1,uVar1);
      uVar1 = uVar1 * 2;
    }
  }
  return;
}

