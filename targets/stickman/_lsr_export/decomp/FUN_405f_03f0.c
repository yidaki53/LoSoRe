
void __cdecl16far FUN_405f_03f0(void)

{
  undefined2 unaff_DS;
  
  FUN_42b5_04df();
  if (*(int *)0xaaec != 0) {
    FUN_405f_0000();
    *(undefined2 *)0xaaee = 0x600;
    *(int *)0xaaf4 = *(int *)0xaaec + -1;
    FUN_428f_000b(0xaaee);
  }
  return;
}

