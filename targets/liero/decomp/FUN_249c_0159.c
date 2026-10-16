
void __cdecl16far FUN_249c_0159(void)

{
  code *pcVar1;
  
  pcVar1 = (code *)swi(0x10);
  (*pcVar1)();
  pcVar1 = (code *)swi(0x10);
  (*pcVar1)();
  FUN_249c_0000();
  return;
}

