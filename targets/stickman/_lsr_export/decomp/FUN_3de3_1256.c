
void __cdecl16far FUN_3de3_1256(void)

{
  uint uVar1;
  uint uVar2;
  int iVar3;
  undefined2 uVar4;
  undefined2 uVar5;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  undefined2 local_6;
  undefined1 uStack_4;
  bool local_3;
  
  uStack_4 = 0xe3;
  local_3 = true;
  local_6 = 0xf091;
  FUN_42b5_04df();
  FUN_428f_006c(&local_6,unaff_SS,0xa8da,unaff_DS,0xa8d8,unaff_DS,0xa8d6,unaff_DS);
  FUN_428f_00a2(&local_6,unaff_SS,0xa8e0,unaff_DS,0xa8de,unaff_DS,0xa8dc,unaff_DS);
  *(int *)0xa8de = *(int *)0xa8de + *(int *)0xa7ca;
  if (0x3b < *(uint *)0xa8de) {
    *(int *)0xa8dc = *(uint *)0xa8de / 0x3c + *(int *)0xa8dc;
    *(uint *)0xa8de = *(uint *)0xa8de % 0x3c;
    if (0x17 < *(uint *)0xa8dc) {
      *(int *)0xa8da = *(uint *)0xa8dc / 0x18 + *(int *)0xa8da;
      *(uint *)0xa8dc = *(uint *)0xa8dc % 0x18;
    }
    iVar3 = *(int *)0xa8d8;
    if ((((iVar3 == 4) || (iVar3 == 5)) || (iVar3 == 9)) || (iVar3 == 0xb)) {
      local_3 = 0x1e < *(uint *)0xa8da;
    }
    else if (iVar3 == 2) {
      if (*(uint *)0xa8d6 % 4 == 0) {
        local_3 = 0x1d < *(uint *)0xa8da;
      }
      else {
        local_3 = 0x1c < *(uint *)0xa8da;
      }
    }
    else {
      local_3 = 0x1f < *(uint *)0xa8da;
    }
    if (local_3 != false) {
      *(undefined2 *)0xa8da = 1;
      *(int *)0xa8d8 = *(int *)0xa8d8 + 1;
      if (0xc < *(uint *)0xa8d8) {
        *(undefined2 *)0xa8d8 = 1;
        *(int *)0xa8d6 = *(int *)0xa8d6 + 1;
      }
    }
  }
  *(int *)0xa8d6 = *(int *)0xa8d6 + -0x76c;
  *(undefined2 *)0xa7c6 = *(undefined2 *)0xa8d6;
  *(undefined2 *)0xa7c8 = 0;
  uVar5 = *(undefined2 *)0xa7c8;
  uVar4 = FUN_42b5_0b14();
  *(undefined2 *)0xa7c6 = uVar4;
  *(undefined2 *)0xa7c8 = uVar5;
  uVar1 = *(uint *)0xa8d8;
  uVar2 = *(uint *)0xa7c6;
  iVar3 = *(int *)0xa7c8;
  *(int *)0xa7c6 = uVar1 + *(uint *)0xa7c6;
  *(int *)0xa7c8 = iVar3 + (uint)CARRY2(uVar1,uVar2);
  uVar5 = *(undefined2 *)0xa7c8;
  uVar4 = FUN_42b5_0b14();
  *(undefined2 *)0xa7c6 = uVar4;
  *(undefined2 *)0xa7c8 = uVar5;
  uVar1 = *(uint *)0xa8da;
  uVar2 = *(uint *)0xa7c6;
  iVar3 = *(int *)0xa7c8;
  *(int *)0xa7c6 = uVar1 + *(uint *)0xa7c6;
  *(int *)0xa7c8 = iVar3 + (uint)CARRY2(uVar1,uVar2);
  uVar5 = *(undefined2 *)0xa7c8;
  uVar4 = FUN_42b5_0b14();
  *(undefined2 *)0xa7c6 = uVar4;
  *(undefined2 *)0xa7c8 = uVar5;
  uVar1 = *(uint *)0xa8dc;
  uVar2 = *(uint *)0xa7c6;
  iVar3 = *(int *)0xa7c8;
  *(int *)0xa7c6 = uVar1 + *(uint *)0xa7c6;
  *(int *)0xa7c8 = iVar3 + (uint)CARRY2(uVar1,uVar2);
  uVar5 = *(undefined2 *)0xa7c8;
  uVar4 = FUN_42b5_0b14();
  *(undefined2 *)0xa7c6 = uVar4;
  *(undefined2 *)0xa7c8 = uVar5;
  uVar1 = *(uint *)0xa8de;
  uVar2 = *(uint *)0xa7c6;
  iVar3 = *(int *)0xa7c8;
  *(int *)0xa7c6 = uVar1 + *(uint *)0xa7c6;
  *(int *)0xa7c8 = iVar3 + (uint)CARRY2(uVar1,uVar2);
  uVar5 = *(undefined2 *)0xa7c8;
  uVar4 = FUN_42b5_0b14();
  *(undefined2 *)0xa7c6 = uVar4;
  *(undefined2 *)0xa7c8 = uVar5;
  uVar1 = *(uint *)0xa8e0;
  uVar2 = *(uint *)0xa7c6;
  iVar3 = *(int *)0xa7c8;
  *(int *)0xa7c6 = uVar1 + *(uint *)0xa7c6;
  *(int *)0xa7c8 = iVar3 + (uint)CARRY2(uVar1,uVar2);
  return;
}

