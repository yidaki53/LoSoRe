
void __cdecl16near FUN_1000_3a5e(void)

{
  bool bVar1;
  char cVar2;
  undefined2 uVar3;
  undefined2 uVar4;
  undefined2 unaff_DS;
  undefined2 local_6;
  
  FUN_42b5_04df();
  *(undefined1 *)0x136 = 0;
  uVar4 = 0x3de3;
  FUN_3de3_0c99(0x3a45,0x42b5);
  local_6 = 1;
  bVar1 = false;
  while (!bVar1) {
    FUN_3de3_0b67(local_6 + 0xd,0x1e);
    FUN_3de3_0d8a();
    uVar3 = FUN_3de3_0339();
    uVar4 = 0x42b5;
    cVar2 = FUN_42b5_1bc4(uVar3);
    if (cVar2 == '\0') {
      uVar4 = 0x3de3;
      FUN_3de3_0339();
    }
    else if (cVar2 == '2') {
      if (local_6 < 3) {
        local_6 = local_6 + 1;
      }
    }
    else if (cVar2 == '8') {
      if (1 < local_6) {
        local_6 = local_6 + -1;
      }
    }
    else if (cVar2 == '\r') {
      if (local_6 == 1) {
        FUN_1000_374b();
      }
      else if (local_6 == 2) {
        FUN_1000_390b();
      }
      else if (local_6 == 3) {
        bVar1 = true;
      }
    }
    else if (cVar2 == 'S') {
      FUN_1000_374b();
    }
    else if (cVar2 == 'Y') {
      FUN_1000_390b();
    }
    else if (((cVar2 == 'E') || (cVar2 == 'Q')) || (cVar2 == '\x1b')) {
      bVar1 = true;
    }
  }
  FUN_3de3_002d(0x3a4d,uVar4);
  FUN_3de3_0c99(0x3a56,0x3de3);
  *(undefined1 *)0x136 = 1;
  return;
}

