
undefined1 FUN_1000_10fa(int param_1,int param_2)

{
  char cVar1;
  undefined2 unaff_DS;
  undefined1 local_3;
  
  FUN_42b5_04df();
  if ((param_2 < 1) || (0x4f < param_2)) {
    *(undefined2 *)0x3ac = 0;
    local_3 = 1;
  }
  else {
    cVar1 = FUN_1000_0c8f(param_1,param_2);
    if (((cVar1 == '\0') && (cVar1 = FUN_1000_0c8f(param_1 + 1,param_2), cVar1 == '\0')) &&
       (cVar1 = FUN_1000_0c8f(param_1 + 2,param_2), cVar1 == '\0')) {
      local_3 = 0;
    }
    else {
      FUN_1000_0f1f(param_1,param_2);
      FUN_1000_0f1f(param_1 + 1,param_2);
      FUN_1000_0f1f(param_1 + 2,param_2);
      cVar1 = FUN_1000_0c8f(param_1,param_2);
      if (((cVar1 == '\0') && (cVar1 = FUN_1000_0c8f(param_1 + 1,param_2), cVar1 == '\0')) &&
         (cVar1 = FUN_1000_0c8f(param_1 + 2,param_2), cVar1 == '\0')) {
        local_3 = 0;
      }
      else {
        local_3 = 1;
      }
    }
  }
  return local_3;
}

