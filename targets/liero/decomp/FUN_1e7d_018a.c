
bool __stdcall16far FUN_1e7d_018a(undefined1 *param_1,char *param_2,char *param_3,int *param_4)

{
  char cVar1;
  undefined1 uVar2;
  int iVar3;
  undefined2 unaff_SS;
  undefined1 *puVar4;
  undefined2 uVar5;
  undefined1 *puVar6;
  undefined2 uVar7;
  undefined1 *puVar8;
  undefined1 local_30c [256];
  undefined1 local_20c [256];
  undefined1 local_10c [8];
  char local_104 [257];
  bool local_3;
  
  puVar8 = local_30c;
  puVar6 = local_20c;
  puVar4 = local_10c;
  uVar5 = unaff_SS;
  uVar7 = unaff_SS;
  FUN_24dd_3e95(0x182,0x1e7d);
  FUN_24cb_00a7(puVar4,uVar5);
  func_0x0001e7d0(puVar6);
  FUN_24dd_3eaf(0xff,local_104,unaff_SS,uVar7,puVar8);
  iVar3 = FUN_1e7d_0082(1,0x41,local_104,unaff_SS);
  *param_4 = iVar3;
  cVar1 = FUN_1e7d_0082(0,0x49,local_104,unaff_SS);
  *param_3 = cVar1;
  cVar1 = FUN_1e7d_0082(0,0x44,local_104,unaff_SS);
  *param_2 = cVar1;
  uVar2 = FUN_1e7d_0082(0,0x48,local_104,unaff_SS);
  *param_1 = uVar2;
  local_3 = *param_4 != 0xff && local_104[0] != '\0';
  if (*param_3 == -1) {
    local_3 = false;
  }
  if (*param_2 == -1) {
    local_3 = false;
  }
  return local_3;
}

