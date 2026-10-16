
void __stdcall16far FUN_24dd_02cb(undefined4 *param_1)

{
  undefined2 uVar1;
  undefined2 uVar2;
  undefined2 unaff_DS;
  
  uVar2 = (undefined2)((ulong)*param_1 >> 0x10);
  uVar1 = (undefined2)*param_1;
  *(undefined2 *)0x63ee = uVar1;
  *(undefined2 *)0x63f0 = uVar2;
  *(undefined2 *)0x63f6 = uVar1;
  *(undefined2 *)0x63f8 = uVar2;
  return;
}

