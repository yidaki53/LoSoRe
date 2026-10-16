
void __cdecl16near FUN_24dd_35b3(void)

{
  code *pcVar1;
  undefined2 uVar2;
  int in_CX;
  int unaff_BP;
  char *unaff_DI;
  undefined2 unaff_ES;
  undefined2 unaff_SS;
  
  for (; (in_CX != 0 && (0xf5 < (byte)(*unaff_DI - 0x3aU))); unaff_DI = unaff_DI + 1) {
    pcVar1 = (code *)swi(0x3c);
    (*pcVar1)();
    uVar2 = func_0x000a4d2e();
    *(undefined2 *)(unaff_BP + -4) = uVar2;
    pcVar1 = (code *)swi(0x3a);
    (*pcVar1)();
    in_CX = in_CX + -1;
  }
  return;
}

