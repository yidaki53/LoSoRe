
void __cdecl16near FUN_410e_047c(void)

{
  char in_AL;
  char extraout_DL;
  undefined2 unaff_DS;
  
  thunk_FUN_410e_0609();
  if (in_AL == '\a') {
    FUN_410e_0609();
  }
  else if (((in_AL != '\b') && (in_AL != '\r')) &&
          ((in_AL == '\n' || (FUN_410e_0609(), *(byte *)0xeb0c < (byte)(extraout_DL + 1U))))) {
    FUN_410e_04d5();
  }
  thunk_FUN_410e_0609();
  return;
}

