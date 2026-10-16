
void __stdcall16far
FUN_202c_005a(char param_1,undefined4 param_2,undefined4 param_3,int param_4,int param_5)

{
  char cVar1;
  undefined4 uVar2;
  byte bVar3;
  uint uVar4;
  uint uVar5;
  int iVar6;
  undefined2 uVar7;
  undefined2 unaff_DS;
  int local_a;
  int local_8;
  undefined2 uVar8;
  
  uVar7 = (undefined2)((ulong)param_3 >> 0x10);
  uVar8 = (undefined2)((ulong)param_2 >> 0x10);
  if (param_1 == '\0') {
    for (local_a = 0; uVar4 = local_a + param_4, (int)uVar4 < 0x15d; local_a = local_a + 1) {
      if (uVar4 < 0x8000) {
        local_8 = 0;
        while( true ) {
          uVar5 = local_8 + param_5;
          if ((uVar5 < 0x8000) && ((int)uVar5 < 0x1f8)) {
            cVar1 = *(char *)((int)param_3 + local_a * 0x10 + local_8);
            if ((cVar1 == '\n') || (cVar1 == '\x06')) {
              iVar6 = 0x20;
              bVar3 = FUN_24dd_4161();
              if ((*(byte *)(iVar6 + 0x14c0) & bVar3) != 0) {
                uVar2 = *(undefined4 *)((int)*(undefined4 *)0x6674 + uVar4 * 4);
                *(undefined1 *)((int)uVar2 + uVar5) =
                     *(undefined1 *)((int)param_2 + (uVar4 & 0xf) * 0x10 + (uVar5 & 0xf));
              }
            }
            else if (cVar1 == '\x02') {
              iVar6 = 0x20;
              bVar3 = FUN_24dd_4161();
              if ((*(byte *)(iVar6 + 0x14c0) & bVar3) != 0) {
                uVar2 = *(undefined4 *)((int)*(undefined4 *)0x6674 + uVar4 * 4);
                *(undefined1 *)((int)uVar2 + uVar5) = 2;
              }
            }
            else if (cVar1 == '\x01') {
              iVar6 = 0x20;
              bVar3 = FUN_24dd_4161();
              if ((*(byte *)(iVar6 + 0x14c0) & bVar3) != 0) {
                uVar2 = *(undefined4 *)((int)*(undefined4 *)0x6674 + uVar4 * 4);
                *(undefined1 *)((int)uVar2 + uVar5) = 1;
              }
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
  else {
    for (local_a = 0; uVar4 = local_a + param_4, (int)uVar4 < 0x15d; local_a = local_a + 1) {
      if (uVar4 < 0x8000) {
        local_8 = 0;
        while( true ) {
          uVar5 = local_8 + param_5;
          if ((uVar5 < 0x8000) && ((int)uVar5 < 0x1f8)) {
            cVar1 = *(char *)((int)param_3 + local_a * 0x10 + local_8);
            if (cVar1 == '\x06') {
              iVar6 = 0x20;
              bVar3 = FUN_24dd_4161();
              if ((*(byte *)(iVar6 + 0x6624) & bVar3) != 0) {
                uVar2 = *(undefined4 *)((int)*(undefined4 *)0x6674 + uVar4 * 4);
                *(undefined1 *)((int)uVar2 + uVar5) =
                     *(undefined1 *)((int)param_2 + (uVar4 & 0xf) * 0x10 + (uVar5 & 0xf));
              }
            }
            else if (cVar1 == '\x01') {
              iVar6 = 0x20;
              bVar3 = FUN_24dd_4161();
              if ((*(byte *)(iVar6 + 0x1460) & bVar3) != 0) {
                uVar2 = *(undefined4 *)((int)*(undefined4 *)0x6674 + uVar4 * 4);
                *(undefined1 *)((int)uVar2 + uVar5) = 1;
              }
              iVar6 = 0x20;
              bVar3 = FUN_24dd_4161();
              if ((*(byte *)(iVar6 + 0x1480) & bVar3) != 0) {
                uVar2 = *(undefined4 *)((int)*(undefined4 *)0x6674 + uVar4 * 4);
                *(undefined1 *)((int)uVar2 + uVar5) = 2;
              }
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

