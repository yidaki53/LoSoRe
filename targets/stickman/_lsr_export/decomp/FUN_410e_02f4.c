
byte __cdecl16far FUN_410e_02f4(void)

{
  byte bVar1;
  
  bVar1 = in(0x61);
  out(0x61,bVar1 & 0xfc);
  return bVar1 & 0xfc;
}

