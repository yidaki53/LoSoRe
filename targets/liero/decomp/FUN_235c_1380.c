
bool __cdecl16far FUN_235c_1380(void)

{
  code *pcVar1;
  char cVar2;
  
  pcVar1 = (code *)swi(0x2f);
  cVar2 = (*pcVar1)();
  return cVar2 == -0x80;
}

