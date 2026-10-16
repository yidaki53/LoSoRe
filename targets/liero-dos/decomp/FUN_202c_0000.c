
undefined4 __stdcall16far
FUN_202c_0000(uint param_1,int param_2,uint param_3,int param_4,uint param_5,int param_6,
             uint param_7,int param_8)

{
  code *pcVar1;
  uint uVar2;
  uint uVar3;
  undefined2 uVar4;
  int iVar5;
  int iVar6;
  undefined2 extraout_DX;
  undefined2 uVar7;
  
  iVar5 = (param_6 - param_2) - (uint)(param_5 < param_1);
  uVar2 = FUN_24dd_3d80();
  iVar6 = (param_8 - param_4) - (uint)(param_7 < param_3);
  uVar3 = FUN_24dd_3d80(uVar2,iVar5);
  pcVar1 = (code *)swi(0x37);
  (*pcVar1)(iVar6 + iVar5 + (uint)CARRY2(uVar3,uVar2));
  uVar7 = extraout_DX;
  FUN_24dd_32a9();
  uVar4 = FUN_24dd_3249();
  return CONCAT22(uVar7,uVar4);
}

