
void __cdecl16near FUN_1000_4b69(void)

{
  undefined2 unaff_DS;
  
  FUN_42b5_04df();
  FUN_3de3_002d(0x4b5a,0x42b5);
  if (*(char *)0x593 == '\0') {
    FUN_3de3_0bea(0x4b65,0x3de3,8,0x1c);
  }
  else {
    FUN_3de3_0bea(0x4b65,0x3de3,8,0x11);
  }
  *(bool *)0x593 = *(char *)0x593 == '\0';
  if (*(char *)0x593 == '\0') {
    FUN_3de3_0bea(0x4b67,0x3de3,8,0x1c);
  }
  else {
    FUN_3de3_0bea(0x4b67,0x3de3,8,0x11);
  }
  return;
}

