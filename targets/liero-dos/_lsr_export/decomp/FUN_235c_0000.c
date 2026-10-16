
undefined1 FUN_235c_0000(undefined1 param_1)

{
  byte bVar1;
  undefined2 unaff_DS;
  
  do {
    bVar1 = in(*(undefined2 *)0x67d4);
  } while ((bVar1 & 0x80) != 0);
  out(*(undefined2 *)0x67d4,param_1);
  return param_1;
}

