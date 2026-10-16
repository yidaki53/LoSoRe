
void __stdcall16far FUN_24dd_4181(uint *param_1,uint *param_2)

{
  uint *puVar1;
  uint *puVar2;
  uint *puVar3;
  int iVar4;
  uint *puVar5;
  uint *puVar6;
  undefined2 uVar7;
  
  uVar7 = (undefined2)((ulong)param_2 >> 0x10);
  puVar6 = (uint *)param_2;
  puVar5 = (uint *)param_1;
  iVar4 = 0x10;
  do {
    puVar2 = puVar5;
    puVar5 = puVar5 + 1;
    puVar1 = puVar6;
    puVar3 = puVar6;
    puVar6 = puVar6 + 1;
    *puVar3 = *puVar2 | *puVar1;
    iVar4 = iVar4 + -1;
  } while (iVar4 != 0);
  return;
}

