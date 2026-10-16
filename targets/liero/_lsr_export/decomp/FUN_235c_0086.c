
/* WARNING: Control flow encountered bad instruction data */

uint __stdcall16far FUN_235c_0086(void)

{
  code *pcVar1;
  uint uVar2;
  undefined2 uVar3;
  undefined2 uVar4;
  undefined2 in_BX;
  int unaff_SI;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  undefined1 uVar5;
  int in_stack_0000000a;
  
  *(int *)0x67d0 = in_stack_0000000a + 6;
  *(int *)0x67d2 = in_stack_0000000a + 10;
  *(int *)0x67d4 = in_stack_0000000a + 0xc;
  *(int *)0x67d6 = in_stack_0000000a + 0xe;
  uVar2 = FUN_235c_0036();
  if ((char)uVar2 == '\0') {
    return uVar2 & 0xff00;
  }
  FUN_235c_0000();
  FUN_235c_001a();
  uVar4 = 0;
  uVar3 = FUN_24dd_462e();
  *(undefined2 *)0x67c6 = uVar3;
  *(undefined2 *)0x67c8 = in_BX;
  *(undefined2 *)0x67ca = uVar4;
  FUN_24dd_31d8();
  FUN_235c_001a();
  uVar5 = 0;
  pcVar1 = (code *)swi(0x37);
  (*pcVar1)();
  pcVar1 = (code *)swi(0x3c);
  (*pcVar1)();
  pcVar1 = (code *)swi(0x3a);
  (*pcVar1)();
  uVar2 = *(uint *)(&stack0x3201 + unaff_SI);
  *(uint *)(&stack0x3201 + unaff_SI) = (uint)(CONCAT12(uVar5,uVar2) >> 0xc) | uVar2 << 5;
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}

