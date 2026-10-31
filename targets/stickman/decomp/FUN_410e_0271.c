
void __stdcall16far FUN_410e_0271(byte param_1)

{
  undefined2 unaff_DS;
  
  *(byte *)0xeb08 = *(byte *)0xeb08 & 0x8f;
  *(byte *)0xeb08 = *(byte *)0xeb08 | (param_1 & 7) << 4;
  return;
}

