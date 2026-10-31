
void __cdecl16near FUN_1000_00e8(void)

{
  undefined2 unaff_DS;
  
  FUN_42b5_04df();
  if (*(char *)0x3b8 == '\0') {
    *(undefined1 *)0x136 = 1;
  }
  else {
    if (*(int *)0x3b6 == 1) {
      FUN_42b5_0d75(1,1,0x3b8,unaff_DS);
    }
    else {
      *(int *)0x3b6 = *(int *)0x3b6 + -1;
    }
    if (*(int *)0x3b6 == 1) {
      FUN_42b5_0d75(1,1,0x3b8,unaff_DS);
    }
    else {
      *(int *)0x3b6 = *(int *)0x3b6 + -1;
    }
    FUN_3de3_0b67(0x17,1);
    FUN_3de3_002d(0x8d,0x3de3);
    FUN_3de3_0b67(0x17,*(undefined2 *)0x3b6);
    FUN_3de3_002d(0x3b8,unaff_DS);
    FUN_3de3_002d(0xe3,0x3de3);
  }
  return;
}

