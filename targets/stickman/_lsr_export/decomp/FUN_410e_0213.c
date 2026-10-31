
void __stdcall16far FUN_410e_0213(char param_1,char param_2)

{
  undefined2 unaff_DS;
  
  if ((((!CARRY1(param_2 - 1U,*(byte *)0xeb0a)) &&
       ((byte)((param_2 - 1U) + *(byte *)0xeb0a) <= *(byte *)0xeb0c)) &&
      (!CARRY1(param_1 - 1U,*(byte *)0xeb0b))) &&
     ((byte)((param_1 - 1U) + *(byte *)0xeb0b) <= *(byte *)0xeb0d)) {
    thunk_FUN_410e_0609();
  }
  return;
}

