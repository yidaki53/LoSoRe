
uint __stdcall16far FUN_42b5_1279(uint param_1)

{
  uint uVar1;
  uint extraout_DX;
  
  FUN_42b5_12c8();
  uVar1 = 0;
  if (param_1 != 0) {
    uVar1 = extraout_DX % param_1;
  }
  return uVar1;
}

