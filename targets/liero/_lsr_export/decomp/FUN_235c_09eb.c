
void __stdcall16far FUN_235c_09eb(char param_1)

{
  undefined2 unaff_DS;
  undefined1 local_3;
  
  local_3 = 0;
  while( true ) {
    if (*(char *)((uint)local_3 * 10 + 0x6808) == param_1) {
      FUN_235c_091d(local_3);
      *(char *)0x67ce = *(char *)0x67ce + -1;
    }
    if (local_3 == 7) break;
    local_3 = local_3 + 1;
  }
  return;
}

