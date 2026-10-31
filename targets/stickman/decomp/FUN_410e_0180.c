
void __stdcall16far FUN_410e_0180(byte param_1,byte param_2,byte param_3,byte param_4)

{
  undefined2 unaff_DS;
  
  if ((((param_4 <= param_2) && (param_3 <= param_1)) && (-1 < (char)(param_4 - 1))) &&
     (((-1 < (char)(param_3 - 1) && ((byte)(param_2 - 1) <= *(byte *)0xeb10)) &&
      ((byte)(param_1 - 1) <= *(byte *)0xeb11)))) {
    *(undefined2 *)0xeb0a = CONCAT11(param_3 - 1,param_4 - 1);
    *(undefined2 *)0xeb0c = CONCAT11(param_1 - 1,param_2 - 1);
    thunk_FUN_410e_0609();
  }
  return;
}

