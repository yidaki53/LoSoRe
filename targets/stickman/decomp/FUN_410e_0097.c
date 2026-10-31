
void __cdecl16near FUN_410e_0097(void)

{
  undefined2 in_AX;
  char extraout_DL;
  
  DAT_0000_0487 = DAT_0000_0487 & 0xfe;
  if (((byte)in_AX != 7) && (3 < (byte)in_AX)) {
    in_AX = CONCAT11((char)((uint)in_AX >> 8),3);
  }
  FUN_410e_0609();
  if ((char)((uint)in_AX >> 8) != '\0') {
    FUN_410e_0609();
    FUN_410e_0609();
    if (extraout_DL == '*') {
      DAT_0000_0487 = DAT_0000_0487 | 1;
      FUN_410e_0609();
      FUN_410e_0609();
    }
  }
  return;
}

