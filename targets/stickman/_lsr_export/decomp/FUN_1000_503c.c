
void __cdecl16near FUN_1000_503c(void)

{
  undefined1 uVar1;
  undefined2 unaff_SS;
  undefined2 unaff_DS;
  long lVar2;
  undefined1 local_16 [2];
  undefined1 local_14 [2];
  undefined1 local_12 [2];
  undefined2 local_10;
  undefined2 local_e;
  undefined2 local_c;
  uint local_a;
  uint local_8;
  undefined2 local_6;
  int local_4;
  
  local_4 = 0x1000;
  local_6 = 0x5047;
  FUN_42b5_04df();
  FUN_42b5_0bde(0x40,0x4b8,unaff_DS,0xa7d6,unaff_DS);
  *(undefined2 *)0x4f9 = 0;
  *(undefined2 *)0x4fb = 0;
  *(undefined2 *)0x4fd = 1;
  *(undefined2 *)0x4ff = 0;
  *(undefined2 *)0x501 = 0;
  *(undefined2 *)0x503 = 0;
  *(undefined2 *)0x505 = 0;
  *(undefined2 *)0x507 = 0;
  *(undefined1 *)0x509 = 1;
  *(undefined1 *)0x50a = 1;
  FUN_42b5_1a42(0,0x28,0x50b,unaff_DS);
  local_4 = 1;
  while( true ) {
    uVar1 = FUN_42b5_1279(0x100);
    *(undefined1 *)(local_4 + 0x532) = uVar1;
    if (local_4 == 0xe) break;
    local_4 = local_4 + 1;
  }
  *(undefined1 *)0x541 = 0;
  local_4 = FUN_4170_01b8(0x42,0x5015,0x42b5);
  if (local_4 == -1) {
    FUN_3de3_0278(0x5022,0x4170);
  }
  FUN_4170_02fc(0,0,2,local_4);
  lVar2 = FUN_4170_034d(local_4);
  if (lVar2 == 0) {
    FUN_428f_006c(&local_6,unaff_SS,local_12,unaff_SS,local_14,unaff_SS,local_16,unaff_SS);
    local_10 = FUN_42b5_1279(0x18);
    local_e = FUN_42b5_1279(0x3c);
    local_c = FUN_42b5_1279(0x3c);
    FUN_428f_0156(&local_a,unaff_SS,local_16,unaff_SS);
    local_a = local_a ^ 0x4abe;
    local_8 = local_8 ^ 0x2bad;
    FUN_42b5_1a1f(4,0x539,unaff_DS,&local_a,unaff_SS);
  }
  FUN_4170_02a4(0x8a,0x4b8,unaff_DS,local_4);
  FUN_4170_049d(local_4);
  return;
}

