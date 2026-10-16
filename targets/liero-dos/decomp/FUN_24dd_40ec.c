
void __stdcall16far FUN_24dd_40ec(byte param_1,undefined4 param_2)

{
  byte *pbVar1;
  
  pbVar1 = (byte *)((uint)(param_1 >> 3) + (int)param_2);
  *pbVar1 = *pbVar1 | '\x01' << (param_1 & 7);
  return;
}

