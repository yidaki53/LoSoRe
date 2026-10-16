
void __stdcall16far FUN_1ec2_15bb(undefined4 param_1)

{
  int iVar1;
  undefined2 uVar2;
  undefined2 unaff_SS;
  byte local_3;
  
  local_3 = 0;
  while( true ) {
    uVar2 = (undefined2)((ulong)param_1 >> 0x10);
    iVar1 = (int)param_1;
    FUN_1ec2_152f(iVar1 + (uint)local_3 * 3 + 2,uVar2,iVar1 + (uint)local_3 * 3 + 1,uVar2,
                  iVar1 + (uint)local_3 * 3,uVar2,&local_3,unaff_SS);
    if (local_3 == 0xff) break;
    local_3 = local_3 + 1;
  }
  return;
}

