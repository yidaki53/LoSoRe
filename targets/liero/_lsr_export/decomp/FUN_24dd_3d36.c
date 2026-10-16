
void __cdecl16near FUN_24dd_3d36(void)

{
  undefined2 uVar1;
  byte *pbVar2;
  byte *pbVar3;
  uint uVar4;
  int in_DX;
  undefined2 unaff_DS;
  
  uVar1 = *(undefined2 *)0x640c;
  uVar4 = (uint)*(byte *)0x80;
  pbVar2 = (byte *)0x81;
  do {
    for (; (pbVar3 = pbVar2, uVar4 != 0 && (*pbVar2 < 0x21)); pbVar2 = pbVar2 + 1) {
      uVar4 = uVar4 - 1;
    }
    for (; (uVar4 != 0 && (0x20 < *pbVar3)); pbVar3 = pbVar3 + 1) {
      uVar4 = uVar4 - 1;
    }
  } while ((pbVar3 != pbVar2) && (in_DX = in_DX + -1, pbVar2 = pbVar3, in_DX != 0));
  return;
}

