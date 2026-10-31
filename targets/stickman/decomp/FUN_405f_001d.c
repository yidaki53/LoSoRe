
bool __cdecl16far FUN_405f_001d(void)

{
  undefined2 unaff_DS;
  bool local_3;
  
  FUN_42b5_04df();
  if (*(int *)0xaaec == 0) {
    local_3 = true;
  }
  else {
    *(undefined1 *)0xaaef = 3;
    *(int *)0xaaf4 = *(int *)0xaaec + -1;
    FUN_428f_000b(0xaaee);
    local_3 = (*(byte *)0xaaee & 0x80) != 0;
  }
  return local_3;
}

