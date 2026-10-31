
void __cdecl16near FUN_1000_35bb(void)

{
  bool bVar1;
  char cVar2;
  undefined2 uVar3;
  undefined2 uVar4;
  undefined2 local_6;
  
  FUN_42b5_04df();
  uVar4 = 0x3de3;
  FUN_3de3_0c99(0x35a2,0x42b5);
  local_6 = 1;
  bVar1 = false;
  while (!bVar1) {
    if (local_6 == 1) {
      FUN_3de3_0b67(7,0xf);
    }
    else if (local_6 == 2) {
      FUN_3de3_0b67(0xf,0xf);
    }
    else if (local_6 == 3) {
      FUN_3de3_0b67(7,0x32);
    }
    else if (local_6 == 4) {
      FUN_3de3_0b67(0xf,0x32);
    }
    FUN_3de3_0d8a();
    uVar3 = FUN_3de3_0339();
    uVar4 = 0x42b5;
    cVar2 = FUN_42b5_1bc4(uVar3);
    if (cVar2 == '\0') {
      uVar4 = 0x3de3;
      FUN_3de3_0339();
    }
    else if (cVar2 == '2') {
      if (local_6 < 4) {
        local_6 = local_6 + 1;
      }
      else {
        local_6 = 1;
      }
    }
    else if (cVar2 == '8') {
      if (local_6 < 2) {
        local_6 = 4;
      }
      else {
        local_6 = local_6 + -1;
      }
    }
    else if ((cVar2 == '4') || (cVar2 == '6')) {
      if (local_6 < 3) {
        local_6 = local_6 + 2;
      }
      else {
        local_6 = local_6 + -2;
      }
    }
    else if (cVar2 == '\r') {
      if (local_6 == 1) {
        FUN_1000_3493();
      }
      else if (local_6 == 2) {
        FUN_1000_34f9();
      }
      else if (local_6 == 3) {
        FUN_1000_355f();
      }
      else if (local_6 == 4) {
        bVar1 = true;
      }
    }
    else if (cVar2 == 'A') {
      FUN_1000_3493();
    }
    else if (cVar2 == 'M') {
      FUN_1000_34f9();
    }
    else if (cVar2 == 'S') {
      FUN_1000_355f();
    }
    else if (((cVar2 == 'E') || (cVar2 == 'Q')) || (cVar2 == '\x1b')) {
      bVar1 = true;
    }
  }
  FUN_3de3_002d(0x35aa,uVar4);
  FUN_3de3_0c99(0x35b3,0x3de3);
  return;
}

