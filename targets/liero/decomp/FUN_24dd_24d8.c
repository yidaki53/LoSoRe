
void __cdecl16near FUN_24dd_24d8(void)

{
  byte *pbVar1;
  uint uVar2;
  bool bVar3;
  char cVar4;
  char cVar5;
  byte bVar6;
  int iVar7;
  uint *unaff_SI;
  byte *unaff_DI;
  undefined2 unaff_ES;
  undefined2 unaff_DS;
  
  uVar2 = unaff_SI[4];
  if ((int)uVar2 < 0) {
    bVar6 = 0;
  }
  else {
    if (((int)uVar2 < 0x3c) ||
       ((uVar2 - 0x3c == 0 || (int)uVar2 < 0x3c &&
        ((unaff_SI[3] < 0xde0b ||
         ((unaff_SI[3] < 0xde0c &&
          ((unaff_SI[2] < 0x6b3a ||
           ((unaff_SI[2] < 0x6b3b &&
            ((unaff_SI[1] < 0x763f || ((unaff_SI[1] < 0x7640 && (*unaff_SI < 0xfff1))))))))))))))))
    {
      cVar4 = (char)(uVar2 - 0x3c) + -4;
      do {
        cVar5 = cVar4;
        cVar4 = cVar5 + '\x10';
      } while (cVar4 == '\0' || cVar5 < -0x10);
      if (cVar4 < '\x10') {
        do {
          bVar3 = cVar5 < -1;
          cVar5 = cVar5 + '\x01';
        } while (bVar3);
      }
      FUN_24dd_24ba();
      FUN_24dd_24ba();
      FUN_24dd_24ba();
      bVar6 = FUN_24dd_24ba();
      pbVar1 = unaff_DI;
      unaff_DI = unaff_DI + 1;
      *pbVar1 = bVar6 % 10 | bVar6 / 10 << 4;
      goto LAB_24dd_2585;
    }
    FUN_24dd_2361();
    bVar6 = 0x99;
  }
  for (iVar7 = 9; iVar7 != 0; iVar7 = iVar7 + -1) {
    pbVar1 = unaff_DI;
    unaff_DI = unaff_DI + 1;
    *pbVar1 = bVar6;
  }
LAB_24dd_2585:
  *unaff_DI = (byte)unaff_SI[5] >> 1 | (byte)unaff_SI[5] << 7;
  return;
}

