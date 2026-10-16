
void __stdcall16far FUN_1ec2_0dc8(undefined4 param_1,char param_2,int param_3,int param_4)

{
  if (param_2 != '\0') {
    if ((((-1 < param_4) && (param_4 < 0x9e)) && (-1 < param_3)) && (param_3 < 0x9e)) {
      *(char *)((int)param_1 + param_3 * 0x140 + param_4) = param_2;
    }
  }
  return;
}

