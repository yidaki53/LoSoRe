
void __cdecl16near FUN_235c_03a1(void)

{
  undefined2 uVar1;
  undefined2 unaff_DS;
  
  out(*(undefined2 *)0x67de,*(undefined1 *)0x67ee);
  out(*(undefined2 *)0x67e0,0);
  out(*(undefined2 *)0x67e2,*(undefined1 *)0x67ef);
  out(*(undefined2 *)0x67e4,*(undefined1 *)0x6e76);
  out(*(undefined2 *)0x67e4,*(undefined1 *)0x6e77);
  out(*(undefined2 *)0x67e6,(char)*(undefined2 *)0x67f0 + -1);
  out(*(undefined2 *)0x67e6,(char)((uint)(*(int *)0x67f0 + -1) >> 8));
  out(*(undefined2 *)0x67e8,*(undefined1 *)0x6e74);
  out(*(undefined2 *)0x67de,*(undefined1 *)0x67ed);
  if (*(char *)0x67cd == '\0') {
    FUN_235c_0000(0xffd1);
    FUN_235c_0000(0x40);
    uVar1 = FUN_235c_0372(0x5609);
    FUN_235c_0000(uVar1);
    if (*(char *)0x67cc == '\0') {
      FUN_235c_0000(0x14);
      FUN_235c_0000(0xffff);
      FUN_235c_0000(1);
    }
    else {
      FUN_235c_0000(0x48);
      FUN_235c_0000(0xffff);
      FUN_235c_0000(1);
      FUN_235c_0000(0x1c);
    }
  }
  else {
    FUN_235c_0000(0x41);
    FUN_235c_0000(0x56);
    FUN_235c_0000(9);
    FUN_235c_0000(0xffb6);
    FUN_235c_0000(0x10);
    FUN_235c_0000(0xffff);
    FUN_235c_0000(1);
  }
  return;
}

