
void __cdecl16near FUN_42b5_1bb5(undefined2 param_1)

{
  code *pcVar1;
  undefined2 uVar2;
  undefined1 in_CF;
  
  pcVar1 = (code *)swi(0x21);
  uVar2 = (*pcVar1)();
  if ((bool)in_CF) {
    *(undefined2 *)0x39c = uVar2;
  }
  return;
}

