
char __cdecl16far FUN_3de3_0339(void)

{
  char cVar1;
  char cVar2;
  undefined2 in_DX;
  undefined2 extraout_DX;
  undefined2 unaff_DS;
  undefined2 uVar3;
  
  uVar3 = 0x3de3;
  FUN_42b5_04df();
  cVar1 = FUN_405f_0420(uVar3);
  if (cVar1 == '\0') {
    cVar1 = (char)((uint)uVar3 >> 8);
    cVar2 = FUN_405f_0420();
    if (cVar2 == '#') {
      FUN_405f_03f0();
      FUN_405f_03c9();
      *(undefined2 *)0xaaec = 0;
      FUN_3de3_0278(0x325,0x405f);
      in_DX = extraout_DX;
    }
    else if (cVar2 == 'P') {
      cVar1 = '2';
    }
    else if (cVar2 == 'K') {
      cVar1 = '4';
    }
    else if (cVar2 == 'M') {
      cVar1 = '6';
    }
    else if (cVar2 == 'H') {
      cVar1 = '8';
    }
    else if (cVar2 == 'O') {
      cVar1 = '1';
    }
    else if (cVar2 == 'Q') {
      cVar1 = '3';
    }
    else if (cVar2 == 'G') {
      cVar1 = '7';
    }
    else if (cVar2 == 'I') {
      cVar1 = '9';
    }
    else {
      cVar1 = '~';
    }
  }
  uVar3 = FUN_4170_0096();
  *(undefined2 *)0xa7d2 = uVar3;
  *(undefined2 *)0xa7d4 = in_DX;
  return cVar1;
}

