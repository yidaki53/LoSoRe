
undefined1 __stdcall16far FUN_235c_0a1e(char param_1)

{
  undefined2 unaff_DS;
  undefined1 local_4;
  undefined1 local_3;
  
  local_3 = 0;
  local_4 = 0;
  while( true ) {
    if (*(char *)((uint)local_4 * 10 + 0x6808) == param_1) {
      local_3 = 1;
    }
    if (local_4 == 7) break;
    local_4 = local_4 + 1;
  }
  return local_3;
}

