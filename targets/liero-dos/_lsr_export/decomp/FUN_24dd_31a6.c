
void __cdecl16near FUN_24dd_31a6(void)

{
  uint uVar1;
  longdouble lVar2;
  undefined2 unaff_DS;
  longdouble in_ST0;
  
  lVar2 = (longdouble)0;
  *(uint *)0x7b40 =
       (uint)NAN(in_ST0) << 8 | (uint)(in_ST0 < lVar2) << 9 | (uint)(in_ST0 != lVar2) << 10 |
       (uint)(in_ST0 == lVar2) << 0xe;
  uVar1 = *(uint *)0x7b40;
  if ((((uVar1 & 0x4500) != 0) && ((uVar1 & 0x4000) != 0)) && ((uVar1 & 0x400) != 0)) {
    return;
  }
  return;
}

