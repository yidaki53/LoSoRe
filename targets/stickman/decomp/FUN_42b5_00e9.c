
/* WARNING: Removing unreachable block (ram,0x00042c4c) */
/* WARNING: Removing unreachable block (ram,0x00042c4f) */
/* WARNING: Removing unreachable block (ram,0x00042c53) */
/* WARNING: Removing unreachable block (ram,0x00042c62) */
/* WARNING: Removing unreachable block (ram,0x00042c5c) */
/* WARNING: Removing unreachable block (ram,0x00042c64) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __cdecl16far FUN_42b5_00e9(void)

{
  code *pcVar1;
  undefined2 in_AX;
  int iVar2;
  char *pcVar3;
  undefined2 uVar4;
  
  uVar4 = 0x4473;
  DAT_4473_0392 = in_AX;
  DAT_4473_0394 = 0;
  DAT_4473_0396 = 0;
  pcVar3 = (char *)_DAT_4473_038e;
  if ((int)((ulong)_DAT_4473_038e >> 0x10) == 0 && pcVar3 == (char *)0x0) {
    FUN_42b5_05bf(0xeb16,0x4473);
    FUN_42b5_05bf(0xec16,0x4473);
    iVar2 = 0x13;
    do {
      pcVar1 = (code *)swi(0x21);
      (*pcVar1)();
      iVar2 = iVar2 + -1;
    } while (iVar2 != 0);
    if (*(int *)0x394 != 0 || *(int *)0x396 != 0) {
      FUN_42b5_01a5();
      FUN_42b5_01b3();
      FUN_42b5_01a5();
      FUN_42b5_01cd();
      FUN_42b5_01e7();
      FUN_42b5_01cd();
      pcVar3 = (char *)0x215;
      FUN_42b5_01a5();
    }
    pcVar1 = (code *)swi(0x21);
    (*pcVar1)();
    for (; *pcVar3 != '\0'; pcVar3 = pcVar3 + 1) {
      FUN_42b5_01e7();
    }
    return;
  }
  _DAT_4473_038e = (char *)0x0;
  DAT_4473_039c = 0;
  return;
}

