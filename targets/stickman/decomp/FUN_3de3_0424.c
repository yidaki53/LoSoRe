
undefined4 FUN_3de3_0424(undefined4 param_1)

{
  uint uVar1;
  uint uVar2;
  int iVar3;
  undefined2 unaff_SS;
  undefined1 local_12 [6];
  undefined2 local_c;
  int local_a;
  uint local_8;
  undefined2 local_6;
  undefined2 local_4;
  
  local_4 = 0x3de3;
  local_6 = 0xe25f;
  FUN_42b5_04df();
  FUN_42b5_0af8(0xc,local_12,unaff_SS,(int)param_1,(int)((ulong)param_1 >> 0x10));
  iVar3 = 0;
  uVar1 = FUN_42b5_0b14(local_c);
  uVar2 = local_a * 0x3c + uVar1;
  return CONCAT22(iVar3 + (uint)CARRY2(local_a * 0x3c,uVar1) + (uint)CARRY2(uVar2,local_8),
                  uVar2 + local_8);
}

