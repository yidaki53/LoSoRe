
void __cdecl16near FUN_1000_4d03(void)

{
  bool bVar1;
  char cVar2;
  undefined2 uVar3;
  undefined2 unaff_DS;
  undefined2 uVar4;
  int iVar5;
  
  uVar3 = 0x42b5;
  uVar4 = 0x4d0e;
  FUN_42b5_04df();
  FUN_1000_4a8d(uVar4);
  iVar5 = 1;
  bVar1 = false;
  while (!bVar1) {
    FUN_3de3_0b67(iVar5 + 0xf,0x2b);
    FUN_3de3_0d8a();
    uVar4 = FUN_3de3_0339();
    uVar3 = 0x42b5;
    cVar2 = FUN_42b5_1bc4(uVar4);
    if (cVar2 == '\0') {
      uVar3 = 0x3de3;
      FUN_3de3_0339();
    }
    else if (cVar2 == '2') {
      if (iVar5 < 5) {
        iVar5 = iVar5 + 1;
      }
    }
    else if (cVar2 == '8') {
      if (1 < iVar5) {
        iVar5 = iVar5 + -1;
      }
    }
    else if (cVar2 == '\r') {
      if (iVar5 == 1) {
        FUN_1000_4b69();
      }
      else if (iVar5 == 2) {
        FUN_1000_4bf5();
      }
      else if (iVar5 == 3) {
        FUN_1000_4c81();
      }
      else if (iVar5 == 4) {
        FUN_42b5_0af8(0x8a,0x4b8,unaff_DS,0x542,unaff_DS);
        FUN_1000_01cf();
        bVar1 = true;
      }
      else if (iVar5 == 5) {
        bVar1 = true;
      }
      uVar3 = 0x42b5;
    }
    else if (cVar2 == 'S') {
      FUN_1000_4b69();
    }
    else if (cVar2 == 'M') {
      FUN_1000_4bf5();
    }
    else if (cVar2 == 'T') {
      FUN_1000_4c81();
    }
    else if (cVar2 == 'A') {
      uVar3 = 0x42b5;
      FUN_42b5_0af8(0x8a,0x4b8,unaff_DS,0x542,unaff_DS);
      FUN_1000_01cf();
      bVar1 = true;
    }
    else if (cVar2 == 'E') {
      bVar1 = true;
    }
  }
  FUN_3de3_002d(0x4cf2,uVar3);
  FUN_3de3_0c99(0x4cfb,0x3de3);
  *(undefined1 *)0x136 = 1;
  return;
}

