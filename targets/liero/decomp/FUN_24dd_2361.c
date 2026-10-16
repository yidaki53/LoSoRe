
/* WARNING: Unable to track spacebase fully for stack */

undefined2 __cdecl16near FUN_24dd_2361(void)

{
  code *pcVar1;
  byte bVar2;
  undefined2 in_AX;
  undefined2 uVar3;
  byte bVar4;
  undefined2 in_CX;
  uint uVar5;
  undefined2 in_BX;
  undefined2 unaff_ES;
  undefined2 unaff_SS;
  
  uVar5 = CONCAT11((char)((uint)in_CX >> 8),*(undefined1 *)0xd6) & 0xff3f;
  bVar4 = (byte)uVar5 ^ 0x3f;
  bVar2 = *(byte *)0xd4 | (byte)(uVar5 >> 8);
  if (((bVar2 & bVar4 ^ bVar2) & 8) != 0) {
    bVar2 = bVar2 | 0x20;
  }
  if ((bVar4 & bVar2) != 0) {
    *(byte *)0xd4 = bVar2 | 0x80;
    if ((bVar2 & bVar4) == 0x20) {
      return in_AX;
    }
    pcVar1 = (code *)swi(0x21);
    (*pcVar1)();
    *(undefined2 *)0xd0 = in_BX;
    *(undefined2 *)0xd2 = unaff_ES;
                    /* WARNING: Could not recover jumptable at 0x0002718b. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    uVar3 = (*(code *)(ulong)*(uint *)0xd0)();
    return uVar3;
  }
  *(byte *)0xd4 = bVar2 & 0x7f;
  return in_AX;
}

