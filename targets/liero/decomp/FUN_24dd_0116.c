
/* WARNING: Removing unreachable block (ram,0x00024ef9) */
/* WARNING: Removing unreachable block (ram,0x00024efc) */
/* WARNING: Removing unreachable block (ram,0x00024f00) */
/* WARNING: Removing unreachable block (ram,0x00024f0a) */
/* WARNING: Removing unreachable block (ram,0x00024f0e) */
/* WARNING: Removing unreachable block (ram,0x00024f15) */
/* WARNING: Removing unreachable block (ram,0x00024f1e) */
/* WARNING: Removing unreachable block (ram,0x00024f2b) */
/* WARNING: Removing unreachable block (ram,0x00024f25) */
/* WARNING: Removing unreachable block (ram,0x00024f2f) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __cdecl16far FUN_24dd_0116(void)

{
  code *pcVar1;
  undefined2 in_AX;
  int iVar2;
  char *pcVar3;
  undefined2 uVar4;
  
  uVar4 = 0x2971;
  DAT_2971_6406 = in_AX;
  DAT_2971_6408 = 0;
  DAT_2971_640a = 0;
  pcVar3 = (char *)_DAT_2971_6402;
  if ((int)((ulong)_DAT_2971_6402 >> 0x10) == 0 && pcVar3 == (char *)0x0) {
    DAT_2971_6408 = 0;
    FUN_24dd_3711(0x78f0,0x2971);
    FUN_24dd_3711(0x79f0,0x2971);
    iVar2 = 0x13;
    do {
      pcVar1 = (code *)swi(0x21);
      (*pcVar1)();
      iVar2 = iVar2 + -1;
    } while (iVar2 != 0);
    if (*(int *)0x6408 != 0 || *(int *)0x640a != 0) {
      FUN_24dd_01f0();
      FUN_24dd_01fe();
      FUN_24dd_01f0();
      FUN_24dd_0218();
      FUN_24dd_0232();
      FUN_24dd_0218();
      pcVar3 = (char *)0x260;
      FUN_24dd_01f0();
    }
    pcVar1 = (code *)swi(0x21);
    (*pcVar1)();
    for (; *pcVar3 != '\0'; pcVar3 = pcVar3 + 1) {
      FUN_24dd_0232();
    }
    return;
  }
  _DAT_2971_6402 = (char *)0x0;
  DAT_2971_6410 = 0;
  return;
}

