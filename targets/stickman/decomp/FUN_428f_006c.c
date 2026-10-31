
void __stdcall16far FUN_428f_006c(uint *param_1,uint *param_2,uint *param_3,undefined2 *param_4)

{
  code *pcVar1;
  uint uVar2;
  undefined2 in_CX;
  byte extraout_DL;
  byte extraout_DH;
  
  pcVar1 = (code *)swi(0x21);
  uVar2 = (*pcVar1)();
  *param_1 = uVar2 & 0xff;
  *param_2 = (uint)extraout_DL;
  *param_3 = (uint)extraout_DH;
  *param_4 = in_CX;
  return;
}

