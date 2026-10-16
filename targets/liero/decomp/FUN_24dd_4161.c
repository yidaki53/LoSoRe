
int __cdecl16far FUN_24dd_4161(void)

{
  sbyte sVar1;
  uint in_AX;
  byte bVar2;
  undefined2 in_DX;
  byte bVar3;
  
  bVar2 = (byte)in_AX >> 3;
  bVar3 = (byte)((uint)in_DX >> 8);
  if ((bVar3 <= bVar2) && ((byte)(bVar2 - bVar3) < (byte)in_DX)) {
    sVar1 = (sbyte)(in_AX & 0xff07);
    bVar2 = (byte)((in_AX & 0xff07) >> 8);
    return CONCAT11(bVar2,bVar2 << sVar1 | bVar2 >> 8 - sVar1);
  }
  return (int)in_AX >> 0xf;
}

