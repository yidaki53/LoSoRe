
/* WARNING: Removing unreachable block (ram,0x0004238e) */

uint __stdcall16far FUN_4170_0a65(undefined4 param_1,undefined4 param_2)

{
  char cVar1;
  undefined1 extraout_AH;
  undefined2 uVar2;
  undefined2 uVar3;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  undefined1 uVar4;
  long lVar5;
  undefined1 *puVar6;
  undefined1 *puVar7;
  undefined2 uVar8;
  undefined1 local_57e [256];
  undefined1 local_47e [256];
  undefined1 local_37e [6];
  undefined1 local_378 [10];
  undefined1 local_36e [68];
  undefined2 local_32a [3];
  undefined1 *local_324;
  uint local_318;
  undefined1 local_316;
  byte local_315;
  undefined4 local_216;
  int local_212;
  int local_210;
  undefined2 local_20e [2];
  uint local_20a;
  uint local_208;
  char local_205;
  byte local_204 [256];
  char local_104;
  undefined1 local_103 [253];
  undefined2 uStack_6;
  undefined2 uStack_4;
  
  uStack_4 = 0x4170;
  uStack_6 = 0x2170;
  FUN_42b5_04df();
  FUN_42b5_0bde(0xff,&local_104,unaff_SS,(int)param_2,(int)((ulong)param_2 >> 0x10));
  FUN_42b5_0bde(0xff,local_204,unaff_SS,(int)param_1,(int)((ulong)param_1 >> 0x10));
  FUN_4170_088d(&stack0xfffe,local_20e,unaff_SS,&local_20a,unaff_SS);
  local_210 = -1;
  local_212 = -1;
  local_205 = '\0';
  *(undefined1 *)0x262 = 0;
  if ((local_20a | local_208) == 0) {
    local_205 = '\x01';
    FUN_42b5_0bde(0xff,0x262,unaff_DS,0x9bf,0x42b5);
  }
  else {
    local_212 = FUN_4170_01b8(CONCAT11((char)((local_20a | local_208) >> 8),0x12),&local_104,
                              unaff_SS);
    if (local_212 == -1) {
      local_205 = '\x01';
      puVar7 = local_47e;
      uVar3 = unaff_SS;
      FUN_42b5_0bc4(0x9e6,0x42b5);
      FUN_42b5_0c51(&local_104,unaff_SS);
      FUN_42b5_0bde(0xff,0x262,unaff_DS,puVar7,uVar3);
    }
    else {
      cVar1 = FUN_4170_0812(local_204,unaff_SS);
      uVar4 = cVar1 == '\0';
      if (!(bool)uVar4) {
        uVar4 = local_204[0] == 0;
        if ((!(bool)uVar4) &&
           (((local_204[0] != 2 || (uVar4 = local_204[2] == ':', !(bool)uVar4)) &&
            (uVar4 = local_204[local_204[0]] == 0x5c, !(bool)uVar4)))) {
          puVar7 = local_47e;
          uVar3 = unaff_SS;
          FUN_42b5_0bc4(local_204,unaff_SS);
          FUN_42b5_0c51(0x9fe,0x42b5);
          FUN_42b5_0bde(0xff,local_204,unaff_SS,puVar7,uVar3);
        }
        FUN_428f_018e(local_37e,unaff_SS,local_378,unaff_SS,local_36e,unaff_SS,&local_104,unaff_SS);
        puVar7 = local_47e;
        uVar3 = unaff_SS;
        FUN_42b5_0bc4(local_204,unaff_SS);
        FUN_42b5_0c51(local_378,unaff_SS);
        FUN_42b5_0c51(local_37e,unaff_SS);
        FUN_42b5_0bde(0xff,local_204,unaff_SS,puVar7,uVar3);
      }
      FUN_4170_00c3(local_204,unaff_SS);
      FUN_4170_00c3(&local_104,unaff_SS);
      FUN_42b5_0cc9(&local_104,unaff_SS,local_204,unaff_SS);
      if ((bool)uVar4) {
        local_205 = '\x01';
        FUN_42b5_0bde(0xff,0x262,unaff_DS,0xa00,0x42b5);
      }
      else {
        FUN_4170_0570(local_204,unaff_SS);
        local_216 = FUN_4170_0449(local_212);
        if ((local_204[0] < 2) || (local_204[2] != ':')) {
          FUN_42b5_0bde(0xff,&local_316,unaff_SS,0xa23,0x42b5);
        }
        else {
          FUN_42b5_0bde(0xff,&local_316,unaff_SS,local_204,unaff_SS);
        }
        uVar3 = 0x428f;
        lVar5 = FUN_428f_00de(local_315 - 0x40);
        if (lVar5 < local_216) {
          local_205 = '\x01';
          if (local_315 == 0x40) {
            uVar3 = 0x42b5;
            FUN_42b5_1ade(0xff,&local_316,unaff_SS,(uint)lVar5 & 0xff00);
          }
          puVar7 = local_57e;
          uVar8 = unaff_SS;
          FUN_42b5_0bc4(0xa25,uVar3);
          puVar6 = local_47e;
          uVar3 = unaff_SS;
          uVar2 = FUN_42b5_1bc4(CONCAT11(extraout_AH,local_315));
          FUN_42b5_0cf4(uVar2);
          FUN_42b5_0c51(puVar6,uVar3);
          FUN_42b5_0c51(0xa46,0x42b5);
          FUN_42b5_0bde(0xff,0x262,unaff_DS,puVar7,uVar8);
        }
        else {
          local_210 = FUN_4170_0123(local_204,unaff_SS);
          if (local_210 == -1) {
            local_205 = '\x01';
            puVar7 = local_47e;
            uVar3 = unaff_SS;
            FUN_42b5_0bc4(0xa48,0x428f);
            FUN_42b5_0c51(local_204,unaff_SS);
            FUN_42b5_0bde(0xff,0x262,unaff_DS,puVar7,uVar3);
          }
          else {
            FUN_4170_0911(&stack0xfffe);
          }
        }
      }
    }
    FUN_42b5_0254(local_20e[0],local_20a,local_208);
  }
  if (local_212 != -1) {
    FUN_4170_049d(local_212);
  }
  if (local_210 != -1) {
    FUN_4170_049d(local_210);
  }
  if (local_205 == '\0') {
    uStack_4 = CONCAT11(1,(undefined1)uStack_4);
    local_32a[0] = 0x4300;
    local_324 = local_103;
    puVar7 = local_47e;
    uVar3 = unaff_SS;
    FUN_42b5_0bc4(&local_104,unaff_SS);
    FUN_42b5_0c51(0xa63,0x42b5);
    FUN_42b5_0bde(0xff,&local_104,unaff_SS,puVar7,uVar3);
    local_104 = local_104 + -1;
    FUN_428f_0000(0x42b5,local_32a);
    if ((local_318 & 1) == 0) {
      local_32a[0] = 0x4301;
      FUN_428f_0000(0x428f,local_32a);
    }
  }
  else {
    uStack_4 = 0;
  }
  return uStack_4 >> 8;
}

