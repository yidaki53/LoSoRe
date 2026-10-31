
void __stdcall16far FUN_3de3_0c99(undefined4 param_1)

{
  char cVar1;
  int iVar2;
  undefined2 unaff_SS;
  undefined1 *puVar3;
  undefined2 uVar4;
  undefined1 local_402 [256];
  undefined1 local_302 [256];
  undefined1 local_202 [256];
  undefined1 local_102 [252];
  undefined2 uStack_6;
  undefined2 uStack_4;
  
  uStack_4 = 0x3de3;
  uStack_6 = 0xead4;
  FUN_42b5_04df();
  FUN_42b5_0bde(0xff,local_102,unaff_SS,(int)param_1,(int)((ulong)param_1 >> 0x10));
  FUN_42b5_04f5(local_102,unaff_SS,local_302,unaff_SS);
  FUN_42b5_0565(0x42b5,local_302);
  iVar2 = FUN_42b5_04a2();
  if (iVar2 == 0) {
    while( true ) {
      FUN_42b5_0abd(local_302,unaff_SS);
      cVar1 = FUN_42b5_04a9();
      if (cVar1 != '\0') break;
      puVar3 = local_302;
      uVar4 = unaff_SS;
      FUN_42b5_08df(0xff,local_202,unaff_SS);
      FUN_42b5_081a(puVar3,uVar4);
      FUN_42b5_04a9();
      FUN_3de3_002d(local_202,unaff_SS);
      FUN_42b5_0abd(local_302,unaff_SS);
      cVar1 = FUN_42b5_04a9();
      if (cVar1 == '\0') {
        FUN_3de3_002d(0xc96,0x42b5);
      }
    }
    FUN_42b5_05bf(local_302,unaff_SS);
    FUN_42b5_04a9();
    FUN_405f_017d();
  }
  else {
    puVar3 = local_402;
    uVar4 = unaff_SS;
    FUN_42b5_0bc4(0xc73,0x42b5);
    FUN_42b5_0c51(local_102,unaff_SS);
    FUN_3de3_002d(puVar3,uVar4);
  }
  return;
}

