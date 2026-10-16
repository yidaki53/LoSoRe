
void __stdcall16far FUN_24cb_007c(undefined2 *param_1)

{
  code *pcVar1;
  undefined2 in_BX;
  undefined2 unaff_ES;
  
  pcVar1 = (code *)swi(0x21);
  (*pcVar1)();
  *param_1 = in_BX;
  ((undefined2 *)param_1)[1] = unaff_ES;
  return;
}

