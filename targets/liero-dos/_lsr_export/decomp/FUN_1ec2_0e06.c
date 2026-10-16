
void __stdcall16far FUN_1ec2_0e06(undefined4 param_1,byte param_2,int param_3,int param_4)

{
  if (param_2 != 0) {
    if ((((-1 < param_4) && (param_4 < 0x9e)) && (-1 < param_3)) && (param_3 < 0x9e)) {
      if (param_2 < 0x27) {
        param_2 = param_2 + 9;
      }
      *(byte *)((int)param_1 + param_3 * 0x140 + param_4) = param_2;
    }
  }
  return;
}

