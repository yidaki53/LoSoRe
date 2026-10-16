
void __stdcall16far FUN_24cb_0000(void)

{
  byte *pbVar1;
  code *pcVar2;
  byte bVar3;
  byte *pbVar5;
  byte *pbVar6;
  undefined2 unaff_SS;
  byte *in_stack_0000000a;
  int iVar4;
  
  pbVar5 = (byte *)in_stack_0000000a;
  pbVar6 = &stack0xffae;
  bVar3 = *in_stack_0000000a;
  if (0x4e < bVar3) {
    bVar3 = 0x4f;
  }
  for (iVar4 = (int)(char)bVar3; pbVar5 = pbVar5 + 1, iVar4 != 0; iVar4 = iVar4 + -1) {
    pbVar1 = pbVar6;
    pbVar6 = pbVar6 + 1;
    *pbVar1 = *pbVar5;
  }
  *pbVar6 = 0;
  pcVar2 = (code *)swi(0x21);
  (*pcVar2)();
  pcVar2 = (code *)swi(0x21);
  (*pcVar2)();
  FUN_24cb_0058();
  return;
}

