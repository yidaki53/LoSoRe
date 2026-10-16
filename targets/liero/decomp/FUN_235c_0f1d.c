
void __cdecl16far FUN_235c_0f1d(void)

{
  undefined2 unaff_DS;
  
  FUN_235c_045d();
  if (*(int *)0x6e58 != 0 || *(int *)0x6e5a != 0) {
    if (*(char *)0x67cd == '\0') {
      FUN_24dd_029f(0x800,*(undefined2 *)0x6e58,*(undefined2 *)0x6e5a);
    }
    else {
      FUN_24dd_029f(0x1000,*(undefined2 *)0x6e58,*(undefined2 *)0x6e5a);
    }
  }
  return;
}

