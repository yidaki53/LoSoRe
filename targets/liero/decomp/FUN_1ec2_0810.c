
void __stdcall16far FUN_1ec2_0810(byte param_1,undefined1 *param_2)

{
  undefined1 *puVar1;
  undefined1 *puVar2;
  int iVar3;
  undefined1 *puVar4;
  undefined1 *puVar5;
  undefined2 unaff_SS;
  undefined1 local_302 [768];
  
  puVar5 = local_302;
  puVar4 = (undefined1 *)param_2;
  for (iVar3 = 0x300; iVar3 != 0; iVar3 = iVar3 + -1) {
    puVar2 = puVar5;
    puVar5 = puVar5 + 1;
    puVar1 = puVar4;
    puVar4 = puVar4 + 1;
    *puVar2 = *puVar1;
  }
  FUN_1ec2_10cf(local_302[(uint)param_1 * 3 + 2],local_302[(uint)param_1 * 3 + 1],
                local_302[(uint)param_1 * 3],param_1);
  return;
}

