
/* WARNING: Instruction at (ram,0x00028886) overlaps instruction at (ram,0x00028885)
    */
/* WARNING: Removing unreachable block (ram,0x0002886f) */
/* WARNING: Removing unreachable block (ram,0x00028876) */

uint __cdecl16far FUN_24dd_3a7f(void)

{
  code *pcVar1;
  undefined1 uVar2;
  uint uVar3;
  undefined2 extraout_DX;
  undefined2 unaff_DS;
  
  FUN_24dd_37ec();
  pcVar1 = (code *)swi(0x35);
  uVar2 = (*pcVar1)();
  out(extraout_DX,uVar2);
  pcVar1 = (code *)swi(0x3d);
  (*pcVar1)();
  *(undefined2 *)0x6410 = 0x6a;
  pcVar1 = (code *)swi(0x39);
  uVar3 = (*pcVar1)();
  return uVar3 ^ 0xcdee;
}

