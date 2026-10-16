
void __stdcall16far FUN_1ec2_0e4a(undefined4 param_1,int param_2,int param_3)

{
  byte bVar1;
  byte *pbVar2;
  undefined2 uVar3;
  
  if ((((-1 < param_3) && (param_3 < 0x9e)) && (-1 < param_2)) && (param_2 < 0x9e)) {
    uVar3 = (undefined2)((ulong)param_1 >> 0x10);
    pbVar2 = (byte *)((int)param_1 + param_2 * 0x140 + param_3);
    bVar1 = *pbVar2;
    if ((0x9f < bVar1) && (bVar1 < 0xa4)) {
      *pbVar2 = bVar1 + 4;
    }
  }
  return;
}

