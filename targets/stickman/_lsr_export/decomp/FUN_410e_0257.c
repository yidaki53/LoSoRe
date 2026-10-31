
void __stdcall16far FUN_410e_0257(byte param_1)

{
  undefined2 unaff_DS;
  
  if ((param_1 & 0xf0) != 0) {
    param_1 = param_1 & 0xf | 0x80;
  }
  *(byte *)0xeb08 = *(byte *)0xeb08 & 0x70;
  *(byte *)0xeb08 = *(byte *)0xeb08 | param_1;
  return;
}

