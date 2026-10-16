
undefined1 __cdecl16far FUN_24ba_00d8(void)

{
  undefined2 unaff_DS;
  byte local_4;
  
  local_4 = 0xab;
  while( true ) {
    if (*(char *)(local_4 + 0x783b) != '\0') {
      return 1;
    }
    if (local_4 == 1) break;
    local_4 = local_4 - 1;
  }
  return 0;
}

