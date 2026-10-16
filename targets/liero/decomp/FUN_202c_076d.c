
void __stdcall16far FUN_202c_076d(undefined2 param_1,undefined2 param_2,undefined4 param_3)

{
  undefined2 unaff_SS;
  undefined1 local_102 [256];
  
  FUN_24dd_47d9(0xff,local_102,unaff_SS,0,param_1,param_2);
  FUN_24dd_3eaf(0xff,(int)param_3,(int)((ulong)param_3 >> 0x10),local_102,unaff_SS);
  return;
}

