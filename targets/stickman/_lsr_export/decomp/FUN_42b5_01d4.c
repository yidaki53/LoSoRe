
void FUN_42b5_01d4(void)

{
  code *pcVar1;
  
  FUN_42b5_01df();
  pcVar1 = (code *)swi(0x21);
  (*pcVar1)();
  return;
}

