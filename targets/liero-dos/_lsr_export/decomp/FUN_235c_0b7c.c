
void __cdecl16near FUN_235c_0b7c(void)

{
  undefined2 unaff_DS;
  undefined2 local_6;
  undefined2 local_4;
  
  local_4 = -0x400;
  while( true ) {
    local_6 = local_4;
    if (local_4 < -0x80) {
      local_6 = -0x80;
    }
    if (0x7f < local_6) {
      local_6 = 0x7f;
    }
    *(char *)(local_4 + 0x7286) = (char)local_6 + -0x80;
    if (local_4 == 0x400) break;
    local_4 = local_4 + 1;
  }
  return;
}

