
int __cdecl16far FUN_24dd_3e7c(void)

{
  int in_AX;
  uint in_CX;
  uint uVar1;
  undefined2 unaff_DS;
  
  if (*(byte *)0x6420 < 2) {
    for (uVar1 = in_CX & 0x1f; uVar1 != 0; uVar1 = uVar1 - 1) {
      in_AX = in_AX << 1;
    }
    return in_AX;
  }
  return in_AX << ((byte)in_CX & 0x1f);
}

