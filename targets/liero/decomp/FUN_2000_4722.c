
void __cdecl16near FUN_2000_4722(void)

{
  undefined2 unaff_DS;
  uint local_4;
  
  FUN_235c_0aeb();
  local_4 = 0;
  while( true ) {
    if (*(char *)(local_4 + 0x67fc) != '\0') {
      FUN_235c_10a3(local_4 & 0xff);
    }
    if (local_4 == 7) break;
    local_4 = local_4 + 1;
  }
  return;
}

