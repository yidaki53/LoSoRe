
void __cdecl16far FUN_24dd_0530(void)

{
  uint in_AX;
  undefined2 unaff_DS;
  
  if (((in_AX < 0xfe00) && ((undefined1 *)(in_AX + 0x200) < &stack0x0000)) &&
     (*(uint *)0x640e <= (uint)-((int)(in_AX + 0x200) - (int)&stack0x0000))) {
    return;
  }
  FUN_24dd_010f();
  return;
}

