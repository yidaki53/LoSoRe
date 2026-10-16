
void __stdcall16far
FUN_1ea2_01a8(undefined2 *param_1,int param_2,uint param_3,int param_4,undefined2 *param_5)

{
  undefined2 *puVar1;
  undefined2 *puVar2;
  undefined2 *puVar3;
  undefined2 *puVar4;
  uint uVar5;
  uint uVar6;
  undefined2 *puVar7;
  undefined2 *puVar8;
  undefined2 uVar9;
  undefined2 uVar10;
  
  uVar10 = (undefined2)((ulong)param_5 >> 0x10);
  puVar7 = (undefined2 *)param_5;
  uVar9 = (undefined2)((ulong)param_1 >> 0x10);
  puVar8 = (undefined2 *)param_1;
  uVar5 = param_3 >> 1;
  uVar6 = uVar5;
  if ((param_3 & 1) == 0) {
    do {
      for (; uVar6 != 0; uVar6 = uVar6 - 1) {
        puVar4 = puVar8;
        puVar8 = puVar8 + 1;
        puVar2 = puVar7;
        puVar7 = puVar7 + 1;
        *puVar4 = *puVar2;
      }
      puVar8 = (undefined2 *)((int)puVar8 + (0x140 - param_3));
      puVar7 = (undefined2 *)((int)puVar7 + (param_4 - param_3));
      param_2 = param_2 + -1;
      uVar6 = uVar5;
    } while (param_2 != 0);
  }
  else {
    do {
      puVar3 = (undefined2 *)((int)puVar8 + 1);
      puVar1 = (undefined2 *)((int)puVar7 + 1);
      *(undefined1 *)puVar8 = *(undefined1 *)puVar7;
      for (uVar6 = uVar5; uVar6 != 0; uVar6 = uVar6 - 1) {
        puVar4 = puVar3;
        puVar3 = puVar3 + 1;
        puVar2 = puVar1;
        puVar1 = puVar1 + 1;
        *puVar4 = *puVar2;
      }
      puVar8 = (undefined2 *)((int)puVar3 + (0x140 - param_3));
      puVar7 = (undefined2 *)((int)puVar1 + (param_4 - param_3));
      param_2 = param_2 + -1;
    } while (param_2 != 0);
  }
  return;
}

