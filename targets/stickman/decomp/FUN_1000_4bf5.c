
void __cdecl16near FUN_1000_4bf5(void)

{
  undefined2 unaff_DS;
  
  FUN_42b5_04df();
  FUN_3de3_002d(0x4be6,0x42b5);
  if (*(char *)0x594 == '\0') {
    FUN_3de3_0bea(0x4bf1,0x3de3,0xc,0x1c);
  }
  else {
    FUN_3de3_0bea(0x4bf1,0x3de3,0xc,0x11);
  }
  *(bool *)0x594 = *(char *)0x594 == '\0';
  if (*(char *)0x594 == '\0') {
    FUN_3de3_0bea(0x4bf3,0x3de3,0xc,0x1c);
  }
  else {
    FUN_3de3_0bea(0x4bf3,0x3de3,0xc,0x11);
  }
  return;
}

