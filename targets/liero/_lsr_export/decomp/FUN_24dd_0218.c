
void FUN_24dd_0218(void)

{
  code *pcVar1;
  
  FUN_24dd_021f();
  FUN_24dd_022a();
  pcVar1 = (code *)swi(0x21);
  (*pcVar1)();
  return;
}

