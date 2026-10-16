
void __cdecl16far FUN_24dd_31d8(void)

{
  code *pcVar1;
  undefined1 uVar2;
  uint in_AX;
  int iVar3;
  undefined2 in_DX;
  undefined2 extraout_DX;
  
  if ((char)in_AX != '\0') {
    iVar3 = (CONCAT11((char)((uint)in_DX >> 8),(char)in_AX) & 0x80ff) + 0x3f7e;
    pcVar1 = (code *)swi(0x3c);
    (*pcVar1)(in_AX & 0xff00);
    pcVar1 = (code *)swi(0x3d);
    (*pcVar1)(iVar3);
    return;
  }
  pcVar1 = (code *)swi(0x35);
  uVar2 = (*pcVar1)();
  out(extraout_DX,uVar2);
  return;
}

