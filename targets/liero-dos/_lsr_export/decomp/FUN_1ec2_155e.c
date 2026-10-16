
void __stdcall16far FUN_1ec2_155e(undefined4 param_1)

{
  int iVar1;
  undefined2 uVar2;
  undefined1 local_3;
  
  local_3 = 0;
  while( true ) {
    uVar2 = (undefined2)((ulong)param_1 >> 0x10);
    iVar1 = (int)param_1;
    FUN_2971_65df(0x1ec2,CONCAT11((char)((uint)local_3 * 3 >> 8),
                                  *(undefined1 *)(iVar1 + (uint)local_3 * 3 + 2)),
                  CONCAT11((char)((uint)local_3 * 3 >> 8),
                           *(undefined1 *)(iVar1 + (uint)local_3 * 3 + 1)),
                  CONCAT11((char)((uint)local_3 * 3 >> 8),*(undefined1 *)(iVar1 + (uint)local_3 * 3)
                          ),local_3);
    if (local_3 == 0xff) break;
    local_3 = local_3 + 1;
  }
  return;
}

