
void __stdcall16far FUN_249c_01c3(void)

{
  code *pcVar1;
  
  pcVar1 = (code *)swi(0x15);
  (*pcVar1)();
  return;
}

