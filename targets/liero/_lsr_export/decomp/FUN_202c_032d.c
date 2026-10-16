
void __stdcall16far FUN_202c_032d(char param_1,undefined4 param_2,int param_3,int param_4)

{
  undefined4 uVar1;
  byte bVar2;
  uint uVar3;
  uint uVar4;
  int iVar5;
  int iVar6;
  int iVar7;
  undefined2 uVar8;
  undefined2 unaff_DS;
  int local_a;
  int local_8;
  
  iVar7 = (int)param_2;
  uVar8 = (undefined2)((ulong)param_2 >> 0x10);
  if (param_1 == '\0') {
    for (local_a = 0; iVar5 = local_a + param_3, iVar5 < 0x15e; local_a = local_a + 1) {
      if (-1 < iVar5) {
        local_8 = 0;
        while( true ) {
          iVar6 = local_8 + param_4;
          if (((-1 < iVar6) && (iVar6 < 0x1f8)) &&
             (*(char *)(iVar7 + local_a * 0x10 + local_8) != '\0')) {
            uVar1 = *(undefined4 *)((int)*(undefined4 *)0x6674 + iVar5 * 4);
            *(undefined1 *)((int)uVar1 + iVar6) = *(undefined1 *)(iVar7 + local_a * 0x10 + local_8);
          }
          if (local_8 == 0xf) break;
          local_8 = local_8 + 1;
        }
      }
      if (local_a == 0xf) {
        return;
      }
    }
  }
  else {
    for (local_a = 0; uVar3 = local_a + param_3, (int)uVar3 < 0x15e; local_a = local_a + 1) {
      if (uVar3 < 0x8000) {
        local_8 = 0;
        while( true ) {
          uVar4 = local_8 + param_4;
          if (((uVar4 < 0x8000) && ((int)uVar4 < 0x1f8)) &&
             (*(char *)(iVar7 + local_a * 0x10 + local_8) != '\0')) {
            iVar5 = 0x20;
            bVar2 = FUN_24dd_4161();
            if ((*(byte *)(iVar5 + 0x6644) & bVar2) == 0) {
              uVar1 = *(undefined4 *)((int)*(undefined4 *)0x6674 + uVar3 * 4);
              *(char *)((int)uVar1 + uVar4) = *(char *)(iVar7 + local_a * 0x10 + local_8) + '\x03';
            }
            else {
              uVar1 = *(undefined4 *)((int)*(undefined4 *)0x6674 + uVar3 * 4);
              *(undefined1 *)((int)uVar1 + uVar4) =
                   *(undefined1 *)(iVar7 + local_a * 0x10 + local_8);
            }
          }
          if (local_8 == 0xf) break;
          local_8 = local_8 + 1;
        }
      }
      if (local_a == 0xf) {
        return;
      }
    }
  }
  return;
}

