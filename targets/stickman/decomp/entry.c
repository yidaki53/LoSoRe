
/* WARNING: This function may have set the stack pointer */

void entry(void)

{
  undefined1 uVar1;
  char cVar2;
  undefined2 extraout_DX;
  undefined2 uVar3;
  int in_BX;
  int unaff_SI;
  undefined2 unaff_ES;
  undefined2 unaff_DS;
  
  DAT_5000_749e = 0x1000;
  DAT_5000_749c = 0x5947;
  FUN_42b5_0000();
  DAT_5000_749e = 0x42b5;
  DAT_5000_749c = 0x594c;
  FUN_410e_0000();
  DAT_5000_749e = 0x410e;
  DAT_5000_749c = 0x5951;
  FUN_3faf_0ad6();
  DAT_5000_749c = 0x3faf;
  DAT_5000_749a = 0x595c;
  FUN_42b5_04df();
  DAT_5000_739c = 0x42b5;
  DAT_5000_739a = 0x5910;
  DAT_5000_7396 = 0x138;
  DAT_5000_7394 = 8;
  DAT_5000_7392 = 0x42b5;
  DAT_5000_7390 = 0x5973;
  FUN_42b5_0bde();
  DAT_5000_739c = 0x42b5;
  DAT_5000_739a = 0x5919;
  DAT_5000_7396 = 0x142;
  DAT_5000_7394 = 5;
  DAT_5000_7392 = 0x42b5;
  DAT_5000_7390 = 0x5986;
  FUN_42b5_0bde();
  *(undefined1 *)0x137 = 0;
  DAT_5000_739c = 0x42b5;
  DAT_5000_739a = 0x5990;
  FUN_3de3_18e2();
  DAT_5000_739c = 0x3de3;
  DAT_5000_739a = 0x591e;
  DAT_5000_7398 = 0x3de3;
  DAT_5000_7396 = 0x599a;
  FUN_3de3_0c99();
  DAT_5000_739c = 0x599d;
  FUN_1000_53c7();
  DAT_5000_739c = 0x59a0;
  FUN_1000_51ea();
  DAT_5000_739c = 0x59a3;
  FUN_1000_568a();
  *(undefined1 *)0x136 = 1;
  DAT_5000_739c = 0x59ab;
  FUN_1000_4e2e();
  DAT_5000_739c = 0x3de3;
  DAT_5000_739a = 0x59b0;
  FUN_3de3_1b42();
  DAT_5000_739c = 0x59b3;
  FUN_1000_3c49();
  DAT_5000_739c = 0x534a;
  DAT_5000_739a = 0x3efe;
  DAT_5000_7398 = 0x3de3;
  DAT_5000_7396 = 0x5926;
  DAT_5000_7394 = 0x3de3;
  DAT_5000_7392 = 0x59c3;
  FUN_42b5_0bc4();
  DAT_5000_7396 = 0xa6c6;
  DAT_5000_7394 = 0x42b5;
  DAT_5000_7392 = 0x59cd;
  FUN_42b5_0c51();
  DAT_5000_7398 = 0x42b5;
  DAT_5000_7396 = 0x593e;
  DAT_5000_7394 = 0x42b5;
  DAT_5000_7392 = 22999;
  FUN_42b5_0c51();
  DAT_5000_7398 = 0x42b5;
  DAT_5000_7396 = 0x5940;
  DAT_5000_7394 = 0x42b5;
  DAT_5000_7392 = 0x59e1;
  FUN_42b5_0c51();
  DAT_5000_7398 = 0x42b5;
  DAT_5000_7396 = 0x59e6;
  FUN_3de3_002d();
  DAT_5000_739c = 0x3de3;
  DAT_5000_739a = 0x59eb;
  uVar3 = extraout_DX;
  FUN_3de3_1bf7();
  DAT_5000_749e = 0x3de3;
  DAT_5000_749c = 0x59f5;
  cVar2 = FUN_42b5_00e9();
  *(char *)(in_BX + unaff_SI) = *(char *)(in_BX + unaff_SI) + cVar2;
  *(char *)(in_BX + unaff_SI) = *(char *)(in_BX + unaff_SI) + cVar2;
  *(char *)(in_BX + unaff_SI) = *(char *)(in_BX + unaff_SI) + cVar2;
  *(char *)(in_BX + unaff_SI) = *(char *)(in_BX + unaff_SI) + cVar2;
  *(char *)(in_BX + unaff_SI) = *(char *)(in_BX + unaff_SI) + cVar2;
  *(char *)0xa42 = *(char *)0xa42 + (char)uVar3;
  uVar1 = in(uVar3);
  *(undefined1 *)0x5940 = uVar1;
  do {
                    /* WARNING: Do nothing block with infinite loop */
  } while( true );
}

