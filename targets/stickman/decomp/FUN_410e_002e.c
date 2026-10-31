
/* WARNING: Removing unreachable block (ram,0x00041154) */

void __cdecl16near FUN_410e_002e(void)

{
  byte bVar1;
  byte extraout_AH;
  undefined2 unaff_DS;
  
  bVar1 = FUN_410e_0609();
  if ((bVar1 != 7) && (3 < bVar1)) {
    FUN_410e_0097();
  }
  FUN_410e_00e5();
  FUN_410e_0609();
  *(byte *)0xeb12 = extraout_AH & 0x7f;
  *(byte *)0xeb08 = extraout_AH & 0x7f;
  *(undefined1 *)0xeb03 = 0;
  *(undefined1 *)0xeb13 = 0;
  *(undefined1 *)0xeb14 = 0;
  *(undefined1 *)0xeb02 = 1;
  do {
  } while( true );
}

