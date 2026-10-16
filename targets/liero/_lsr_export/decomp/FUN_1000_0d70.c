
undefined1 FUN_1000_0d70(int param_1,int param_2,byte param_3,byte param_4)

{
  byte bVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  undefined2 unaff_DS;
  int local_b;
  int local_9;
  
  FUN_24dd_0530();
  if (*(char *)((int)*(undefined4 *)0x6670 + (uint)param_4 * 0xaa + 0x9a) != '\0') {
    iVar2 = (param_2 - *(int *)((int)*(undefined4 *)0x6670 + (uint)param_4 * 0xaa + 6)) + 7;
    iVar3 = (param_1 - *(int *)((int)*(undefined4 *)0x6670 + (uint)param_4 * 0xaa + 10)) + 5;
    if (*(char *)((int)*(undefined4 *)0x6670 + (uint)param_4 * 0xaa + 0x9b) == '\0') {
      iVar2 = 0xe - iVar2;
    }
    local_9 = iVar2 - (uint)param_3;
    if (local_9 <= (int)((uint)param_3 + iVar2)) {
      while( true ) {
        iVar4 = (uint)param_3 + iVar3;
        local_b = iVar3 - (uint)param_3;
        if (local_b <= iVar4) {
          while( true ) {
            if ((((0 < local_9) && (local_9 < 0xe)) && (-1 < local_b)) && (local_b < 10)) {
              iVar5 = 0x20;
              bVar1 = FUN_24dd_4161();
              if ((*(byte *)(iVar5 + 0x28) & bVar1) != 0) {
                return 1;
              }
            }
            if (local_b == iVar4) break;
            local_b = local_b + 1;
          }
        }
        if (local_9 == (uint)param_3 + iVar2) break;
        local_9 = local_9 + 1;
      }
    }
  }
  return 0;
}

