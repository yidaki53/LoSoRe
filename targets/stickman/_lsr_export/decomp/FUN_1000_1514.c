
void __cdecl16near FUN_1000_1514(void)

{
  int iVar1;
  char cVar2;
  undefined2 unaff_DS;
  undefined2 local_8;
  undefined2 local_4;
  
  FUN_42b5_04df();
  local_4 = 1;
  while( true ) {
    iVar1 = local_4 * 0x27;
    _local_8 = (int *)CONCAT22(unaff_DS,(int *)(iVar1 + 0x25d9));
    if (*(int *)(iVar1 + 0x25dd) != 0) {
      FUN_3de3_0b67(*(int *)(iVar1 + 0x25db) + 1,*_local_8);
      FUN_3de3_002d(0x150d,0x3de3);
      *_local_8 = *_local_8 + *(int *)(iVar1 + 0x25dd);
      if ((*_local_8 < 1) || (0x50 < *_local_8)) {
        *(undefined2 *)(iVar1 + 0x25dd) = 0;
      }
      else {
        cVar2 = FUN_1000_0c8f(*(undefined2 *)(iVar1 + 0x25db),*_local_8);
        if (cVar2 == '\0') {
          if (*(int *)(iVar1 + 0x25dd) != 1) {
            FUN_3de3_0b67(*(int *)(iVar1 + 0x25db) + 1,*_local_8);
          }
          FUN_3de3_002d(local_4 * 0x27 + 0x25df,unaff_DS);
          FUN_3de3_002d(0x150f,0x3de3);
        }
        else {
          FUN_1000_139e(*(undefined2 *)(iVar1 + 0x25db),*_local_8);
          *(undefined2 *)(iVar1 + 0x25dd) = 0;
        }
      }
    }
    if (local_4 == 5) break;
    local_4 = local_4 + 1;
  }
  FUN_410e_029c(0x32);
  return;
}

