
void FUN_1000_4328(int *param_1,int *param_2)

{
  uint uVar1;
  int iVar2;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  undefined1 *puVar3;
  undefined2 uVar4;
  undefined2 uVar5;
  undefined1 local_202 [256];
  byte local_102 [252];
  undefined2 uStack_6;
  undefined2 uStack_4;
  
  uStack_4 = 0x1000;
  uStack_6 = 0x4333;
  FUN_42b5_04df();
  if (*param_1 != *(int *)0x26c4) {
    FUN_1000_3f12(*param_1);
    *param_1 = *param_1 + 1;
    if (*param_2 + 0xf < *param_1) {
      FUN_1000_3f7b();
      *param_2 = *param_2 + 6;
      if (*param_1 < *param_2) {
        *param_2 = *param_1;
      }
      FUN_1000_40d4(*param_1,*param_2);
    }
    else {
      FUN_42b5_1766(0xff,local_102,unaff_SS,0,*param_1 + -1,*param_1 + -1 >> 0xf);
      while (local_102[0] < 3) {
        puVar3 = local_202;
        uVar4 = unaff_SS;
        FUN_42b5_0bc4(0x4300,0x42b5);
        FUN_42b5_0c51(local_102,unaff_SS);
        FUN_42b5_0bde(0xff,local_102,unaff_SS,puVar3,uVar4);
      }
      uVar1 = *(uint *)((*param_1 + -1) * 0x80 + 0x2694);
      iVar2 = (int)uVar1 >> 0xf;
      if ((*(int *)0x4fb < iVar2) || ((*(int *)0x4fb <= iVar2 && (*(uint *)0x4f9 < uVar1)))) {
        FUN_3de3_002d(0x4302,0x42b5);
      }
      else {
        FUN_3de3_002d(0x4307,0x42b5);
      }
      uVar5 = 6;
      iVar2 = (*param_1 - *param_2) + 5;
      puVar3 = local_202;
      uVar4 = unaff_SS;
      FUN_42b5_0bc4(0x430e,0x3de3);
      FUN_42b5_0c51(local_102,unaff_SS);
      FUN_42b5_0c51(0x4313,0x42b5);
      FUN_3de3_0bea(puVar3,uVar4,iVar2,uVar5);
      FUN_42b5_0bde(0xff,local_102,unaff_SS,(*param_1 + -1) * 0x80 + 0x2646,unaff_DS);
      while (local_102[0] < 0x24) {
        puVar3 = local_202;
        uVar4 = unaff_SS;
        FUN_42b5_0bc4(local_102,unaff_SS);
        FUN_42b5_0c51(0x4313,0x42b5);
        FUN_42b5_0bde(0xff,local_102,unaff_SS,puVar3,uVar4);
      }
      FUN_3de3_002d(local_102,unaff_SS);
      FUN_42b5_1766(0xff,local_102,unaff_SS,0,*param_1,*param_1 >> 0xf);
      while (local_102[0] < 3) {
        puVar3 = local_202;
        uVar4 = unaff_SS;
        FUN_42b5_0bc4(0x4300,0x42b5);
        FUN_42b5_0c51(local_102,unaff_SS);
        FUN_42b5_0bde(0xff,local_102,unaff_SS,puVar3,uVar4);
      }
      uVar5 = 6;
      iVar2 = (*param_1 - *param_2) + 6;
      puVar3 = local_202;
      uVar4 = unaff_SS;
      FUN_42b5_0bc4(0x4315,0x42b5);
      FUN_42b5_0c51(local_102,unaff_SS);
      FUN_42b5_0c51(0x4313,0x42b5);
      FUN_3de3_0bea(puVar3,uVar4,iVar2,uVar5);
      FUN_42b5_0bde(0xff,local_102,unaff_SS,*param_1 * 0x80 + 0x2646,unaff_DS);
      while (local_102[0] < 0x21) {
        puVar3 = local_202;
        uVar4 = unaff_SS;
        FUN_42b5_0bc4(local_102,unaff_SS);
        FUN_42b5_0c51(0x4313,0x42b5);
        FUN_42b5_0bde(0xff,local_102,unaff_SS,puVar3,uVar4);
      }
      puVar3 = local_202;
      uVar4 = unaff_SS;
      FUN_42b5_0bc4(local_102,unaff_SS);
      FUN_42b5_0c51(0x4324,0x42b5);
      FUN_42b5_0bde(0xff,local_102,unaff_SS,puVar3,uVar4);
      FUN_3de3_002d(local_102,unaff_SS);
    }
    FUN_1000_3ed4(*param_1);
  }
  return;
}

