
undefined4 FUN_235c_06d7(uint param_1,int param_2,uint param_3,int param_4)

{
  undefined2 local_6;
  undefined2 local_4;
  
  if ((param_4 < param_2) || ((param_4 <= param_2 && (param_3 < param_1)))) {
    local_6 = param_3;
    local_4 = param_4;
  }
  else {
    local_6 = param_1;
    local_4 = param_2;
  }
  return CONCAT22(local_4,local_6);
}

