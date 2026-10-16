
void FUN_1000_0ebe(undefined2 param_1,undefined2 param_2,char param_3)

{
  char *pcVar1;
  undefined4 uVar2;
  char cVar3;
  byte bVar4;
  int iVar5;
  int iVar6;
  int iVar7;
  int iVar8;
  int iVar9;
  int iVar10;
  int iVar11;
  undefined2 uVar12;
  undefined2 unaff_DS;
  uint local_b;
  uint local_9;
  undefined1 local_3;
  
  local_3 = 0x10;
  FUN_24dd_0530();
  if (param_3 == '\0') {
    local_3 = 0x15;
  }
  else if (param_3 == '\x01') {
    local_3 = 0x16;
  }
  do {
    iVar5 = FUN_24dd_4654(0x1f2);
    iVar6 = FUN_24dd_4654(0x154);
    cVar3 = FUN_1000_0c7f(0xff60,0xff60,param_1,param_2,iVar6 + 5,iVar5 + 3);
  } while (cVar3 == '\0');
  iVar7 = iVar5 + -4;
  iVar8 = iVar6 + -2;
  uVar12 = (undefined2)((ulong)*(undefined4 *)0x6678 >> 0x10);
  iVar11 = (int)*(undefined4 *)0x6678 + (uint)*(byte *)0x136a * 0x100;
  iVar9 = FUN_24dd_4654(*(undefined1 *)0x137e);
  iVar10 = ((uint)*(byte *)0x1374 + iVar9) * 0x100;
  if (*(char *)0x1388 == '\x01') {
    iVar10 = iVar10 + 1;
  }
  FUN_202c_005a(iVar10,(int)*(undefined4 *)0x6678 + ((uint)*(byte *)0x1374 + iVar9) * 0x100,
                (int)((ulong)*(undefined4 *)0x6678 >> 0x10),iVar11,uVar12,iVar8,iVar7);
  if (*(char *)0x66af != '\0') {
    local_9 = iVar5 - 7;
    if ((int)local_9 <= (int)(iVar5 + 0xdU)) {
      do {
        if ((local_9 < 0x8000) && ((int)local_9 < 0x1f8)) {
          local_b = iVar6 - 5;
          if ((int)local_b <= (int)(iVar6 + 0xfU)) {
            do {
              if ((local_b < 0x8000) && ((int)local_b < 0x15e)) {
                iVar7 = 0x20;
                bVar4 = FUN_24dd_4161();
                if ((*(byte *)(iVar7 + 0x14e0) & bVar4) != 0) {
                  iVar7 = 0x20;
                  bVar4 = FUN_24dd_4161();
                  if ((*(byte *)(iVar7 + 0x6604) & bVar4) != 0) {
                    uVar2 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_b * 4);
                    pcVar1 = (char *)((int)uVar2 + local_9);
                    *pcVar1 = *pcVar1 + '\x04';
                    goto LAB_1000_10af;
                  }
                }
                uVar2 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_b * 4);
                bVar4 = *(byte *)((int)uVar2 + local_9);
                if ((0xa3 < bVar4) && (bVar4 < 0xa8)) {
                  iVar7 = 0x20;
                  bVar4 = FUN_24dd_4161();
                  if ((*(byte *)(iVar7 + 0x6604) & bVar4) != 0) {
                    uVar2 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_b * 4);
                    pcVar1 = (char *)((int)uVar2 + local_9);
                    *pcVar1 = *pcVar1 + -4;
                  }
                }
              }
LAB_1000_10af:
              if (local_b == iVar6 + 0xfU) break;
              local_b = local_b + 1;
            } while( true );
          }
        }
        if (local_9 == iVar5 + 0xdU) break;
        local_9 = local_9 + 1;
      } while( true );
    }
  }
  FUN_202c_14b6(0,0,0,0,iVar6 + 5,iVar5 + 3,0,local_3);
  return;
}

