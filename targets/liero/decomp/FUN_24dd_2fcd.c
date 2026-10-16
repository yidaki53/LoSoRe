
void __cdecl16near FUN_24dd_2fcd(void)

{
  int *piVar1;
  undefined1 uVar2;
  int iVar3;
  undefined2 uVar4;
  int *piVar5;
  undefined2 unaff_DS;
  bool bVar6;
  longdouble lVar7;
  longdouble lVar8;
  
  piVar5 = (int *)0x0;
  uVar4 = *(undefined2 *)0x2c;
  iVar3 = 0x7fff;
  do {
    if ((char)*piVar5 == '\0') break;
    if ((*piVar5 == 0x3738) && ((char)piVar5[1] == '=')) {
      bVar6 = ((byte)((uint)piVar5[1] >> 8) & 0xdf) == 0x59;
      goto LAB_24dd_3018;
    }
    bVar6 = true;
    do {
      if (iVar3 == 0) break;
      iVar3 = iVar3 + -1;
      piVar1 = piVar5;
      piVar5 = (int *)((int)piVar5 + 1);
      bVar6 = (char)*piVar1 == '\0';
    } while (!bVar6);
  } while (bVar6);
  out(0xf0,0);
  *(undefined2 *)0x7b40 = 0;
  *(undefined2 *)0x7b40 = 0x37f;
  iVar3 = 0x14;
  do {
    iVar3 = iVar3 + -1;
  } while (iVar3 != 0);
  bVar6 = (*(uint *)0x7b40 & 0xf3f) == 0x33f;
LAB_24dd_3018:
  uVar4 = 0x1330;
  uVar2 = 0;
  if (bVar6) {
    lVar8 = (longdouble)1 / (longdouble)0;
    lVar7 = -lVar8;
    *(uint *)0x7b40 =
         (uint)(lVar7 < lVar8) << 8 | (uint)(NAN(lVar7) || NAN(lVar8)) << 10 |
         (uint)(lVar7 == lVar8) << 0xe;
    uVar2 = 2;
    if ((*(uint *)0x7b40 & 0x4000) == 0) {
      uVar4 = 0x1332;
      uVar2 = 3;
    }
  }
  *(undefined1 *)0x6421 = uVar2;
  *(undefined2 *)0x7b3e = uVar4;
  return;
}

